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


def test_exact_lookup():
    """Exact lookup should find keywords."""
    api_data = _load_api_data()
    result = search_api.exact_lookup("(Print | ?)", api_data)
    assert result is not None, "Exact lookup failed for '(Print | ?)'"
    assert result['category'] == 'console'
    print("  Exact lookup for '(Print | ?)'... OK")


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
    test_exact_lookup()

    print("\nAll API search tests passed!")