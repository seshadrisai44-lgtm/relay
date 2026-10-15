import hashlib
from datetime import date, timedelta

import yaml

from gate.pattern_gate import check_note

ALLOWED_OPS = {
    "create_task",
    "complete_task",
    "update_task_status",
    "create_blocker",
    "update_kr",
    "flag_for_lead",
}


def load_registry(path="registry/engagement.yaml"):
    with open(path, encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return {e["code"]: e for e in data["engagements"]}


def _week(note):
    try:
        return date.fromisoformat(str(note.get("week_ending")))
    except ValueError:
        return date.today()


def _key(code, week, op, ref):
    raw = "|".join([code, str(week), op, str(ref).strip().lower()])
    return hashlib.sha256(raw.encode()).hexdigest()[:16]


def propose(note, parsed, eng):
    week = _week(note)
    due = (week + timedelta(days=7)).isoformat()
    who = note.get("submitted_by")
    assignee = who if who in eng["consultants"] else eng["consultants"][0]
    ops, kr_delta = [], {}
    for m in parsed.get("milestones_done", []):
        ops.append(
            {
                "op": "complete_task",
                "task_ref": m,
                "reason": f"Milestone {m} marked done",
            }
        )
        kr = eng.get("kr_links", {}).get(m)
        if kr:
            kr_delta[kr] = kr_delta.get(kr, 0) + 1
    for kr, d in kr_delta.items():
        ops.append(
            {"op": "update_kr", "kr_id": kr, "delta": d, "evidence": "milestones done"}
        )
    for t in parsed.get("tasks", []):
        ops.append(
            {"op": "create_task", "title": t["title"], "assignee": assignee, "due": due}
        )
    for b in parsed.get("blockers", []):
        ops.append(
            {
                "op": "create_blocker",
                "summary": b["summary"],
                "category": b["category"],
                "severity": b["severity"],
                "assignee": eng["lead"],
            }
        )
    if note.get("status") == "red" or note.get("help_needed"):
        ops.append(
            {
                "op": "flag_for_lead",
                "lead": eng["lead"],
                "reason": "red status or help requested",
            }
        )
    return ops


def validate(ops, note, parsed, eng):
    errors = []
    week = _week(note)
    people = set(eng["consultants"]) | {eng["lead"]}
    done = parsed.get("milestones_done", [])
    for op in ops:
        name = op.get("op")
        if name not in ALLOWED_OPS:
            return [f"op not allowed: {name}"]
        if name == "complete_task" and op["task_ref"] not in eng["milestones"]:
            errors.append(f"out of scope: {op['task_ref']}")
        if name == "update_kr":
            linked = [m for m in done if eng["kr_links"].get(m) == op["kr_id"]]
            if op["kr_id"] not in eng["kr_links"].values():
                errors.append(f"out of scope: {op['kr_id']}")
            elif op["delta"] > len(linked):
                errors.append("KR delta too large")
        if "assignee" in op and op["assignee"] not in people:
            errors.append(f"assignee not on engagement: {op['assignee']}")
        if "due" in op:
            d = date.fromisoformat(op["due"])
            if not (week <= d <= week + timedelta(days=21)):
                errors.append("due date out of bounds")
        for field in ("title", "summary", "reason", "evidence"):
            if field in op and not check_note(op[field])["allowed"]:
                errors.append(f"text re-scan blocked: {field}")
    return errors


def plan_note(note, parsed, registry):
    code = note.get("engagement_code")
    if code not in registry:
        return {"changeset_id": None, "ops": [], "errors": ["unknown engagement"]}
    eng = registry[code]
    ops = propose(note, parsed, eng)
    errors = validate(ops, note, parsed, eng)
    week = _week(note)
    if errors:
        return {
            "changeset_id": None,
            "engagement_code": code,
            "ops": [],
            "errors": errors,
        }
    for op in ops:
        ref = (
            op.get("task_ref")
            or op.get("kr_id")
            or op.get("title")
            or op.get("summary")
            or "flag"
        )
        op["idem_key"] = _key(code, week, op["op"], ref)
    return {
        "changeset_id": f"cs_{code}_{week}",
        "engagement_code": code,
        "ops": ops,
        "errors": [],
    }
