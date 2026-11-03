import json
import sqlite3
import sys
from datetime import date, timedelta

from filelock import FileLock
from openpyxl import load_workbook

from adapters.spreadsheet import _append
from agent.plan import load_registry

DB = "relay.db"
XLSX = "relay_tracker.xlsx"
PLAN_HOURS = 40  # planned hours per consultant per week


def load_notes(week, db=DB):
    con = sqlite3.connect(db)
    try:
        rows = con.execute(
            "SELECT engagement_code, submitted_by, status, data FROM notes "
            "WHERE week_ending=? ORDER BY created_at",
            (week,),
        ).fetchall()
    except sqlite3.OperationalError:
        rows = []
    con.close()
    notes = {}
    for code, user, status, data in rows:  # latest note per person wins
        d = json.loads(data)
        notes[(code, user)] = {
            "code": code,
            "user": user,
            "status": status,
            "hours": sum(d.get("hours", {}).values()),
            "milestones": d.get("milestones_done", []),
        }
    return list(notes.values())


def load_blockers(path=XLSX):
    wb = load_workbook(path)
    out = []
    for r in wb["Blockers"].iter_rows(min_row=2, values_only=True):
        if r[0]:  # ids and dates only, never text
            out.append(
                {"code": r[1], "severity": r[4], "opened_on": r[6], "status": r[7]}
            )
    return out


def build_digest(week, notes, prior, reg, blockers, today):
    out = {"week": week, "engagements": {}, "missing": [], "old_high_blockers": []}
    for code, e in reg.items():
        mine = [n for n in notes if n["code"] == code]
        prev = [n for n in prior if n["code"] == code]
        done = {m for n in mine for m in n["milestones"]}
        out["engagements"][code] = {
            "status": mine[-1]["status"] if mine else "missing",
            "previous": prev[-1]["status"] if prev else None,
            "hours": sum(n["hours"] for n in mine),
            "plan_hours": PLAN_HOURS * len(e["consultants"]),
            "kr": f"{len(done)}/{len(e['milestones'])}",
        }
        have = {n["user"] for n in mine}
        out["missing"] += [(code, u) for u in e["consultants"] if u not in have]
    for b in blockers:
        if b["severity"] == "high" and b["status"] == "open":
            age = (today - date.fromisoformat(str(b["opened_on"])[:10])).days
            if age > 5:
                out["old_high_blockers"].append((b["code"], age))
    return out


def write_digest(d, blockers, path=XLSX):
    with FileLock(path + ".lock"):
        wb = load_workbook(path)
        have = {
            (str(r[0]), r[1])
            for r in wb["Digest"].iter_rows(min_row=2, values_only=True)
            if r[0]
        }
        for code, e in d["engagements"].items():
            if (d["week"], code) in have:
                continue
            open_n = sum(
                1 for b in blockers if b["code"] == code and b["status"] == "open"
            )
            _append(
                wb,
                "Digest",
                [d["week"], code, e["status"], e["hours"], open_n, e["kr"]],
            )
        wb.save(path)


if __name__ == "__main__":
    week = sys.argv[1]
    prior = (date.fromisoformat(week) - timedelta(days=7)).isoformat()
    reg, blockers = load_registry(), load_blockers()
    d = build_digest(
        week, load_notes(week), load_notes(prior), reg, blockers, date.today()
    )
    write_digest(d, blockers)
    print(json.dumps(d, indent=2, default=str))
    try:
        from digest_ai import summarize

        print("\nAI summary:\n" + summarize(json.dumps(d, default=str)))
    except Exception as e:
        print("\n(AI summary skipped:", e, ")")
