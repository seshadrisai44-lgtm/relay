from agent.extract import extract_note
from agent.plan import load_registry, plan_note
from app.review import register_changeset

note = {
    "note_id": "demo1",
    "engagement_code": "ENG-001",
    "week_ending": "2026-10-16",
    "submitted_by": "u_2001",
    "status": "amber",
    "help_needed": False,
    "milestones_done": ["M1"],
    "next_week": ["Review phase 2 runbook"],
    "blockers": ["Waiting on access approval"],
}
cs = plan_note(note, extract_note(note), load_registry())
print(cs["errors"] or "plan ok")
register_changeset(cs)
