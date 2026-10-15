from fastapi import APIRouter, Form, HTTPException
from fastapi.responses import HTMLResponse

from adapters.spreadsheet import apply_changeset
from agent.plan import load_registry
from app.approval import can_write_back

router = APIRouter()
CHANGESETS = {}  # changeset_id -> changeset dict (in memory for the prototype)


def post_review_card(engagement_code, op_count, review_url):
    # Stub: prints instead of posting to Teams. Never put note text here.
    print(
        f"[TEAMS CARD] Change set ready: {engagement_code} | "
        f"{op_count} proposed updates | Review: {review_url}"
    )


def register_changeset(cs, base_url="http://127.0.0.1:8000"):
    CHANGESETS[cs["changeset_id"]] = cs
    post_review_card(
        cs["engagement_code"],
        len(cs["ops"]),
        f"{base_url}/review/{cs['changeset_id']}?user=LEAD_ID",
    )


def _lead_of(cs):
    return load_registry()[cs["engagement_code"]]["lead"]


@router.get("/review/{changeset_id}", response_class=HTMLResponse)
def review_page(changeset_id: str, user: str = ""):
    cs = CHANGESETS.get(changeset_id)
    if not cs:
        raise HTTPException(404, "unknown change set")
    if user != _lead_of(cs):
        raise HTTPException(403, "only the engagement lead can review")
    boxes = "".join(
        f'<li><label><input type="checkbox" name="approve" value="{i}" checked> '
        f"{op['op']}: {op.get('title') or op.get('summary') or op.get('task_ref') or op.get('kr_id') or ''}"
        f"</label></li>"
        for i, op in enumerate(cs["ops"])
    )
    return (
        f"<h2>{cs['engagement_code']}: {len(cs['ops'])} proposed updates</h2>"
        f'<form method="post" action="/review/{changeset_id}">'
        f'<input type="hidden" name="user" value="{user}">'
        f"<ul>{boxes}</ul><p>Untick any op to reject it.</p>"
        f'<button type="submit">Apply approved</button></form>'
    )


@router.post("/review/{changeset_id}")
def review_submit(
    changeset_id: str, user: str = Form(""), approve: list[str] = Form(default=[])
):
    cs = CHANGESETS.get(changeset_id)
    if not cs:
        raise HTTPException(404, "unknown change set")
    if user != _lead_of(cs):
        raise HTTPException(403, "only the engagement lead can approve")
    chosen = [cs["ops"][int(i)] for i in approve]
    if not can_write_back(bool(chosen)):
        return {"applied": 0, "skipped": 0, "note": "nothing approved"}
    applied, skipped = apply_changeset({**cs, "ops": chosen}, user)
    return {"applied": applied, "skipped": skipped}
