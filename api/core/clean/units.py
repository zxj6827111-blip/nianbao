from __future__ import annotations

import re
from decimal import Decimal, ROUND_HALF_UP
from typing import Optional, Tuple

UNIT_MAP = {
    "元": Decimal("1"),
    "万元": Decimal("10000"),
    "件": Decimal("1"),
    "条": Decimal("1"),
    "个": Decimal("1"),
    "人次": Decimal("1"),
    "%": Decimal("0.01"),
}

CHINESE_NUM_MAP = {
    "零": 0,
    "一": 1,
    "二": 2,
    "两": 2,
    "三": 3,
    "四": 4,
    "五": 5,
    "六": 6,
    "七": 7,
    "八": 8,
    "九": 9,
}


def _parse_chinese_digits(text: str) -> Optional[int]:
    if not text:
        return None
    units = {"十": 10, "百": 100, "千": 1000, "万": 10000}
    total = 0
    current = 0
    num = 0
    for ch in text:
        if ch in CHINESE_NUM_MAP:
            num = CHINESE_NUM_MAP[ch]
        elif ch in units:
            unit_value = units[ch]
            if ch == "万":
                current += num
                total += current * unit_value
                current = 0
                num = 0
            else:
                if num == 0:
                    num = 1
                current += num * unit_value
                num = 0
        else:
            return None
    return total + current + num


VALUE_RE = re.compile(
    r"(?P<sign>[+-])?(?P<num>(?:\d{1,3}(?:,\d{3})+|\d+)(?:\.\d+)?|[零一二三四五六七八九十]+)(?P<unit>万元|元|件|条|个|人次|%)?"
)


def normalize_number(text: str) -> Optional[Tuple[Decimal, str]]:
    match = VALUE_RE.search(text.replace("，", ","))
    if not match:
        return None
    number_text = match.group("num")
    unit = match.group("unit") or ""
    if number_text.isdigit() or re.match(r"^\d", number_text):
        number = Decimal(number_text.replace(",", ""))
    else:
        parsed = _parse_chinese_digits(number_text)
        if parsed is None:
            return None
        number = Decimal(parsed)
    scale = UNIT_MAP.get(unit, Decimal("1"))
    normalized = (number * scale).quantize(Decimal("0.0001"))
    return normalized, unit


def normalize_pair(value_left: str, value_right: str) -> Tuple[Optional[Decimal], Optional[Decimal], str]:
    left = normalize_number(value_left)
    right = normalize_number(value_right)
    unit = left[1] if left else right[1] if right else ""
    return (left[0] if left else None, right[0] if right else None, unit)


def friendly_number(value: Decimal, unit: str) -> str:
    if unit == "%":
        scaled = (value * Decimal("100")).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        return f"{scaled}%"
    if unit == "万元" and value % Decimal("10000") == 0:
        return f"{(value / Decimal('10000')).quantize(Decimal('1'))}万元"
    if value % Decimal("1") == 0:
        return f"{value.quantize(Decimal('1'))}{unit}"
    return f"{value.normalize()}{unit}"


def is_zero_value(value: Optional[Decimal]) -> bool:
    return value is not None and value == 0
