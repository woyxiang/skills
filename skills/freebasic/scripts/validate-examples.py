#!/usr/bin/env python3
"""
Compile-check every fenced ```freebasic code block in the skill docs.

Each snippet is extracted from the Markdown, wrapped until it compiles as a
FreeBASIC module, and compiled with `fbc`. This catches doc errors like wrong
type names, undefined keywords and invalid identifiers before they reach the
model. Snippets marked with a `...` placeholder are considered intentionally
incomplete and are skipped.

Wrapping tiers (first one that compiles wins):
  1. as-is               full programs
  2. wrapped in a Sub    statement fragments
  3. + common Dims       fragments using shared placeholder variables
  4. + Print wrapping    bare expression fragments like `Left$(s, 4)`

Usage:
    python scripts/validate-examples.py                 # all *.md
    python scripts/validate-examples.py strings.md      # specific files
    python scripts/validate-examples.py --json          # machine-readable
    python scripts/validate-examples.py --keep          # keep temp files
    python scripts/validate-examples.py -v              # show wrapped code
"""

import argparse
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

FENCE = re.compile(r"```freebasic\r?\n(.*?)```", re.S)
DECL = re.compile(r"\b(?:Dim|Const|Static|Redim|Common)\b(?:\s+Shared)?\s+(\w+)", re.I)
SUBDEF = re.compile(r"^\s*(?:Sub|Function|Type|Enum|Union)\s+(\w+)", re.I | re.M)

# placeholder names frequently used by doc fragments, with a plausible type
COMMON_VARS = {
    "x": "Integer", "y": "Integer", "i": "Integer", "j": "Integer",
    "n": "Integer", "k": "Integer", "count": "Integer", "sum": "Integer",
    "result": "Integer", "value": "Integer", "age": "Integer", "flag": "Integer",
    "index": "Integer", "fn": "Integer", "f": "Integer",
    "s": "String", "s1": "String", "s2": "String",
    "text": "String", "filename": "String",
    "buffer": "String", "condition": "Integer", "ok": "Integer",
    "handle": "Any Ptr", "mutex": "Any Ptr", "param": "Any Ptr",
    "d": "Double", "pi": "Double",
    "startTime": "Double", "elapsed": "Double",
}

SKIP_PATTERNS = [
    re.compile(r"^\s*\.\.\.", re.M),                  # intentional placeholder
    re.compile(r"' \.\.\."),                           # trailing placeholder comment
    re.compile(r"#include\s+\"windows\.bi\"", re.I),  # Windows-only API
    re.compile(r"\$\s*include", re.I),                # meta-statement demo
    re.compile(r"Declare\s+(?:Function|Sub)", re.I),  # signature demo, no body
    re.compile(r"^[ 	]*#error", re.I | re.M),      # #error aborts by design
]

STATEMENT_START = re.compile(
    r"^\s*(?:Dim|Const|Static|Redim|If|Else|ElseIf|For|Next|While|Wend|Do|Loop|"
    r"Select|Case|Sub|Function|End|Type|Union|Enum|Print|Input|Locate|Open|Close|"
    r"Get|Put|Write|Seek|Line|Circle|Pset|Preset|Screen|Def|Lock|Unlock|Width|View|Window|Paint|Poke|Beep|Clear|Palette|Paint|Draw|Poke|Peek|Beep|BLoad|BSave|Width|View|Window|Color|Cls|Sleep|Shell|"
    r"Kill|Name|ChDir|MkDir|RmDir|On|Goto|GoSub|Return|Exit|Continue|Goto|Assert|"
    r"AssertWarn|Error|Resume|Randomize|Swap|Erase|Restore|Read|Data|With|Lock|"
    r"Unlock|Thread|Mutex|Dim|\?|:|#|\w+\s*(?:=|\+=|-=|\*=|/=|\=|\^=|And=|Or=|Xor=|Mod=|Shl=|Shr=))",
    re.I,
)


def find_blocks(md_file: Path):
    """Yield (start_line, code) for each freebasic block in a markdown file."""
    text = md_file.read_text(encoding="utf-8")
    for m in FENCE.finditer(text):
        start_line = text[: m.start()].count("\n") + 1
        yield start_line, m.group(1)


def needs_skip(code: str) -> bool:
    return any(p.search(code) for p in SKIP_PATTERNS)


def declared_names(code: str) -> set:
    names = set(DECL.findall(code))
    names.update(SUBDEF.findall(code))
    # "Dim [Shared] As <Type> [Ptr] a, b, c"
    for m in re.finditer(r"\bDim\b(?:\s+Shared)?\s+As\s+\w+(?:\s+Ptr)*\s+([^'\n=]+)", code, re.I):
        names.update(re.findall(r"\w+", m.group(1)))
    return {n.lower() for n in names}


def inject_common_dims(code: str) -> str:
    """Declare placeholder variables the snippet forgot to declare."""
    have = declared_names(code)
    dims = [
        f"Dim As {typ} {name}"
        for name, typ in sorted(COMMON_VARS.items())
        if name.lower() not in have
    ]
    return "\n".join(dims) + "\n" + code if dims else code


def wrap_sub(code: str) -> str:
    return "Sub __snippet()\n" + code + "\nEnd Sub\n"


def wrap_expressions(code: str) -> str:
    """Turn bare expression lines like `Left$(s, 4) ' "Free"` into Print statements."""
    out = []
    for line in code.split("\n"):
        stripped = line.strip()
        comment = ""
        if "'" in line:
            head, tail = line.split("'", 1)
            if '"' not in head or head.count('"') % 2 == 0:
                line, comment = head, "'" + tail
        s = line.strip()
        if (
            s
            and not STATEMENT_START.match(s)
            and "=" not in s
            and re.match(r"^([A-Za-z_]\w*[$%&!#]?|\"|[0-9.])", s)
        ):
            line = f"Print ({s})"
        out.append(line + ((" " + comment) if comment and line.strip() else comment.rstrip()))
    return "\n".join(out)


def compile_check(code: str, tmpdir: Path, tag: str):
    src = tmpdir / f"snippet_{tag}.bas"
    src.write_text(code, encoding="utf-8")
    r = subprocess.run(
        ["fbc", "-w", "all", "-c", str(src)],
        capture_output=True, text=True, timeout=60,
    )
    if r.returncode == 0:
        return True, ""
    lines = (r.stderr or r.stdout).strip().splitlines()
    for ln in lines:
        if "error" in ln.lower():
            return False, ln.strip()
    lines = [ln for ln in lines if ln.strip() and not ln.strip().startswith("Compiling")]
    return False, lines[0].strip() if lines else "unknown error"


def validate_block(code: str, tmpdir: Path, tag: str):
    """Try wrapping tiers until the snippet compiles. Returns (status, tier, error)."""
    if needs_skip(code):
        return "skip", "", ""

    expr_code = wrap_expressions(code)
    defines_procedures = bool(SUBDEF.search(code))
    tiers = [("as-is", code), ("as-is + common Dims", inject_common_dims(code))]
    if not defines_procedures:
        tiers += [
            ("wrapped in Sub", wrap_sub(code)),
            ("Sub + common Dims", wrap_sub(inject_common_dims(code))),
        ]
    tiers.append(
        ("expression wrap", wrap_sub(inject_common_dims(expr_code))
         if not defines_procedures else inject_common_dims(expr_code))
    )
    last_err = ""
    for label, candidate in tiers:
        ok, err = compile_check(candidate, tmpdir, tag)
        if ok:
            return "pass", label, ""
        last_err = err
    return "fail", "", last_err


def main():
    parser = argparse.ArgumentParser(description="Compile-check FreeBASIC doc examples")
    parser.add_argument("files", nargs="*", help="Markdown files (default: all in skill root)")
    parser.add_argument("--json", action="store_true", help="JSON output")
    parser.add_argument("--keep", action="store_true", help="Keep temp files")
    parser.add_argument("-v", "--verbose", action="store_true", help="Show per-block status")
    args = parser.parse_args()

    base_dir = Path(__file__).resolve().parent.parent
    if args.files:
        md_files = [Path(f) for f in args.files]
    else:
        md_files = sorted(p for p in base_dir.glob("*.md") if p.name != "SKILL.md")

    results = []
    tmpdir = Path(tempfile.mkdtemp(prefix="fb-validate-"))
    try:
        for md_file in md_files:
            for idx, (line, code) in enumerate(find_blocks(md_file)):
                status, tier, err = validate_block(code, tmpdir, f"{md_file.stem}_{idx}")
                results.append({
                    "file": md_file.name, "line": line, "status": status,
                    "tier": tier, "error": err,
                })
                if args.verbose and not args.json:
                    note = f"  [{tier}]" if tier else (f"  {err}" if err else "")
                    print(f"{md_file.name}:{line:<5} {status.upper():<5}{note}")
    finally:
        if args.keep:
            print(f"temp files kept in {tmpdir}", file=sys.stderr)
        else:
            import shutil
            shutil.rmtree(tmpdir, ignore_errors=True)

    if args.json:
        print(json.dumps(results, indent=2, ensure_ascii=False))
        return

    passed = sum(r["status"] == "pass" for r in results)
    failed = [r for r in results if r["status"] == "fail"]
    skipped = sum(r["status"] == "skip" for r in results)
    print(f"\n{len(results)} blocks: {passed} pass, {len(failed)} fail, {skipped} skipped")
    for r in failed:
        print(f"  FAIL {r['file']}:{r['line']}  {r['error']}")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
