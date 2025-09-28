from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Tuple

DATA_DIR = Path(__file__).resolve().parents[2] / "data"

with (DATA_DIR / "region_domain_map.json").open("r", encoding="utf-8") as f:
    REGION_DOMAIN_MAP = json.load(f)


def _ratio(a: str, b: str) -> float:
    if not a or not b:
        return 0.0
    set_a = set(a)
    set_b = set(b)
    if not set_a or not set_b:
        return 0.0
    return len(set_a & set_b) / len(set_a | set_b)


@dataclass
class AutoDetectResult:
    region_code: Optional[str]
    region_name: Optional[str]
    org_name: Optional[str]
    year: Optional[int]
    confidence: float
    matched_org_id: Optional[int] = None


def detect_region_from_url(url: str) -> Tuple[Optional[str], float]:
    for domain, code in REGION_DOMAIN_MAP.items():
        if domain in url:
            return code, 0.4
    return None, 0.0


def detect_year(text: str) -> Optional[int]:
    match = re.search(r"(20\d{2})年", text)
    return int(match.group(1)) if match else None


def load_alias(region_code: str) -> list[str]:
    alias_path = DATA_DIR / "aliases" / f"{region_code}.txt"
    if not alias_path.exists():
        return []
    content = alias_path.read_text(encoding="utf-8")
    return [item.strip() for item in content.split("|") if item.strip()]


def detect_region_by_alias(text: str) -> Tuple[Optional[str], float]:
    for domain, code in REGION_DOMAIN_MAP.items():
        aliases = load_alias(code)
        for alias in aliases:
            if alias in text:
                return code, 0.3
    return None, 0.0


def detect_org_name(text: str, region_code: Optional[str]) -> Tuple[Optional[str], float]:
    if not region_code:
        return None, 0.0
    aliases = load_alias(region_code)
    for alias in aliases:
        if alias and alias in text:
            return alias, 0.2
    best_score = 0.0
    best_alias: Optional[str] = None
    for alias in aliases:
        score = _ratio(alias, text)
        if score > best_score:
            best_score = score
            best_alias = alias
    if best_score >= 0.3:
        return best_alias, 0.1
    return None, 0.0


def auto_detect(text: str, url: str = "", title: str = "") -> AutoDetectResult:
    region_by_url, score_url = detect_region_from_url(url)
    region_by_alias, score_alias = detect_region_by_alias(text + title)
    region_code = region_by_url or region_by_alias
    region_score = score_url + (score_alias if region_by_alias == region_code else 0)

    org_name, org_score = detect_org_name(text + title, region_code)
    year = detect_year(title) or detect_year(text)

    confidence = min(1.0, region_score + org_score + (0.3 if year else 0))
    return AutoDetectResult(
        region_code=region_code,
        region_name=None,
        org_name=org_name,
        year=year,
        confidence=confidence,
    )
