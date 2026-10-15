import json
import sqlite3
import uuid
from html import escape

from dotenv import load_dotenv
from fastapi import APIRouter, Form, HTTPException
from fastapi.responses import HTMLResponse

from agent.plan import load_registry
from audit.audit_log import append_event
from gate.model_gate import model_gate
from gate.pattern_gate import check_note

load_dotenv()
router = APIRouter()
DB = "relay.db"


def _db():
    con = sqlite3.connect(DB)
    con.execute("PRAGMA journal_mode=WAL")
    con.execute("""CREATE TABLE IF NOT EXISTS notes (
        note_id TEXT PRIMARY KEY, engagement_code TEXT, submitted_by TEXT,
        week_ending TEXT, status TEXT, data TEXT,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP)""")
    return con


def _lines(text, max_items, max_len):
    items = [x.strip() for x in text.splitlines() if x.strip()]
    if len(items) > max_items or any(len(x) > max_len for x in items):
        raise HTTPException(422, f"max {max_items} items of {max_len} characters")
    return items


@router.get("/note", response_class=HTMLResponse)
def note_form(user: str = ""):
    reg = load_registry()
    mine = [e for e in reg.values() if user in e["consultants"]]
    if not mine:
        raise HTTPException(403, "you are not assigned to any engagement")
    opts = "".join(f"<option>{escape(e['code'])}</option>" for e in mine)
    ms = "".join(
        f'<label><input type="checkbox" name="milestones_done" value="{escape(m)}"> '
        f"{escape(m)} {escape(t)}</label><br>"
        for m, t in mine[0]["milestones"].items()
    )
    return f"""<h2>Weekly note</h2>
<form method="post" action="/note">
<input type="hidden" name="user" value="{escape(user)}">
Engagement: <select name="engagement_code">{opts}</select><br><br>
Week ending (Friday): <input name="week_ending" placeholder="2026-10-16"><br><br>
Status: <select name="status"><option>green</option><option>amber</option><option>red</option></select><br><br>
Milestones done:<br>{ms}<br>
Hours (0 to 60 each, total 60 or less):<br>
Delivery <input name="h_delivery" type="number" min="0" max="60" step="0.5" value="0" style="width:60px">
Meetings <input name="h_meetings" type="number" min="0" max="60" step="0.5" value="0" style="width:60px">
Travel <input name="h_travel" type="number" min="0" max="60" step="0.5" value="0" style="width:60px">
Admin <input name="h_admin" type="number" min="0" max="60" step="0.5" value="0" style="width:60px"><br><br>
Progress (600 chars max, no client details):<br>
<textarea name="progress_note" rows="4" cols="50" maxlength="600"></textarea><br><br>
Blockers (one per line, max 3):<br><textarea name="blockers" rows="3" cols="50"></textarea><br><br>
Next week (one per line, max 5):<br><textarea name="next_week" rows="4" cols="50"></textarea><br><br>
<label><input type="checkbox" name="help_needed"> Help needed</label><br><br>
<label><input type="checkbox" name="attest"> I typed this on a firm device and it contains no client data.</label><br><br>
<button type="submit">Submit</button></form>"""


@router.post("/note", response_class=HTMLResponse)
def note_submit(
    user: str = Form(""),
    engagement_code: str = Form(""),
    week_ending: str = Form(""),
    status: str = Form("green"),
    milestones_done: list[str] = Form(default=[]),
    progress_note: str = Form(""),
    blockers: str = Form(""),
    next_week: str = Form(""),
    help_needed: str = Form(""),
    h_delivery: float = Form(0),
    h_meetings: float = Form(0),
    h_travel: float = Form(0),
    h_admin: float = Form(0),
    attest: str = Form(""),
):
    eng = load_registry().get(engagement_code)
    if not eng or user not in eng["consultants"]:
        raise HTTPException(403, "you are not on this engagement")
    if not attest:
        raise HTTPException(422, "attestation is required")
    if status not in ("green", "amber", "red") or len(progress_note) > 600:
        raise HTTPException(422, "invalid input")
    if any(m not in eng["milestones"] for m in milestones_done):
        raise HTTPException(422, "unknown milestone")
    data = {
        "progress_note": progress_note,
        "blockers": _lines(blockers, 3, 200),
        "next_week": _lines(next_week, 5, 120),
    }
    hours = {
        "delivery": h_delivery,
        "meetings": h_meetings,
        "travel": h_travel,
        "admin": h_admin,
    }
    if any(not 0 <= v <= 60 for v in hours.values()) or sum(hours.values()) > 60:
        raise HTTPException(422, "hours must be 0 to 60 each, total 60 or less")
    note_id = "note_" + uuid.uuid4().hex[:8]

    # Gate 1: pattern gate, every free-text field, runs before any model call
    hits = []
    fields = [("progress_note", progress_note)]
    fields += [("blockers", b) for b in data["blockers"]]
    fields += [("next_week", n) for n in data["next_week"]]
    for name, text in fields:
        r = check_note(text)
        hits += [f"{name}: {rule}" for rule in r["findings"]]
    if hits:
        append_event(
            "gate.pattern",
            "block",
            note_id=note_id,
            engagement=engagement_code,
            rules=hits,
        )
        return (
            f"<h3>Blocked by the pattern gate</h3><p>{escape(', '.join(hits))}</p>"
            "<p>Rewrite without client details and resubmit. Nothing was saved.</p>"
        )

    # Gate 2: model gate on all free text together; fails closed
    combined = "\n".join(t for _, t in fields)
    if model_gate(combined)["decision"] != "PASS":
        append_event("gate.model", "block", note_id=note_id, engagement=engagement_code)
        return (
            "<h3>Blocked by the model gate</h3>"
            "<p>The note may contain client detail. Rewrite it and resubmit. "
            "Nothing was saved.</p>"
        )

    data.update(
        {
            "milestones_done": milestones_done,
            "help_needed": bool(help_needed),
            "hours": hours,
        }
    )
    with _db() as con:
        con.execute(
            "INSERT INTO notes (note_id, engagement_code, submitted_by, "
            "week_ending, status, data) VALUES (?,?,?,?,?,?)",
            (note_id, engagement_code, user, week_ending, status, json.dumps(data)),
        )
    append_event("gate.both", "pass", note_id=note_id, engagement=engagement_code)
    return f"<h3>Saved</h3><p>Note {note_id} passed both gates.</p>"
