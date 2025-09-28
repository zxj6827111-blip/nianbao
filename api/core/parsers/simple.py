from __future__ import annotations

import csv
import io
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List

SECTION_MAP = {
    "一": "sec_1",
    "二": "sec_2",
    "三": "sec_3",
    "四": "sec_4",
    "五": "sec_5",
    "六": "sec_6",
}


@dataclass
class ParsedDocument:
    sections: Dict[str, str]
    tables: Dict[str, Dict[str, str]]


SECTION_HEADER_RE = re.compile(r"^([一二三四五六])、")


def parse_text_document(text: str) -> ParsedDocument:
    current_sec = None
    buffer: List[str] = []
    sections: Dict[str, str] = {}
    tables: Dict[str, Dict[str, str]] = {"sec_2": {}, "sec_3": {}, "sec_4": {}}
    lines = text.strip().splitlines()
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        header_match = SECTION_HEADER_RE.match(line)
        if header_match:
            if current_sec and buffer:
                sections[current_sec] = "\n".join(buffer).strip()
                buffer = []
            current_sec = SECTION_MAP[header_match.group(1)]
            buffer.append(line[len(header_match.group(0)) :].strip() or line)
            i += 1
            continue
        if "," in line and current_sec in {"sec_2", "sec_3", "sec_4"}:
            reader = csv.reader([line])
            row = next(reader)
            if len(row) == 2:
                key, value = row
                tables[current_sec][key.strip()] = value.strip()
            i += 1
            continue
        buffer.append(line)
        i += 1
    if current_sec and buffer:
        sections[current_sec] = "\n".join(buffer).strip()
    return ParsedDocument(sections=sections, tables=tables)


def load_sample(name: str) -> ParsedDocument:
    sample_path = Path(__file__).resolve().parents[2] / "data" / "samples" / name
    return parse_text_document(sample_path.read_text(encoding="utf-8"))
