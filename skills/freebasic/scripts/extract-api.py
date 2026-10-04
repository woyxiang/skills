#!/usr/bin/env python3
"""
Extract API entries from FreeBASIC manual HTML files (stdlib only).

Parses KeyPg*.html pages into data/api.json. Each entry keeps:
  - clean description (intro prose only, not polluted with the Syntax block)
  - syntax/usage with line breaks preserved (one overload per line)
  - parameter names AND descriptions
  - example code with whitespace intact (spaces are `&nbsp;` in the manual)
  - expected example output when the page shows one

Category and doc routing come from the manual's own CatPg*.html category pages.

Usage:
    python scripts/extract-api.py [--manual DIR] [--output FILE]

Manual directory resolution:
    --manual DIR, then $FREEBASIC_MANUAL_DIR, then ../references/FB-manual,
    then E:/scoop/apps/freebasic/current/doc/FB-manual-1.10.1-html
"""

import argparse
import json
import os
import re
import sys
from html import unescape
from pathlib import Path
from typing import Optional

MANUAL_VERSION = "1.10.1"

# CatPg*.html page -> (category, skill doc)
CATEGORY_MAP = {
    "CatPgArray": ("arrays", "arrays.md"),
    "CatPgBits": ("types", "types.md"),
    "CatPgCasting": ("types", "types.md"),
    "CatPgCompilerSwitches": ("compiler", "compiler.md"),
    "CatPgCompOpt": ("compiler", "compiler.md"),
    "CatPgConsole": ("console", "basics.md"),
    "CatPgControlFlow": ("control-flow", "control-flow.md"),
    "CatPgDate": ("date-time", "date-time.md"),
    "CatPgDddefines": ("preprocessor", "preprocessor.md"),
    "CatPgError": ("error-handling", "error-handling.md"),
    "CatPgFile": ("file-io", "file-io.md"),
    "CatPgGfx": ("graphics", "graphics.md"),
    "CatPgGfx2D": ("graphics", "graphics.md"),
    "CatPgGfxInput": ("graphics", "graphics.md"),
    "CatPgGfxScreen": ("graphics", "graphics.md"),
    "CatPgInput": ("console", "basics.md"),
    "CatPgMath": ("math", "math.md"),
    "CatPgMemory": ("pointers", "pointers.md"),
    "CatPgMisc": ("general", "basics.md"),
    "CatPgModularizing": ("procedures", "procedures.md"),
    "CatPgOpArithmetic": ("operators", "operators.md"),
    "CatPgOpAssignment": ("operators", "operators.md"),
    "CatPgOpConditional": ("operators", "operators.md"),
    "CatPgOpIndex": ("operators", "operators.md"),
    "CatPgOpIndexing": ("operators", "operators.md"),
    "CatPgOpIterating": ("operators", "operators.md"),
    "CatPgOpLogical": ("operators", "operators.md"),
    "CatPgOpMemory": ("operators", "operators.md"),
    "CatPgOpPoint": ("operators", "pointers.md"),
    "CatPgOpPrepro": ("operators", "preprocessor.md"),
    "CatPgOpShortCircuit": ("operators", "operators.md"),
    "CatPgOpString": ("operators", "operators.md"),
    "CatPgOpTypeclass": ("operators", "operators.md"),
    "CatPgOpsys": ("general", "basics.md"),
    "CatPgPreProcess": ("preprocessor", "preprocessor.md"),
    "CatPgProcedures": ("procedures", "procedures.md"),
    "CatPgProgrammer": ("compiler", "compiler.md"),
    "CatPgStdDataTypes": ("types", "types.md"),
    "CatPgString": ("strings", "strings.md"),
    "CatPgThreading": ("threading", "threading.md"),
    "CatPgUserDefTypes": ("user-defined-types", "user-defined-types.md"),
    "CatPgVariables": ("types", "types.md"),
}
SKIP_CAT_PAGES = {"CatPgFullIndex", "CatPgFunctIndex", "CatPgOperators"}

BR_TAG = re.compile(r"<br[^>]*>", re.I)
ANY_TAG = re.compile(r"<[^>]+>")
SECT_TITLE = re.compile(r'<div class="fb_sect_title">')


# ---------- text extraction helpers ----------

def html_to_text(html: str, keep_lines: bool = False) -> str:
    """HTML fragment -> text. keep_lines=True turns <br> into newlines (code);
    otherwise breaks collapse to spaces (prose)."""
    html = BR_TAG.sub("\n" if keep_lines else " ", html)
    text = unescape(ANY_TAG.sub("", html)).replace("\xa0", " ").replace("\r", "")
    if keep_lines:
        lines = [re.sub(r"[ \t]+", " ", ln).rstrip() for ln in text.split("\n")]
        return "\n".join(ln for ln in lines if ln.strip())
    return re.sub(r"\s+", " ", text).strip()


def cap_text(text: str, limit: int) -> str:
    if len(text) <= limit:
        return text
    cut = text[:limit]
    pos = max(cut.rfind(". "), cut.rfind("; "))
    if pos > limit // 2:
        return cut[: pos + 1].strip()
    return cut.rsplit(" ", 1)[0].strip() + "..."


def get_body_html(page: str) -> Optional[str]:
    m = re.search(r'<div id="fb_pg_body">', page)
    return page[m.end():] if m else None


def split_sections(body_html: str):
    """Return (intro_text, [(title, content_html), ...])."""
    marks = list(SECT_TITLE.finditer(body_html))
    intro = html_to_text(body_html[: marks[0].start()]) if marks else html_to_text(body_html)
    sections = []
    for i, m in enumerate(marks):
        start = m.end()
        end = marks[i + 1].start() if i + 1 < len(marks) else len(body_html)
        chunk = body_html[start:end]
        t_end = chunk.find("</div>")
        title = html_to_text(chunk[:t_end]) if t_end != -1 else ""
        content = chunk[t_end + len("</div>"):] if t_end != -1 else chunk
        sections.append((title.strip(), content))
    return intro, sections


def find_section(sections, *titles: str) -> Optional[str]:
    wanted = {t.lower() for t in titles}
    for title, content in sections:
        if title.lower() in wanted:
            return content
    return None


# ---------- field extractors ----------

def normalize_name(raw: str) -> tuple:
    """'(Print | ?) #' -> ('Print #', ['? #']); '(Pointer | Ptr)' -> ('Pointer', ['Ptr'])"""
    raw = raw.strip()
    m = re.match(r"^\(([^|)]+)\s*\|\s*([^)]+)\)\s*(.*)$", raw)
    if m:
        a, b, suffix = m.group(1).strip(), m.group(2).strip(), m.group(3).strip()
        return f"{a} {suffix}".strip(), [f"{b} {suffix}".strip()]
    return raw, []


def extract_title(page: str) -> tuple:
    m = re.search(r'<div id="fb_tab_l">(.*?)</div>', page, re.S)
    if m:
        return normalize_name(html_to_text(m.group(1)))
    return "", []


def extract_syntax(sections) -> str:
    cont = find_section(sections, "Syntax")
    return html_to_text(cont, keep_lines=True) if cont else ""


def extract_usage(sections) -> str:
    cont = find_section(sections, "Usage")
    return html_to_text(cont, keep_lines=True) if cont else ""


def extract_parameters(sections) -> list:
    """Parameters section: <tt><i>name</i></tt> then <div class="fb_indent">description"""
    params = []
    cont = find_section(sections, "Parameters")
    if not cont:
        return params
    for tt_html, desc_html in re.findall(
        r"(<tt>.*?</tt>)\s*(?:<br[^>]*>\s*)*<div class=\"fb_indent\">(.*?)</div>", cont, re.S
    ):
        desc = html_to_text(desc_html)[:300]
        for name_html in re.findall(r"<i>(.*?)</i>", tt_html, re.S):
            name = html_to_text(name_html)
            if name and name != "i":
                params.append({"name": name, "description": desc})
    return params


def extract_examples(sections) -> tuple:
    """<div class="freebasic"> code with &nbsp; spacing intact + expected output tail."""
    examples = []
    output = ""
    cont = find_section(sections, "Example", "Examples") or ""
    for m in re.finditer(r'<div class="freebasic">(.*?)</div>', cont, re.S):
        code = html_to_text(m.group(1), keep_lines=True)
        if code:
            examples.append(code)
        # expected output lives in a <pre>/<tt> block right after "will produce ..."
        m2 = re.search(
            r"(?:will produce|prints?|output)[^<]{0,60}(?:<br[^>]*>\s*)*"
            r"(?:<pre[^>]*>|<tt[^>]*>)(.*?)(?:</pre>|</tt>)",
            cont[m.end():], re.S | re.I,
        )
        if m2:
            output = html_to_text(m2.group(1), keep_lines=True)
    return examples, output


def extract_section_text(sections, *titles: str, limit: int = 500) -> Optional[str]:
    cont = find_section(sections, *titles)
    if not cont:
        return None
    text = html_to_text(cont)
    return text[:limit] if text else None


def extract_see_also(sections) -> list:
    cont = find_section(sections, "See also")
    if not cont:
        return []
    names = []
    for _, label in re.findall(r'<a href="(KeyPg\w+\.html)"[^>]*>([^<]*)</a>', cont):
        if label.strip():
            names.append(html_to_text(label))
    return names


# ---------- category mapping ----------

def build_category_map(manual_dir: Path) -> dict:
    """KeyPg file -> (category, doc), from the manual's CatPg index pages."""
    mapping = {}
    for stem, (category, doc) in CATEGORY_MAP.items():
        if stem in SKIP_CAT_PAGES:
            continue
        f = manual_dir / f"{stem}.html"
        if not f.exists():
            continue
        page = f.read_text(encoding="utf-8", errors="replace")
        for keypg in re.findall(r'href="(KeyPg\w+\.html)"', page):
            mapping.setdefault(keypg, (category, doc))
    return mapping


# ---------- page parsing ----------

def parse_keyword_file(html_path: Path, cat_map: dict) -> Optional[dict]:
    try:
        page = html_path.read_text(encoding="utf-8", errors="replace")
        body = get_body_html(page)
        if body is None:
            return None

        name, aliases = extract_title(page)
        if not name:
            return None

        intro, sections = split_sections(body)
        category, doc = cat_map.get(html_path.name, ("general", "basics.md"))
        examples, example_output = extract_examples(sections)

        return {
            "name": name,
            "aliases": aliases,
            "category": category,
            "doc": doc,
            "syntax": extract_syntax(sections),
            "usage": extract_usage(sections),
            "description": cap_text(intro, 300),
            "parameters": extract_parameters(sections),
            "return": extract_section_text(sections, "Return Value", limit=300),
            "examples": examples,
            "example_output": example_output or None,
            "dialect_differences": extract_section_text(sections, "Dialect Differences"),
            "qb_differences": extract_section_text(sections, "Differences from QB"),
            "see_also": extract_see_also(sections),
            "file": html_path.name,
        }
    except Exception as e:  # keep going; report at the end
        print(f"Error parsing {html_path}: {e}", file=sys.stderr)
        return None


def find_manual_dir(explicit: Optional[str]) -> Path:
    candidates = []
    if explicit:
        candidates.append(explicit)
    if os.environ.get("FREEBASIC_MANUAL_DIR"):
        candidates.append(os.environ["FREEBASIC_MANUAL_DIR"])
    base_dir = Path(__file__).resolve().parent.parent
    candidates.append(str(base_dir.parent / "references" / "FB-manual"))
    candidates.append(r"E:\scoop\apps\freebasic\current\doc\FB-manual-1.10.1-html")
    for c in candidates:
        p = Path(c)
        if p.is_dir() and any(p.glob("KeyPg*.html")):
            return p
    print("Error: FreeBASIC manual directory not found. Use --manual DIR.", file=sys.stderr)
    sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="Extract FreeBASIC API data from manual HTML")
    parser.add_argument("--manual", help="Path to FB-manual-*-html directory")
    parser.add_argument("--output", help="Output JSON path (default: data/api.json)")
    args = parser.parse_args()

    base_dir = Path(__file__).resolve().parent.parent
    manual_dir = find_manual_dir(args.manual)
    output_file = Path(args.output) if args.output else base_dir / "data" / "api.json"

    print(f"Scanning {manual_dir}...")
    keypg_files = sorted(manual_dir.glob("KeyPg*.html"))
    print(f"Found {len(keypg_files)} keyword files")

    cat_map = build_category_map(manual_dir)
    print(f"Category map covers {len(cat_map)} keyword files")

    keywords = []
    for i, html_file in enumerate(keypg_files):
        if i % 100 == 0:
            print(f"Processing {i}/{len(keypg_files)}...")
        entry = parse_keyword_file(html_file, cat_map)
        if entry:
            keywords.append(entry)

    keywords.sort(key=lambda k: k["name"].lower())
    print(f"\nExtracted {len(keywords)} keyword entries")

    output_file.parent.mkdir(parents=True, exist_ok=True)
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(
            {
                "version": MANUAL_VERSION,
                "source": f"FreeBASIC manual {MANUAL_VERSION} (FB-manual-{MANUAL_VERSION}-html)",
                "count": len(keywords),
                "keywords": keywords,
            },
            f,
            indent=2,
            ensure_ascii=False,
        )
    print(f"Written to {output_file}")


if __name__ == "__main__":
    main()
