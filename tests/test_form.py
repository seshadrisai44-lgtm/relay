import sqlite3

from fastapi.testclient import TestClient

from app import form
from app.main import app

client = TestClient(app)


def setup(monkeypatch, tmp_path):
    monkeypatch.setattr(form, "DB", str(tmp_path / "t.db"))
    monkeypatch.setattr(form, "append_event", lambda *a, **k: None)
    monkeypatch.setattr(form, "model_gate", lambda t: {"decision": "PASS"})


def body(text):
    return {
        "user": "u_2001",
        "engagement_code": "ENG-001",
        "status": "green",
        "week_ending": "2026-10-16",
        "progress_note": text,
        "attest": "on",
    }


def rows(tmp_path):
    con = sqlite3.connect(str(tmp_path / "t.db"))
    try:
        return con.execute("SELECT count(*) FROM notes").fetchone()[0]
    except sqlite3.OperationalError:
        return 0


def test_clean_note_saved(monkeypatch, tmp_path):
    setup(monkeypatch, tmp_path)
    r = client.post("/note", data=body("Finished phase 1 onboarding."))
    assert "Saved" in r.text and rows(tmp_path) == 1


def test_leak_not_saved(monkeypatch, tmp_path):
    setup(monkeypatch, tmp_path)
    r = client.post("/note", data=body("Contact alex@example.com"))
    assert "Blocked" in r.text and rows(tmp_path) == 0


def test_wrong_user_rejected(monkeypatch, tmp_path):
    setup(monkeypatch, tmp_path)
    d = body("ok")
    d["user"] = "u_2003"
    assert client.post("/note", data=d).status_code == 403
