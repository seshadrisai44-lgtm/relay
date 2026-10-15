import os
from datetime import UTC, datetime

from filelock import FileLock
from openpyxl import load_workbook
from openpyxl.utils import get_column_letter, range_boundaries

PATH = "relay_tracker.xlsx"


def _append(wb, sheet, values):
    ws = wb[sheet]
    tbl = list(ws.tables.values())[0]
    c1, r1, c2, r2 = range_boundaries(tbl.ref)
    placeholder = r2 == r1 + 1 and all(
        ws.cell(row=r2, column=c).value is None for c in range(c1, c2 + 1)
    )
    row = r2 if placeholder else r2 + 1
    for i, v in enumerate(values):
        ws.cell(row=row, column=c1 + i, value=v)
    if not placeholder:
        tbl.ref = f"{get_column_letter(c1)}{r1}:{get_column_letter(c2)}{row}"
        if tbl.autoFilter is not None:
            tbl.autoFilter.ref = tbl.ref


def _find(wb, sheet, col, value):
    for row in wb[sheet].iter_rows(min_row=2):
        if row[col - 1].value == value:
            return row
    return None


def _do(wb, cs, op, now):
    code = cs["engagement_code"]
    key = op["idem_key"]
    kind = op["op"]
    if kind == "create_task":
        _append(
            wb,
            "Tasks",
            [
                f"T-{key[:6]}",
                code,
                op["title"],
                op["assignee"],
                op["due"],
                "open",
                cs.get("source_note_id", ""),
                key,
                now,
            ],
        )
    elif kind == "complete_task":
        tid = f"{code}-{op['task_ref']}"
        row = _find(wb, "Tasks", 1, tid)
        if row:
            row[5].value = "done"
            row[8].value = now
        else:
            _append(
                wb,
                "Tasks",
                [
                    tid,
                    code,
                    op["reason"],
                    "",
                    "",
                    "done",
                    cs.get("source_note_id", ""),
                    key,
                    now,
                ],
            )
    elif kind == "update_kr":
        row = _find(wb, "KRs", 1, op["kr_id"])
        if row:
            row[4].value = (row[4].value or 0) + op["delta"]
            row[6].value = now
        else:
            _append(wb, "KRs", [op["kr_id"], "", "", "", op["delta"], "", now])
    elif kind == "create_blocker":
        _append(
            wb,
            "Blockers",
            [
                f"B-{key[:6]}",
                code,
                op["summary"],
                op["category"],
                op["severity"],
                op["assignee"],
                now[:10],
                "open",
                key,
            ],
        )
    # flag_for_lead has no sheet; it is recorded in Applied only


def apply_changeset(cs, approved_by, path=PATH):
    applied = skipped = 0
    now = datetime.now(UTC).isoformat(timespec="seconds")
    with FileLock(path + ".lock"):
        wb = load_workbook(path)
        done = {
            r[0] for r in wb["Applied"].iter_rows(min_row=2, values_only=True) if r[0]
        }
        for op in cs["ops"]:
            if op["idem_key"] in done:
                skipped += 1
                continue
            _do(wb, cs, op, now)
            _append(
                wb,
                "Applied",
                [op["idem_key"], op["op"], cs["changeset_id"], approved_by, now],
            )
            done.add(op["idem_key"])
            applied += 1
        tmp = path + ".tmp.xlsx"
        wb.save(tmp)
        os.replace(tmp, path)
    return applied, skipped
