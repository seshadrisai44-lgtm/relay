from agent.plan import plan_note

ENG = {
    "ENG-001": {
        "code": "ENG-001",
        "lead": "u_1001",
        "consultants": ["u_2001"],
        "milestones": {"M1": "Phase 1"},
        "kr_links": {"M1": "KR-1.1"},
    }
}
NOTE = {
    "engagement_code": "ENG-001",
    "week_ending": "2026-10-16",
    "submitted_by": "u_2001",
    "status": "green",
    "help_needed": False,
}


def parsed(**kw):
    base = {"milestones_done": [], "tasks": [], "blockers": []}
    base.update(kw)
    return base


def test_basic_ops():
    r = plan_note(
        NOTE, parsed(milestones_done=["M1"], tasks=[{"title": "Review runbook"}]), ENG
    )
    kinds = [o["op"] for o in r["ops"]]
    assert kinds == ["complete_task", "update_kr", "create_task"]
    assert r["errors"] == []


def test_unknown_milestone_rejected():
    r = plan_note(NOTE, parsed(milestones_done=["M9"]), ENG)
    assert r["ops"] == [] and r["errors"]


def test_echoed_email_rejected():
    r = plan_note(NOTE, parsed(tasks=[{"title": "Mail bob@example.com"}]), ENG)
    assert r["ops"] == [] and r["errors"]


def test_red_status_flags_lead():
    r = plan_note({**NOTE, "status": "red"}, parsed(), ENG)
    assert r["ops"][0]["op"] == "flag_for_lead"


def test_idem_key_is_stable():
    p = parsed(tasks=[{"title": "Review runbook"}])
    a = plan_note(NOTE, p, ENG)["ops"][0]["idem_key"]
    b = plan_note(NOTE, p, ENG)["ops"][0]["idem_key"]
    assert a == b
