from decimal import Decimal

from api.core.clean.units import friendly_number, normalize_number, normalize_pair, is_zero_value


def test_normalize_number_with_chinese_digits():
    value, unit = normalize_number("三十万元")
    assert value == Decimal("300000")
    assert unit == "万元"


def test_normalize_pair_and_zero():
    left, right, unit = normalize_pair("10件", "10件")
    assert left == right == Decimal("10")
    assert unit == "件"
    assert is_zero_value(Decimal("0"))


def test_friendly_number_percent():
    value = Decimal("0.128")
    assert friendly_number(value, "%") == "12.80%"
