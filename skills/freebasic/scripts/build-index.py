#!/usr/bin/env python3
"""
Build BM25 search index from api.json.
Creates api-bm25.json with inverted index for full-text search.
"""

import json
import math
import re
from pathlib import Path
from collections import defaultdict

# BM25 parameters
K1 = 1.5
B = 0.75

# Field weights for scoring
WEIGHTS = {
    'name': 3.0,
    'syntax': 2.0,
    'description': 1.0,
    'category': 1.5,
    'parameters': 1.0,
}


def tokenize(text: str) -> list:
    """Tokenize text into lowercase words."""
    if not text:
        return []
    text = text.lower()
    # Split on non-alphanumeric sequences
    tokens = re.findall(r'[a-z0-9]+', text)
    return tokens


def build_index(api_data: dict) -> dict:
    """Build BM25 inverted index from api.json."""
    keywords = api_data['keywords']
    total_docs = len(keywords)
    avg_length = 0

    # Collect all field values for tokenization
    doc_fields = []
    for kw in keywords:
        fields = {}
        for field in ['name', 'syntax', 'description', 'category']:
            fields[field] = tokenize(kw.get(field, '') or '')
        fields['parameters'] = tokenize(
            ' '.join(p.get('name', '') + ' ' + p.get('description', '') for p in kw.get('parameters', []))
        )
        doc_fields.append(fields)
        avg_length += sum(len(v) for v in fields.values())

    avg_length = avg_length / total_docs if total_docs > 0 else 1

    # Build inverted index
    inverted = defaultdict(lambda: {'df': 0, 'postings': []})

    for doc_id, fields in enumerate(doc_fields):
        seen_terms = set()
        for field_name, tokens in fields.items():
            if field_name not in WEIGHTS:
                continue
            weight = WEIGHTS[field_name]

            for term in tokens:
                if term in seen_terms:
                    continue
                seen_terms.add(term)

                inverted[term]['df'] += 1
                inverted[term]['postings'].append({
                    'doc_id': doc_id,
                    'field': field_name,
                    'tf': 1,  # Simplified - count occurrences
                    'weight': weight
                })

    # Build document length info
    doc_lengths = []
    for fields in doc_fields:
        doc_len = 0
        for field_name, tokens in fields.items():
            if field_name in WEIGHTS:
                doc_len += len(tokens) * WEIGHTS[field_name]
        doc_lengths.append(doc_len)

    return {
        'version': '1.0',
        'document_count': total_docs,
        'average_length': avg_length,
        'k1': K1,
        'b': B,
        'weights': WEIGHTS,
        'inverted': dict(inverted),
        'doc_lengths': doc_lengths,
        'doc_names': [kw['name'] for kw in keywords],
    }


def main():
    base_dir = Path(__file__).parent.parent  # skills/freebasic
    api_file = base_dir / "data" / "api.json"
    output_file = base_dir / "data" / "api-bm25.json"

    print(f"Loading {api_file}...")
    with open(api_file, encoding='utf-8') as f:
        api_data = json.load(f)

    print(f"Building BM25 index for {api_data['count']} documents...")
    index = build_index(api_data)

    print(f"Inverted index has {len(index['inverted'])} unique terms")

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(index, f, indent=2, ensure_ascii=False)

    print(f"Written to {output_file}")


if __name__ == "__main__":
    main()