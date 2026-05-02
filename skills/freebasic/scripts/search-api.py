#!/usr/bin/env python3
"""
Search FreeBASIC API using BM25 ranking.
Usage: python search-api.py "query" [--top N] [--json] [--kind TYPE] [--name NAME] [-v]
"""

import argparse
import json
import math
import re
from pathlib import Path

K1 = 1.5
B = 0.75
WEIGHTS = {'name': 3.0, 'syntax': 2.0, 'description': 1.0, 'category': 1.5, 'parameters': 1.0}


def tokenize(text: str) -> list:
    if not text:
        return []
    text = text.lower()
    return re.findall(r'[a-z0-9]+', text)


def bm25_score(terms: list, doc_id: int, index: dict, doc_lengths: list, avg_length: float, doc_count: int) -> float:
    score = 0.0
    for term in terms:
        if term not in index['inverted']:
            continue
        term_info = index['inverted'][term]
        df = term_info['df']
        idf = math.log((doc_count - df + 0.5) / (df + 0.5) + 1)

        for posting in term_info['postings']:
            if posting['doc_id'] != doc_id:
                continue
            tf = posting['tf']
            weight = posting['weight']
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

    doc_count = index['document_count']
    avg_length = index['average_length']
    doc_lengths = index['doc_lengths']

    scores = []
    for doc_id in range(doc_count):
        score = bm25_score(terms, doc_id, index, doc_lengths, avg_length, doc_count)
        if score > 0:
            scores.append((doc_id, score))

    scores.sort(key=lambda x: -x[1])
    return scores[:top]


def clean_text(text: str) -> str:
    """Clean text for display - remove nbsp and fix encoding issues."""
    if not text:
        return ""
    # Replace non-breaking spaces and other problematic chars
    text = text.replace('\xa0', ' ')
    text = text.replace('​', '')  # zero-width space
    return text


def exact_lookup(name: str, api_data: dict) -> dict | None:
    name_lower = name.lower().strip()
    # Exact match on name
    for kw in api_data['keywords']:
        if kw['name'].lower() == name_lower:
            return kw
    return None


def list_all_keywords(api_data: dict) -> list:
    """List all keyword names, sorted."""
    return sorted([kw['name'] for kw in api_data['keywords']])


def main():
    parser = argparse.ArgumentParser(description='Search FreeBASIC API using BM25')
    parser.add_argument('query', nargs='?', help='Search query')
    parser.add_argument('--top', '-n', type=int, default=5, help='Number of results (default: 5)')
    parser.add_argument('--json', '-j', action='store_true', help='Output JSON')
    parser.add_argument('--name', help='Exact keyword name lookup')
    parser.add_argument('-v', '--verbose', action='store_true', help='Verbose output')
    args = parser.parse_args()

    base_dir = Path(__file__).parent.parent  # skills/freebasic
    api_file = base_dir / "data" / "api.json"
    index_file = base_dir / "data" / "api-bm25.json"

    with open(api_file, encoding='utf-8') as f:
        api_data = json.load(f)
    with open(index_file, encoding='utf-8') as f:
        index = json.load(f)

    if args.name:
        result = exact_lookup(args.name, api_data)
        if result:
            if args.json:
                print(json.dumps(result, indent=2, ensure_ascii=False))
            else:
                name = clean_text(result['name'])
                print(f"\n=== {name} ===")
                print(f"Category: {result['category']}")
                print(f"Syntax: {clean_text(result['syntax'])}")
                print(f"Description: {clean_text(result['description'][:300])}")
                if result.get('parameters'):
                    print("\nParameters:")
                    for p in result['parameters']:
                        pname = clean_text(p.get('name', ''))
                        pdesc = clean_text(p.get('description', ''))[:100]
                        if pname:
                            print(f"  {pname}: {pdesc}")
                if result.get('return'):
                    print(f"\nReturn: {clean_text(result['return'])}")
                if result.get('examples') and result['examples']:
                    print("\nExamples:")
                    for ex in result['examples'][:2]:
                        ex_clean = clean_text(ex)[:100]
                        print(f"  {ex_clean}...")
                if result.get('see_also'):
                    see_also = clean_text(', '.join(result['see_also']))
                    print(f"\nSee also: {see_also}")
                print(f"Source: {result['file']}")
        else:
            print(f"Keyword '{args.name}' not found. Try '(Print | ?)' or search with --json to see all names.")
            exit(1)
        return

    if not args.query:
        # List categories or show all keywords
        cats = {}
        for kw in api_data['keywords']:
            cat = kw.get('category', 'unknown')
            cats[cat] = cats.get(cat, 0) + 1
        print("Available categories:")
        for cat, count in sorted(cats.items()):
            print(f"  {cat}: {count} keywords")
        print(f"\nTotal: {len(api_data['keywords'])} keywords. Use --name to look up a specific keyword.")
        return

    results = search(args.query, index, args.top)

    if args.json:
        output = []
        for doc_id, score in results:
            kw = api_data['keywords'][doc_id]
            kw['score'] = round(score, 4)
            output.append(kw)
        print(json.dumps(output, indent=2))
    else:
        print(f"\nSearch results for '{args.query}' (top {len(results)}):")
        print("-" * 60)
        for doc_id, score in results:
            kw = api_data['keywords'][doc_id]
            name = clean_text(kw['name'])
            desc = clean_text(kw['description'][:100])
            syntax = clean_text(kw['syntax'][:80])
            print(f"\n{name} (score: {score:.3f})")
            print(f"  {desc}...")
            print(f"  Syntax: {syntax}...")


if __name__ == "__main__":
    main()