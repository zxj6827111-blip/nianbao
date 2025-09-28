from __future__ import annotations

from dataclasses import asdict
from decimal import Decimal
from typing import Dict, List

from ..core.diff.table import TableDiffResult, diff_tables, check_sec3_balance
from ..core.diff.text import pair_sentences, reuse_ratio, split_sentences
from ..core.facts.numbers import align_facts, extract_facts
from ..models.datastore import DATABASE


def _to_float(value: Decimal | None) -> float | None:
    if value is None:
        return None
    return float(value)


class CompareService:
    def compare(self, left_doc_id: int, right_doc_id: int) -> Dict[str, object]:
        left_doc = DATABASE.get_document(left_doc_id)
        right_doc = DATABASE.get_document(right_doc_id)
        if not left_doc or not right_doc:
            raise ValueError("documents not found")
        text_pairs: List[dict] = []
        text_scores: List[float] = []
        table_scores: List[float] = []
        table_details: Dict[str, TableDiffResult] = {}
        fact_pairs: Dict[str, List[dict]] = {}

        for sec_key in ["sec_1", "sec_2", "sec_3", "sec_4", "sec_5", "sec_6"]:
            left_section = DATABASE.get_section(left_doc.id, sec_key)
            right_section = DATABASE.get_section(right_doc.id, sec_key)
            if not left_section or not right_section:
                continue
            left_sentences = split_sentences(left_section.raw or "")
            right_sentences = split_sentences(right_section.raw or "")
            pairs = pair_sentences(left_sentences, right_sentences)
            text_pairs.extend([{**asdict(pair), "sec": sec_key} for pair in pairs])
            text_scores.append(reuse_ratio(pairs))

            facts_left = extract_facts(sec_key, left_sentences)
            facts_right = extract_facts(sec_key, right_sentences)
            aligned = align_facts(facts_left, facts_right)
            fact_pairs[sec_key] = [
                {
                    "key": key,
                    "left": _to_float(fact_map["left"].value) if fact_map["left"] else None,
                    "right": _to_float(fact_map["right"].value) if fact_map["right"] else None,
                    "unit": fact_map["left"].unit if fact_map["left"] else fact_map["right"].unit if fact_map["right"] else "",
                }
                for key, fact_map in aligned.items()
            ]

            if sec_key in {"sec_2", "sec_3", "sec_4"}:
                table_left = {}
                table_right = {}
                table_left_obj = DATABASE.get_table_by_section(left_section.id)
                table_right_obj = DATABASE.get_table_by_section(right_section.id)
                if table_left_obj:
                    for cell in DATABASE.list_cells(table_left_obj.id):
                        table_left[cell.path_key] = cell.value_raw
                if table_right_obj:
                    for cell in DATABASE.list_cells(table_right_obj.id):
                        table_right[cell.path_key] = cell.value_raw
                diff = diff_tables(table_left, table_right)
                table_scores.append(diff.score)
                table_details[sec_key] = diff

        balance_ok, balance_delta = check_sec3_balance({})

        summary = {
            "text_reuse": sum(text_scores) / len(text_scores) if text_scores else 0.0,
            "table_reuse": sum(table_scores) / len(table_scores) if table_scores else 0.0,
            "balance_ok": balance_ok,
            "balance_delta": float(balance_delta or 0),
            "facts": fact_pairs,
        }
        return {
            "summary": summary,
            "text_pairs": text_pairs,
            "tables": {key: value.to_dict() for key, value in table_details.items()},
        }
