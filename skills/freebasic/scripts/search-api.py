#!/usr/bin/env python3
"""
Search the FreeBASIC API using BM25 ranking over data/api.json.

Usage:
    python scripts/search-api.py "print to screen"          # full-text search
    python scripts/search-api.py "array dimension" --top 5  # limit results
    python scripts/search-api.py --name Print -v            # keyword lookup
    python scripts/search-api.py --name "?"                 # aliases work too
    python scripts/search-api.py --list-categories          # browse categories
    python scripts/search-api.py "string" --json            # machine-readable
"""

import argparse
import json
import math
import re
import sys
from pathlib import Path

K1 = 1.5
B = 0.75
NAME_BONUS = 4.0     # per query term found in the keyword name
EXACT_NAME_BONUS = 15.0  # query is exactly the keyword name


def tokenize(text: str) -> list:
    if not text:
        return []
    return re.findall(r"[a-z0-9]+", text.lower())


def name_tokens(name: str) -> set:
    """Tokenize keeping '#' significant, so '#print' does not match 'print'."""
    return set(re.findall(r"[#a-z0-9]+", (name or "").lower()))


def bm25_score(terms: list, doc_id: int, index: dict, doc_lengths: list,
               avg_length: float, doc_count: int) -> float:
    score = 0.0
    for term in terms:
        if term not in index["inverted"]:
            continue
        term_info = index["inverted"][term]
        df = term_info["df"]
        idf = math.log((doc_count - df + 0.5) / (df + 0.5) + 1)
        for posting in term_info["postings"]:
            if posting["doc_id"] != doc_id:
                continue
            tf = posting["tf"]
            weight = posting["weight"]
            doc_len = doc_lengths[doc_id]
            numerator = tf * (K1 + 1)
            denominator = tf + K1 * (1 - B + B * doc_len / avg_length)
            score += idf * (numerator / denominator) * weight
            break
    return score


def search(query: str, index: dict, top: int = 10) -> list:
    terms = tokenize(query)
    if not terms:
        return []

    doc_count = index["document_count"]
    avg_length = index["average_length"]
    doc_lengths = index["doc_lengths"]
    q = query.strip().lower()

    scores = []
    for doc_id in range(doc_count):
        score = bm25_score(terms, doc_id, index, doc_lengths, avg_length, doc_count)
        if score <= 0:
            continue
        # Boost hits on the keyword name itself: "print" should prefer Print
        # over #print (whose name token is '#print').
        nt = name_tokens(index["doc_names"][doc_id])
        score += NAME_BONUS * sum(1 for t in terms if t in nt)
        if index["doc_names"][doc_id].strip().lower() == q:
            score += EXACT_NAME_BONUS
        scores.append((doc_id, score))

    scores.sort(key=lambda x: -x[1])
    return scores[:top]


def lookup(name: str, api_data: dict):
    """Find a keyword by name or alias. Returns (entry, candidates).

    Tries: exact name, exact alias, case-insensitive, whitespace-insensitive,
    then falls back to substring candidates for the error message.
    """
    want = name.strip()
    want_lower = want.lower()
    want_compact = re.sub(r"[\s$]", "", want_lower)

    by_substring = []
    for kw in api_data["keywords"]:
        names = [kw["name"]] + list(kw.get("aliases") or [])
        for n in names:
            nl = n.lower()
            if nl == want_lower or re.sub(r"[\s$]", "", nl) == want_compact:
                return kw, []
            if want_lower and want_lower in nl:
                by_substring.append(kw)
                break
    return None, by_substring


def clean_text(text: str) -> str:
    if not text:
        return ""
    return text.replace("\xa0", " ").replace("\u200b", "")


def print_entry(entry: dict, verbose: bool = False):
    print(f"\n=== {clean_text(entry['name'])} ===")
    if entry.get("aliases"):
        print(f"Aliases: {', '.join(entry['aliases'])}")
    print(f"Category: {entry['category']}  (doc: {entry.get('doc', '?')})")
    print(f"Syntax: {clean_text(entry['syntax'])}")
    print(f"Description: {clean_text(entry['description'])}")
    if entry.get("usage"):
        print(f"Usage: {clean_text(entry['usage'])}")
    if entry.get("parameters"):
        print("\nParameters:")
        for p in entry["parameters"]:
            print(f"  {p['name']}: {clean_text(p.get('description', ''))}")
    if entry.get("return"):
        print(f"\nReturn: {clean_text(entry['return'])}")
    if entry.get("examples"):
        print("\nExamples:")
        limit = len(entry["examples"]) if verbose else 1
        for ex in entry["examples"][:limit]:
            print(ex if verbose else clean_text(ex)[:200])
        if entry.get("example_output"):
            print(f"Output: {clean_text(entry['example_output'])}")
    if entry.get("see_also"):
        print(f"\nSee also: {', '.join(entry['see_also'])}")
    if verbose and entry.get("dialect_differences"):
        print(f"\nDialect differences: {clean_text(entry['dialect_differences'])}")
    if verbose and entry.get("qb_differences"):
        print(f"QB differences: {clean_text(entry['qb_differences'])}")
    print(f"Source: {entry['file']} (FreeBASIC manual)")


def list_categories(api_data: dict):
    cats = {}
    for kw in api_data["keywords"]:
        cats.setdefault(kw.get("category", "unknown"), []).append(kw["name"])
    print("Available categories:")
    for cat in sorted(cats):
        names = cats[cat]
        sample = ", ".join(sorted(names)[:6])
        print(f"  {cat} ({len(names)}): {sample}...")
    print(f"\nTotal: {len(api_data['keywords'])} keywords. "
          "Use --name to look up one, or a query to search.")


def main():
    parser = argparse.ArgumentParser(description="Search FreeBASIC API using BM25")
    parser.add_argument("query", nargs="?", help="Search query")
    parser.add_argument("--top", "-n", type=int, default=5,
                        help="Number of results (default: 5)")
    parser.add_argument("--json", "-j", action="store_true", help="Output JSON")
    parser.add_argument("--name", help="Keyword name or alias lookup")
    parser.add_argument("--list-categories", action="store_true",
                        help="List all categories with sample keywords")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")
    args = parser.parse_args()

    base_dir = Path(__file__).resolve().parent.parent  # skills/freebasic
    with open(base_dir / "data" / "api.json", encoding="utf-8") as f:
        api_data = json.load(f)
    with open(base_dir / "data" / "api-bm25.json", encoding="utf-8") as f:
        index = json.load(f)

    if index.get("api_version") and index["api_version"] != api_data.get("version"):
        print(f"warning: search index built for manual {index['api_version']} "
              f"but api.json is {api_data.get('version')}; rebuild with "
              "scripts/build-index.py", file=sys.stderr)

    if args.list_categories:
        list_categories(api_data)
        return

    if args.name:
        entry, candidates = lookup(args.name, api_data)
        if entry:
            print_entry(entry, verbose=args.verbose)
            return
        if candidates:
            # ambiguous name (e.g. "Mid" -> "Mid (Function)", "Mid (Statement)"):
            # show every match so the answer is still useful
            matches = list({c["name"]: c for c in candidates}.values())
            for c in matches[:5]:
                print_entry(c, verbose=args.verbose)
            if len(matches) > 5:
                print("\n(" + str(len(matches)) + " matches; refine with --name 'Exact Name')")
            return
        print(f"Keyword '{args.name}' not found.")
        print("Try --list-categories, or search with a query.")
        sys.exit(1)

    if not args.query:
        list_categories(api_data)
        return

    results = search(args.query, index, args.top)
    if args.json:
        output = []
        for doc_id, score in results:
            kw = dict(api_data["keywords"][doc_id])
            kw["score"] = round(score, 4)
            output.append(kw)
        print(json.dumps(output, indent=2, ensure_ascii=False))
        return

    print(f"\nSearch results for '{args.query}' (top {len(results)}):")
    print("-" * 60)
    for doc_id, score in results:
        kw = api_data["keywords"][doc_id]
        name = clean_text(kw["name"])
        desc = clean_text(kw["description"])[:100]
        syntax = clean_text(kw["syntax"])[:80]
        print(f"\n{name} (score: {score:.3f})  [{kw.get('doc', '?')}]")
        print(f"  {desc}...")
        print(f"  Syntax: {syntax}...")


if __name__ == "__main__":
    main()
