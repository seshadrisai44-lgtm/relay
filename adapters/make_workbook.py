from openpyxl import Workbook
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.table import Table, TableStyleInfo

SHEETS = {
    "Tasks": (
        "tblTasks",
        [
            "task_id",
            "engagement_code",
            "title",
            "assignee",
            "due",
            "status",
            "source_note_id",
            "idem_key",
            "updated_at",
        ],
    ),
    "Blockers": (
        "tblBlockers",
        [
            "blocker_id",
            "engagement_code",
            "summary",
            "category",
            "severity",
            "assignee",
            "opened_on",
            "status",
            "idem_key",
        ],
    ),
    "KRs": (
        "tblKRs",
        [
            "kr_id",
            "objective",
            "key_result",
            "target",
            "current",
            "owner",
            "updated_at",
        ],
    ),
    "Submissions": (
        "tblSubmissions",
        [
            "note_id",
            "engagement_code",
            "week_ending",
            "submitted_by",
            "status_rag",
            "hours_total",
            "gate_result",
            "submitted_at",
        ],
    ),
    "Applied": (
        "tblApplied",
        ["idem_key", "op", "changeset_id", "approved_by", "applied_at"],
    ),
    "Digest": (
        "tblDigest",
        [
            "week_ending",
            "engagement_code",
            "status_rag",
            "hours_total",
            "open_blockers",
            "kr_progress",
        ],
    ),
}


def make(path="relay_tracker.xlsx"):
    wb = Workbook()
    wb.remove(wb.active)
    for name, (table, cols) in SHEETS.items():
        ws = wb.create_sheet(name)
        ws.append(cols)
        ws.append([None] * len(cols))
        t = Table(displayName=table, ref=f"A1:{get_column_letter(len(cols))}2")
        t.tableStyleInfo = TableStyleInfo(name="TableStyleMedium2", showRowStripes=True)
        ws.add_table(t)
    wb.save(path)
