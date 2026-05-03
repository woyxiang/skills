#!/usr/bin/env python3
"""Validate skill directory structure.

Checks:
- SKILL.md exists and has required frontmatter
- All *.md files in skills/<lang>/ are registered in SKILL.md routing table
- agents/ contains only *.md files
- scripts/ contains only *.py files
- examples/ contains files that can compile (stub: returns OK)

Usage:
    python3 validate-structure.py <skill> <skill-dir>
    python3 validate-structure.py typst skills/typst
"""

import argparse
import os
import re
import sys


def read_file(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def extract_frontmatter(content):
    m = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
    if not m:
        return {}
    result = {}
    for line in m.group(1).split("\n"):
        if ":" in line:
            key, val = line.split(":", 1)
            result[key.strip()] = val.strip().strip("'\"")
    return result


def extract_routed_files(skill_md_content):
    """Extract file references from SKILL.md routing tables."""
    files = set()
    # Match lines like [foo.md](foo.md) or [bar](bar.md) — extract filenames
    pattern = r"\[([^\]]+)\]\(([^)]+\.md)\)"
    for _, filename in re.findall(pattern, skill_md_content):
        files.add(filename)
    # Also match bare markdown links [filename.md]
    pattern2 = r"\b([a-zA-Z0-9_-]+\.md)\b"
    files.update(re.findall(pattern2, skill_md_content))
    return files


def validate_skill(lang_name, skills_dir):
    lang_dir = os.path.join(skills_dir, lang_name)
    skill_md = os.path.join(lang_dir, "SKILL.md")

    errors = []
    warnings = []

    # 1. SKILL.md must exist
    if not os.path.isfile(skill_md):
        errors.append(f"SKILL.md not found at {skill_md}")
        return errors, warnings

    content = read_file(skill_md)
    fm = extract_frontmatter(content)

    # 2. Required frontmatter
    for field in ["name", "description"]:
        if field not in fm:
            errors.append(f"SKILL.md missing frontmatter field: {field}")

    # 3. Extract all registered files
    registered = extract_routed_files(content)

    # 4. Scan skill directory for actual .md files (exclude agents/ — registered via docs, not routing table)
    actual_md = []
    for root, dirs, files in os.walk(lang_dir):
        # Skip hidden dirs and agents/ (agents are referenced from docs, not routing tables)
        dirs[:] = [d for d in dirs if not d.startswith(".") and d != "agents"]
        for f in files:
            if f.endswith(".md"):
                rel = os.path.relpath(os.path.join(root, f), lang_dir)
                rel = rel.replace("\\", "/")  # normalize Windows paths
                actual_md.append(rel)

    # 5. Unregistered files (excluding SKILL.md itself)
    unregistered = [f for f in actual_md if f != "SKILL.md" and f not in registered]

    # 6. agents/ must only contain .md
    agents_dir = os.path.join(lang_dir, "agents")
    if os.path.isdir(agents_dir):
        for f in os.listdir(agents_dir):
            if not f.endswith(".md"):
                errors.append(f"agents/{f} is not a .md file")

    # 7. scripts/ must only contain .py
    scripts_dir = os.path.join(lang_dir, "scripts")
    if os.path.isdir(scripts_dir):
        for f in os.listdir(scripts_dir):
            if not f.endswith(".py"):
                warnings.append(f"scripts/{f} is not a .py file")

    if unregistered:
        errors.append(
            f"Unregistered docs: {', '.join(unregistered)}. Add them to SKILL.md routing table."
        )

    return errors, warnings


def main():
    parser = argparse.ArgumentParser(description="Validate skill directory structure")
    parser.add_argument("name", help="skill name (e.g. typst, python)")
    parser.add_argument("skill_dir", help="Path to skills directory")
    args = parser.parse_args()

    errors, warnings = validate_skill(args.name, args.skill_dir)

    for w in warnings:
        print(f"WARNING: {w}", file=sys.stderr)
    for e in errors:
        print(f"ERROR: {e}", file=sys.stderr)

    if errors:
        print("Validation FAILED")
        sys.exit(1)
    elif warnings:
        print("Validation PASSED with warnings")
    else:
        print("Validation PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
