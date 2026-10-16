# Project Relay: Client-Safe Status Bridge

Prototype, tested on synthetic data only. No agent, connector or file
transfer touches a client environment. Consultants type a fresh note on a
firm device. Two gates check it, then a lead approves each change.

## Status
Working: pattern gate, note form, planner and validator, lead review page,
workbook write-back, weekly digest, hash-chained audit log.
Stand-ins (not real models): model gate and extraction. See eval/report.md.

## Setup
1. `python -m venv .venv` then activate it (`.venv\Scripts\activate`)
2. `pip install fastapi uvicorn jinja2 python-multipart pydantic openai python-dotenv presidio-analyzer detect-secrets rapidfuzz openpyxl filelock apscheduler pyyaml httpx pytest`
3. `python -c "from adapters.make_workbook import make; make()"` creates relay_tracker.xlsx
4. `python -m pytest tests` must show no failures

## Configuration
Create `.env` in the project root (it is gitignored, never commit it):
```
OPENAI_API_KEY=your_key
RELAY_GATE_MODEL=your_model_name
```
If either value is missing or a placeholder, the model gate uses the
keyword stand-in. Never paste the key into chats.

## Run
- Server: `python -c "import uvicorn; from app.main import app; uvicorn.run(app, port=8010)"`
- Note form: http://127.0.0.1:8010/note?user=u_2001
- Review page (lead only): http://127.0.0.1:8010/review/<changeset_id>?user=u_1001
- Digest: `python -m digest.build 2026-10-16`
- Evaluation: `python -m eval.run_eval` (writes eval/report.md)
- Audit check: `python -c "from audit.audit_log import verify; print(verify())"` prints None if intact

## Add an engagement
Edit `registry/engagement.yaml` and add an entry:
```
- code: ENG-006        # must match ENG-000 format
  lead: u_1006
  consultants: [u_2009]
  milestones: {M1: "Kickoff complete"}
  kr_links: {M1: KR-6.1}
  denylist: [Invented Client Name]
```
Use invented names only. Add its client terms to the PG-08 pattern in
gate/pattern_gate.py (see below). Run the tests.

## Add a gate rule
1. In `gate/pattern_gate.py`, add `"PG-11": r"your regex"` to `PATTERNS`.
2. Add 3 positive and 3 negative tests in `tests/test_pattern_gate.py`.
3. Add 3 seeded leaks for it to the dataset, then rerun `python -m eval.run_eval`.
4. Every seeded leak must still be blocked and no clean note wrongly blocked.

## Rules for contributors
- Synthetic data only: no real notes, client names or details anywhere.
- Never commit .env, relay.db, relay_tracker.xlsx or audit/audit.jsonl.
- Nothing merges unless `python -m pytest tests` passes.
- Blocked note text is never stored or logged. The audit log holds IDs and rule codes only.

## Known gaps
- Model gate and extraction are stand-ins until an OpenAI key is available
- Teams card is a terminal stub (needs a Teams admin to create the webhook)
- Login is a stub (a `user` value); the pilot needs Entra ID single sign-on
- No 90-day delete job for stored note text
- Daily audit anchor hash is not posted to Teams
- Monday 8 a.m. digest schedule is not built
- PG-08 and PG-09 use fixed example names, not per-engagement denylists
