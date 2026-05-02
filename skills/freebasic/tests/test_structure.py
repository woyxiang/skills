#!/usr/bin/env python3
"""
Test structure validation for FreeBASIC skill.
Validates SKILL.md and all .md files exist and are properly linked.
"""

import os
import json
from pathlib import Path

skill_dir = Path(__file__).parent.parent  # skills/freebasic


def test_skill_md_exists():
    """SKILL.md must exist with valid frontmatter."""
    skill_path = skill_dir / "SKILL.md"
    assert skill_path.exists(), "SKILL.md not found"

    content = skill_path.read_text(encoding='utf-8')
    assert content.startswith("---"), "SKILL.md missing frontmatter"
    assert "name: freebasic" in content, "SKILL.md missing name field"


def test_all_doc_files_exist():
    """All documentation .md files must exist."""
    expected_docs = [
        "SKILL.md",
        "basics.md",
        "types.md",
        "operators.md",
        "control-flow.md",
        "procedures.md",
        "arrays.md",
        "strings.md",
        "file-io.md",
        "graphics.md",
        "preprocessor.md",
        "error-handling.md",
        "user-defined-types.md",
        "pointers.md",
        "threading.md",
        "math.md",
        "date-time.md",
        "compiler.md",
    ]

    for doc in expected_docs:
        path = skill_dir / doc
        assert path.exists(), f"Missing documentation: {doc}"


def test_api_json_exists():
    """api.json must exist with keyword entries."""
    api_path = skill_dir / "data" / "api.json"
    assert api_path.exists(), "api.json not found"

    with open(api_path, encoding='utf-8') as f:
        data = json.load(f)

    assert "keywords" in data, "api.json missing keywords array"
    assert data["count"] > 500, f"Expected ~626 keywords, got {data['count']}"


def test_api_bm25_exists():
    """api-bm25.json must exist with index."""
    index_path = skill_dir / "data" / "api-bm25.json"
    assert index_path.exists(), "api-bm25.json not found"

    with open(index_path, encoding='utf-8') as f:
        index = json.load(f)

    assert "inverted" in index, "BM25 index missing inverted"
    assert index["document_count"] > 500, "Too few documents in index"


def test_scripts_exist():
    """All scripts must exist."""
    scripts_dir = skill_dir / "scripts"
    expected_scripts = [
        "extract-api.py",
        "build-index.py",
        "search-api.py",
    ]

    for script in expected_scripts:
        path = scripts_dir / script
        assert path.exists(), f"Missing script: {script}"


def test_cross_references():
    """All .md files should have cross-references to related docs."""
    for md_file in skill_dir.glob("*.md"):
        if md_file.name == "SKILL.md":
            continue
        content = md_file.read_text(encoding='utf-8')
        assert "See Also" in content or "see also" in content or ".md" in content, \
            f"{md_file.name} missing cross-references"


if __name__ == "__main__":
    print("Running structure tests...")

    test_skill_md_exists()
    print("  SKILL.md exists with frontmatter... OK")

    test_all_doc_files_exist()
    print("  All doc files exist... OK")

    test_api_json_exists()
    print("  api.json exists with keywords... OK")

    test_api_bm25_exists()
    print("  api-bm25.json exists with index... OK")

    test_scripts_exist()
    print("  All scripts exist... OK")

    test_cross_references()
    print("  Cross-references present... OK")

    print("\nAll structure tests passed!")