from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from typing import Dict, List, Tuple

from ..clean.units import normalize_pair, is_zero_value


@dataclass
class CellDiff:
    path_key: str
    left: Decimal | None
    right: Decimal | None
    unit: str
    changed: bool

    def to_dict(self) -> dict:
        return {
            "path_key": self.path_key,
            "left": float(self.left) if self.left is not None else None,
            "right": float(self.right) if self.right is not None else None,
            "unit": self.unit,
            "changed": self.changed,
        }


@dataclass
class TableDiffResult:
    comparable: int
    matched: int
    cells: List[CellDiff]

    @property
    def score(self) -> float:
        return 0.0 if self.comparable == 0 else self.matched / self.comparable

    def to_dict(self) -> dict:
        return {
            "comparable": self.comparable,
            "matched": self.matched,
            "score": self.score,
            "cells": [cell.to_dict() for cell in self.cells],
        }


def diff_tables(table_left: Dict[str, str], table_right: Dict[str, str]) -> TableDiffResult:
    cells: List[CellDiff] = []
    comparable = 0
    matched = 0
    keys = set(table_left.keys()) | set(table_right.keys())
    for key in sorted(keys):
        left_raw = table_left.get(key, "")
        right_raw = table_right.get(key, "")
        left, right, unit = normalize_pair(left_raw, right_raw)
        if is_zero_value(left) and is_zero_value(right):
            cells.append(CellDiff(key, left, right, unit, changed=False))
            continue
        if left is None and right is None:
            cells.append(CellDiff(key, None, None, unit, changed=False))
            continue
        comparable += 1
        changed = left != right
        if not changed:
            matched += 1
        cells.append(CellDiff(key, left, right, unit, changed=changed))
    return TableDiffResult(comparable=comparable, matched=matched, cells=cells)


class BalanceError(Exception):
    pass


def check_sec3_balance(table: Dict[str, str]) -> Tuple[bool, Decimal | None]:
    first = normalize_pair(table.get("第一项", "0"), "0")[0] or Decimal(0)
    second = normalize_pair(table.get("第二项", "0"), "0")[0] or Decimal(0)
    third = normalize_pair(table.get("第三项", "0"), "0")[0] or Decimal(0)
    fourth = normalize_pair(table.get("第四项", "0"), "0")[0] or Decimal(0)
    diff = first + second - third - fourth
    return (diff == 0, diff)
