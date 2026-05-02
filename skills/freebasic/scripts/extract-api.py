#!/usr/bin/env python3
"""
Extract API entries from FreeBASIC manual HTML files.
Parses KeyPg*.html files to generate api.json with keyword metadata.
"""

import json
import re
import os
from pathlib import Path
from typing import Optional
from html import unescape

try:
    from bs4 import BeautifulSoup
except ImportError:
    print("Error: beautifulsoup4 is required. Install with: pip install beautifulsoup4")
    exit(1)


def extract_title(soup) -> str:
    """Extract keyword name from <div id="fb_tab_l"> or <title>."""
    title_elem = soup.find('div', id='fb_tab_l')
    if title_elem:
        return title_elem.get_text(strip=True)
    if soup.title:
        title_text = soup.title.string or ""
        # Handle titles like "(Print | ?)" - take first name
        if '|' in title_text:
            title_text = title_text.split('|')[0].strip('() ')
        return title_text.strip()
    return ""


def extract_description(body_div) -> str:
    """Extract one-line description from first text in body."""
    text = body_div.get_text(separator=' ', strip=True)
    # First sentence or up to 100 chars
    text = text[:200].split('\n')[0].strip()
    return text


def extract_sections(soup) -> dict:
    """Extract all sections by <div class="fb_sect_title">.</div>"""
    sections = {}
    for sect in soup.find_all('div', class_='fb_sect_title'):
        sect_name = sect.get_text(strip=True)
        cont = sect.find_next_sibling('div', class_='fb_sect_cont')
        if cont:
            # Clean HTML tags, keep text
            text = cont.get_text(separator=' ', strip=True)
            sections[sect_name] = text
    return sections


def parse_parameters(params_text: str) -> list:
    """Parse parameter list from Parameters section text."""
    params = []
    # Pattern: parameter name (italic) followed by description
    # The HTML has <tt><i>paramname</i></tt> then <div class="fb_indent">description
    # For now, extract simple pattern
    return params


def extract_parameters_html(soup) -> list:
    """Extract parameters from HTML structure."""
    params = []
    params_div = None
    for sect in soup.find_all('div', class_='fb_sect_title'):
        if sect.get_text(strip=True) == 'Parameters':
            params_div = sect.find_next_sibling('div', class_='fb_sect_cont')
            break

    if not params_div:
        return params

    # Find all <tt><i>...</i></tt> patterns (parameter names)
    for tt in params_div.find_all('tt'):
        i_elem = tt.find('i')
        if i_elem:
            param_name = i_elem.get_text(strip=True)
            # Get following sibling text for description
            desc = ""
            sibling = tt.find_next_sibling()
            if sibling and sibling.get_text(strip=True):
                desc = sibling.get_text(strip=True)
            else:
                # Check for fb_indent div after this tt
                indent = tt.find_parent('div', class_='fb_indent')
                if indent:
                    desc = indent.get_text(strip=True)

            if param_name and param_name != 'i':
                params.append({
                    "name": param_name,
                    "description": desc[:200]
                })

    return params


def extract_examples(soup) -> list:
    """Extract code examples from <div class="freebasic"> blocks."""
    examples = []
    for div in soup.find_all('div', class_='freebasic'):
        # Get raw text but clean up the highlighting
        code_lines = []
        for span in div.find_all(['span', 'tt', 'br']):
            if span.name == 'br':
                code_lines.append('\n')
            elif span.name == 'span':
                code_lines.append(span.get_text())
            elif span.name == 'tt':
                code_lines.append(span.get_text())
            else:
                code_lines.append(str(span))
        code = ''.join(code_lines)
        # Clean up HTML entities
        code = code.replace('&nbsp;', ' ')
        code = unescape(code)
        # Remove excess whitespace
        code = re.sub(r'\n+', '\n', code).strip()
        if code:
            examples.append(code)
    return examples


def extract_see_also(soup) -> list:
    """Extract 'See also' keyword links."""
    see_also = []
    for sect in soup.find_all('div', class_='fb_sect_title'):
        if sect.get_text(strip=True) == 'See also':
            cont = sect.find_next_sibling('div', class_='fb_sect_cont')
            if cont:
                for a in cont.find_all('a', href=re.compile(r'^KeyPg')):
                    see_also.append(a.get_text(strip=True))
            break
    return see_also


def extract_syntax(soup) -> str:
    """Extract syntax from Syntax section."""
    for sect in soup.find_all('div', class_='fb_sect_title'):
        if sect.get_text(strip=True) == 'Syntax':
            cont = sect.find_next_sibling('div', class_='fb_sect_cont')
            if cont:
                # Get text content, clean up
                syntax = cont.get_text(separator=' ', strip=True)
                syntax = unescape(syntax)
                return syntax[:300]  # Truncate long syntax
    return ""


def extract_dialect_differences(soup) -> Optional[str]:
    """Extract dialect differences."""
    for sect in soup.find_all('div', class_='fb_sect_title'):
        if 'Dialect Differences' in sect.get_text(strip=True):
            cont = sect.find_next_sibling('div', class_='fb_sect_cont')
            if cont:
                return cont.get_text(strip=True)[:500]
    return None


def extract_qb_differences(soup) -> Optional[str]:
    """Extract QB differences."""
    for sect in soup.find_all('div', class_='fb_sect_title'):
        if 'Differences from QB' in sect.get_text(strip=True):
            cont = sect.find_next_sibling('div', class_='fb_sect_cont')
            if cont:
                return cont.get_text(strip=True)[:500]
    return None


def extract_return_value(soup) -> Optional[str]:
    """Extract return value description."""
    for sect in soup.find_all('div', class_='fb_sect_title'):
        if 'Return Value' in sect.get_text(strip=True):
            cont = sect.find_next_sibling('div', class_='fb_sect_cont')
            if cont:
                return cont.get_text(strip=True)[:300]
    return None


def extract_category_from_filename(filename: str) -> str:
    """Derive category from filename."""
    name = filename.replace('KeyPg', '').replace('.html', '').lower()
    # Common categories
    categories = {
        'print': 'console', 'input': 'console', 'cls': 'console',
        'dim': 'types', 'var': 'types', 'type': 'user-defined-types',
        'function': 'procedures', 'sub': 'procedures', 'return': 'procedures',
        'for': 'control-flow', 'while': 'control-flow', 'do': 'control-flow',
        'if': 'control-flow', 'select': 'control-flow',
        'open': 'file-io', 'close': 'file-io', 'get': 'file-io', 'put': 'file-io',
        'string': 'strings', 'len': 'strings', 'mid': 'strings',
        'screen': 'graphics', 'circle': 'graphics', 'line': 'graphics',
        'arraylen': 'arrays', 'lbound': 'arrays', 'ubound': 'arrays',
        'mkdir': 'file-io', 'chdir': 'file-io',
        'threadcreate': 'threading', 'mutexcreate': 'threading',
    }
    return categories.get(name, 'general')


def parse_keyword_file(html_path: Path) -> Optional[dict]:
    """Parse a single KeyPg*.html file."""
    try:
        with open(html_path, encoding='utf-8') as f:
            soup = BeautifulSoup(f.read(), 'html.parser')

        body = soup.find('div', id='fb_pg_body')
        if not body:
            return None

        name = extract_title(soup)
        if not name:
            return None

        entry = {
            "name": name,
            "aliases": [],
            "category": extract_category_from_filename(html_path.name),
            "syntax": extract_syntax(soup),
            "description": extract_description(body),
            "parameters": extract_parameters_html(soup),
            "return": extract_return_value(soup),
            "examples": extract_examples(soup),
            "dialect_differences": extract_dialect_differences(soup),
            "qb_differences": extract_qb_differences(soup),
            "see_also": extract_see_also(soup),
            "file": html_path.name
        }

        return entry
    except Exception as e:
        print(f"Error parsing {html_path}: {e}")
        return None


def main():
    base_dir = Path(__file__).parent.parent  # skills/freebasic
    manual_dir = base_dir.parent / "references" / "FB-manual"  # ../references/FB-manual
    output_file = base_dir / "data" / "api.json"

    print(f"Scanning {manual_dir}...")

    keywords = []
    keypg_files = sorted(manual_dir.glob("KeyPg*.html"))
    print(f"Found {len(keypg_files)} keyword files")

    for i, html_file in enumerate(keypg_files):
        if i % 50 == 0:
            print(f"Processing {i}/{len(keypg_files)}...")

        entry = parse_keyword_file(html_file)
        if entry:
            keywords.append(entry)

    print(f"\nExtracted {len(keywords)} keyword entries")

    # Ensure output directory exists
    output_file.parent.mkdir(parents=True, exist_ok=True)

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump({"keywords": keywords, "count": len(keywords)}, f, indent=2, ensure_ascii=False)

    print(f"Written to {output_file}")


if __name__ == "__main__":
    main()