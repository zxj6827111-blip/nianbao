from api.core.diff.table import diff_tables


def test_zero_cells_excluded():
    left = {"A": "0", "B": "10"}
    right = {"A": "0", "B": "12"}
    result = diff_tables(left, right)
    assert result.comparable == 1
    assert result.matched == 0
    cells = {cell.path_key: cell for cell in result.cells}
    assert cells["A"].changed is False
    assert cells["B"].changed is True
