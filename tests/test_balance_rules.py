from decimal import Decimal

from api.core.diff.table import check_sec3_balance


def test_check_sec3_balance_pass():
    table = {
        "第一项": "20",
        "第二项": "30",
        "第三项": "25",
        "第四项": "25",
    }
    ok, delta = check_sec3_balance(table)
    assert ok
    assert delta == 0


def test_check_sec3_balance_fail():
    table = {
        "第一项": "20",
        "第二项": "20",
        "第三项": "10",
        "第四项": "10",
    }
    ok, delta = check_sec3_balance(table)
    assert not ok
    assert delta == Decimal("20")
