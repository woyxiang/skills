#!/usr/bin/env python3
"""
Test API search functionality.
"""

import json
import importlib.util
from pathlib import Path

skill_dir = Path(__file__).parent.parent  # skills/freebasic

# Load search_api module manually (since it has hyphenated name)
scripts_dir = skill_dir / "scripts"
spec = importlib.util.spec_from_file_location("search_api", scripts_dir / "search-api.py")
search_api = importlib.util.module_from_spec(spec)
spec.loader.exec_module(search_api)

# Shared paths
api_json_file = skill_dir / "data" / "api.json"
api_bm25_file = skill_dir / "data" / "api-bm25.json"


def _load_index():
    with open(api_bm25_file) as f:
        return json.load(f)


def _load_api_data():
    with open(api_json_file) as f:
        return json.load(f)


def test_search_returns_results():
    """Search should return matching results."""
    index = _load_index()
    results = search_api.search("print screen", index, top=5)
    assert len(results) > 0, "Search returned no results"
    print(f"  Search 'print screen' returned {len(results)} results... OK")


def test_search_relevance():
    """Search results should be relevant to query."""
    index = _load_index()
    api_data = _load_api_data()

    results = search_api.search("array dimension", index, top=3)
    assert len(results) > 0, "Search returned no results"

    # Check that top result mentions array
    top_name = api_data['keywords'][results[0][0]]['name']
    print(f"  Top result for 'array dimension': {top_name}")

    # Should include LBound, UBound, or similar
    names_lower = [api_data['keywords'][r[0]]['name'].lower() for r in results]
    assert any('bound' in n or 'array' in n for n in names_lower), \
        f"Expected array-related results, got: {names_lower}"
    print("  Results are relevant... OK")


def test_name_lookup():
    """Lookup should find keywords by name and alias, without confusion."""
    api_data = _load_api_data()

    entry, _ = search_api.lookup("Print", api_data)
    assert entry is not None, "Lookup failed for 'Print'"
    assert entry['name'] == 'Print', f"Expected Print, got {entry['name']}"

    entry, _ = search_api.lookup("?", api_data)
    assert entry is not None and entry['name'] == 'Print', "Alias '?' should map to Print"

    entry, _ = search_api.lookup("#print", api_data)
    assert entry is not None and entry['name'] == '#print', "'#print' must not resolve to 'Print'"

    entry, candidates = search_api.lookup("Mid", api_data)
    assert entry is not None or len(candidates) >= 2, "Ambiguous 'Mid' should list candidates"
    print("  Name/alias lookup... OK")


def test_search_prefers_exact_name():
    """A query naming a keyword should rank that keyword first."""
    index = _load_index()
    api_data = _load_api_data()
    results = search_api.search("print to screen", index, top=3)
    top_name = api_data['keywords'][results[0][0]]['name']
    assert top_name == 'Print', f"Expected Print first, got {top_name}"
    print("  Search prefers exact name... OK")


def test_data_quality():
    """api.json must be clean: no Syntax bleed into descriptions, real example code."""
    api_data = _load_api_data()
    assert api_data.get('version'), "api.json missing manual version"
    for kw in api_data['keywords']:
        desc = kw.get('description') or ''
        assert ' Declare Function ' not in desc and ' Declare Sub ' not in desc,             f"{kw['name']}: description polluted with syntax"
        for ex in kw.get('examples', []):
            assert 'Dimn' not in ex and 'PrintAbs' not in ex,                 f"{kw['name']}: example lost whitespace"
    params = [p for kw in api_data['keywords'] for p in kw.get('parameters', [])]
    with_desc = [p for p in params if p.get('description')]
    assert len(with_desc) > 0.9 * len(params), "Too many parameters without descriptions"
    print(f"  Data quality ({len(params)} params, {len(with_desc)} described)... OK")


def test_tokenize():
    """Tokenization should work correctly."""
    tokens = search_api.tokenize("print to screen")
    assert 'print' in tokens
    assert 'screen' in tokens
    assert len(tokens) == 3
    print("  Tokenization... OK")


def test_categories():
    """Categories should be present in api.json."""
    api_data = _load_api_data()
    cats = set()
    for kw in api_data['keywords']:
        cats.add(kw.get('category', 'unknown'))

    print(f"  Found {len(cats)} categories: {sorted(cats)}")
    assert len(cats) > 5, "Expected more categories"
    print("  Categories present... OK")


if __name__ == "__main__":
    print("Running API search tests...\n")

    test_tokenize()
    test_categories()
    test_search_returns_results()
    test_search_relevance()
    test_name_lookup()
    test_search_prefers_exact_name()
    test_data_quality()

    print("\nAll API search tests passed!")