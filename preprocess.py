import re
from typing import List


def clean_excess_whitespace(text: str) -> str:
    text = re.sub(r"[\r\t\f\v]", " ", text)
    text = re.sub(r" {2,}", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def fix_broken_line_breaks(text: str) -> str:
    text = re.sub(r"(\b[a-zA-Z]+)-\n([a-zA-Z]+\b)", r"\1\2", text)
    
    text = re.sub(r"([a-z0-9,])\n([a-z])", r"\1 \2", text)
    return text


def remove_formatting_artifacts(text: str) -> str:
    text = re.sub(r"[\u2022\u2023\u25b6\u25c0\u25ba\u25c4\u25a0\u25a1\u25cf\u25cb\u2013\u2014]", "-", text)
    
    text = "".join(ch for ch in text if ch == "\n" or ord(ch) >= 32)
    return text


def remove_repeated_headers_footers(lines: List[str]) -> List[str]:
    if len(lines) <= 5:
        return lines

    line_counts = {}
    for line in lines:
        cleaned_line = line.strip()
        if len(cleaned_line) > 3 and not re.match(r"^[-=_*]+$", cleaned_line):
            line_counts[cleaned_line] = line_counts.get(cleaned_line, 0) + 1

    filtered_lines = []
    for line in lines:
        cleaned_line = line.strip()
        if re.search(r"^page\s+\d+(\s+of\s+\d+)?$", cleaned_line, re.IGNORECASE):
            continue
        if line_counts.get(cleaned_line, 0) >= 3:
            continue
        filtered_lines.append(line)

    return filtered_lines


def remove_duplicate_adjacent_lines(lines: List[str]) -> List[str]:
    result = []
    prev_line = None
    for line in lines:
        if line != prev_line or not line.strip():
            result.append(line)
            if line.strip():
                prev_line = line
    return result


def preprocess_resume_text(raw_text: str) -> str:
    if not raw_text:
        return ""

    text = remove_formatting_artifacts(raw_text)

    text = fix_broken_line_breaks(text)

    lines = text.split("\n")
    lines = remove_repeated_headers_footers(lines)
    lines = remove_duplicate_adjacent_lines(lines)

    rejoined_text = "\n".join(lines)

    clean_text = clean_excess_whitespace(rejoined_text)

    return clean_text
