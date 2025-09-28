from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List, Sequence

TEMPLATE_PATH = Path(__file__).resolve().parents[2] / "templates" / "boilerplate.txt"
BOILERPLATE = {
    line.strip()
    for line in TEMPLATE_PATH.read_text(encoding="utf-8").splitlines()
    if line.strip()
}
SENT_SPLIT_RE = re.compile(r"(?<=[。！？\.!?])")


def _simple_similarity(a: str, b: str) -> float:
    if not a or not b:
        return 0.0
    set_a = set(a)
    set_b = set(b)
    if not set_a or not set_b:
        return 0.0
    return len(set_a & set_b) / len(set_a | set_b)


@dataclass
class SentencePair:
    left: str
    right: str
    score: float
    matched: bool


def clean_sentence(sentence: str) -> str:
    cleaned = sentence.strip()
    cleaned = re.sub(r"[\s\u3000]+", " ", cleaned)
    return cleaned


def is_boilerplate(sentence: str) -> bool:
    normalized = sentence.strip().replace(" ", "")
    return any(normalized.startswith(bp.replace(" ", "")) for bp in BOILERPLATE)


def split_sentences(text: str) -> List[str]:
    normalized_text = text.replace('\n', '。')
    segments = [clean_sentence(seg) for seg in SENT_SPLIT_RE.split(normalized_text) if seg.strip()]
    return [seg for seg in segments if seg and not is_boilerplate(seg)]


def pair_sentences(left: Sequence[str], right: Sequence[str], embed_threshold: float = 0.88) -> List[SentencePair]:
    pairs: List[SentencePair] = []
    for sent_r in right:
        best_score = 0.0
        best_sent = ""
        for sent_l in left:
            score = _simple_similarity(sent_l, sent_r)
            if score > best_score:
                best_score = score
                best_sent = sent_l
        pairs.append(SentencePair(best_sent, sent_r, best_score, best_score >= embed_threshold))
    return pairs


def reuse_ratio(pairs: Iterable[SentencePair]) -> float:
    total = 0
    reused = 0
    for pair in pairs:
        length = len(pair.right)
        total += length
        if pair.matched:
            reused += length
    return 0.0 if total == 0 else reused / total
