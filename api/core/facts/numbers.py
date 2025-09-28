from __future__ import annotations

import re
from dataclasses import dataclass
from decimal import Decimal
from typing import Dict, Iterable, List, Sequence

from ..clean.units import normalize_number

NUMBER_SENT_RE = re.compile(r"(?P<label>[\u4e00-\u9fff]{2,10})(?P<num>\d+(?:\.\d+)?)")


@dataclass
class NumericFact:
    key: str
    value: Decimal
    unit: str
    context: str


def extract_facts(section_key: str, sentences: Sequence[str]) -> List[NumericFact]:
    facts: List[NumericFact] = []
    for idx, sentence in enumerate(sentences):
        matches = NUMBER_SENT_RE.finditer(sentence)
        for match in matches:
            label = match.group("label")
            value_unit = normalize_number(match.group("num"))
            if not value_unit:
                continue
            value, unit = value_unit
            facts.append(NumericFact(key=f"{section_key}/{label}", value=value, unit=unit, context=sentence))
    return facts


def align_facts(facts_left: Iterable[NumericFact], facts_right: Iterable[NumericFact]) -> Dict[str, Dict[str, NumericFact | None]]:
    aligned: Dict[str, Dict[str, NumericFact | None]] = {}
    left_index = {fact.key: fact for fact in facts_left}
    right_index = {fact.key: fact for fact in facts_right}
    keys = set(left_index) | set(right_index)
    for key in sorted(keys):
        aligned[key] = {
            "left": left_index.get(key),
            "right": right_index.get(key),
        }
    return aligned
