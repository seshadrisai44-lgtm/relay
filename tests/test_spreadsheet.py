from openpyxl import load_workbook

from adapters.make_workbook import make
from adapters.spreadsheet import apply_changeset

CS = {
    "changeset_id": "cs1",
    "engagement_code": "ENG-001",
    "ops": [
        {
            "op": "create_task",
            "title": "Review",
            "assignee": "u_2001",
            "due": "2026-10-23",
            "idem_key": "k1aaaaaa",
        },
        {"op": "update_kr", "kr_id": "KR-1.1", "delta": 1, "idem_key": "k2bbbbbb"},
    ],
}


def test_apply_twice_makes_one_copy(tmp_path):
    p = str(tmp_path / "t.xlsx")
    make(p)
    assert apply_changeset(CS, "u_1001", p) == (2, 0)
    assert apply_changeset(CS, "u_1001", p) == (0, 2)
    wb = load_workbook(p)
    rows = [r for r in wb["Tasks"].iter_rows(min_row=2, values_only=True) if r[0]]
    assert len(rows) == 1


def test_table_range_extends(tmp_path):
    p = str(tmp_path / "t.xlsx")
    make(p)
    cs = {
        "changeset_id": "cs2",
        "engagement_code": "ENG-001",
        "ops": [
            {
                "op": "create_task",
                "title": f"Task {i}",
                "assignee": "u_2001",
                "due": "2026-10-23",
                "idem_key": f"key{i}xxxx",
            }
            for i in range(3)
        ],
    }
    apply_changeset(cs, "u_1001", p)
    wb = load_workbook(p)
    assert wb["Tasks"].tables["tblTasks"].ref == "A1:I4"
