"""
Resume Preprocessing module.
Cleans raw text extracted from PDF resumes by handling excess whitespace,
broken line breaks, repeated headers/footers, formatting artifacts, while preserving candidate info.
"""

import re
from typing import List


def clean_excess_whitespace(text: str) -> str:
    """Replaces multiple spaces/tabs with single space, and standardizes newlines."""
    # Replace non-breaking spaces or weird spaces
    text = re.sub(r"[\r\t\f\v]", " ", text)
    # Replace multiple horizontal spaces with a single space
    text = re.sub(r" {2,}", " ", text)
    # Standardize multiple consecutive empty lines to maximum 2 newlines
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def fix_broken_line_breaks(text: str) -> str:
    """
    Fixes hyphenated word breaks split across lines (e.g. 'develop-\nment' -> 'development')
    and rejoins broken sentences where line break occurs mid-sentence.
    """
    # Fix hyphenated line breaks: word-\nword -> wordword
    text = re.sub(r"(\b[a-zA-Z]+)-\n([a-zA-Z]+\b)", r"\1\2", text)
    
    # Fix lowercase to lowercase line break: word\nword -> word word
    # preserve line breaks after punctuation or headers
    text = re.sub(r"([a-z0-9,])\n([a-z])", r"\1 \2", text)
    return text


def remove_formatting_artifacts(text: str) -> str:
    """Removes common PDF extraction artifacts, bullet characters, unprintable chars."""
    # Replace bullet points or weird symbols with standard dash
    text = re.sub(r"[\u2022\u2023\u25b6\u25c0\u25ba\u25c4\u25a0\u25a1\u25cf\u25cb\u2013\u2014]", "-", text)
    # Remove control characters except newlines
    text = "".join(ch for ch in text if ch == "\n" or ord(ch) >= 32)
    return text


def remove_repeated_headers_footers(lines: List[str]) -> List[str]:
    """
    Identifies and removes lines that repeat frequently (likely page numbers, headers, footers).
    """
    if len(lines) <= 5:
        return lines

    line_counts = {}
    for line in lines:
        cleaned_line = line.strip()
        if len(cleaned_line) > 3 and not re.match(r"^[-=_*]+$", cleaned_line):
            line_counts[cleaned_line] = line_counts.get(cleaned_line, 0) + 1

    # Lines occurring more than 3 times or matching Page X of Y pattern are candidate header/footers
    filtered_lines = []
    for line in lines:
        cleaned_line = line.strip()
        # Page X or Page X of Y check
        if re.search(r"^page\s+\d+(\s+of\s+\d+)?$", cleaned_line, re.IGNORECASE):
            continue
        if line_counts.get(cleaned_line, 0) >= 3:
            continue
        filtered_lines.append(line)

    return filtered_lines


def remove_duplicate_adjacent_lines(lines: List[str]) -> List[str]:
    """Removes exact adjacent duplicate lines."""
    result = []
    prev_line = None
    for line in lines:
        if line != prev_line or not line.strip():
            result.append(line)
            if line.strip():
                prev_line = line
    return result


def preprocess_resume_text(raw_text: str) -> str:
    """
    Full preprocessing pipeline for raw resume text.
    Preserves all meaningful professional and candidate content.
    """
    if not raw_text:
        return ""

    # Step 1: Remove unprintable formatting artifacts
    text = remove_formatting_artifacts(raw_text)

    # Step 2: Fix broken hyphenated line breaks
    text = fix_broken_line_breaks(text)

    # Step 3: Split into lines for header/footer filtering
    lines = text.split("\n")
    lines = remove_repeated_headers_footers(lines)
    lines = remove_duplicate_adjacent_lines(lines)

    # Rejoin lines
    rejoined_text = "\n".join(lines)

    # Step 4: Clean excess whitespace
    clean_text = clean_excess_whitespace(rejoined_text)

    return clean_text
