from datetime import date

from digest.build import build_digest

REG = {"ENG-1": {"consultants": ["u1", "u2"], "milestones": {"M1": "a", "M2": "b"}}}
NOW = [
    {
        "code": "ENG-1",
        "user": "u1",
        "status": "amber",
        "hours": 40,
        "milestones": ["M1"],
    }
]
PRIOR = [
    {"code": "ENG-1", "user": "u1", "status": "green", "hours": 38, "milestones": []}
]
BLOCKERS = [
    {"code": "ENG-1", "severity": "high", "opened_on": "2026-10-09", "status": "open"},
    {"code": "ENG-1", "severity": "high", "opened_on": "2026-10-14", "status": "open"},
    {
        "code": "ENG-1",
        "severity": "medium",
        "opened_on": "2026-10-01",
        "status": "open",
    },
]


def test_rollups():
    d = build_digest("2026-10-16", NOW, PRIOR, REG, BLOCKERS, date(2026, 10, 16))
    e = d["engagements"]["ENG-1"]
    assert (e["status"], e["previous"]) == ("amber", "green")
    assert (e["hours"], e["plan_hours"], e["kr"]) == (40, 80, "1/2")
    assert d["missing"] == [("ENG-1", "u2")]
    assert d["old_high_blockers"] == [("ENG-1", 7)]


def test_no_notes_means_missing():
    d = build_digest("2026-10-16", [], [], REG, [], date(2026, 10, 16))
    assert d["engagements"]["ENG-1"]["status"] == "missing"
    assert len(d["missing"]) == 2
