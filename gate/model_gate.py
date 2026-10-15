import json
import os

SOFT_WORDS = [
    "unpatched",
    "weak admin",
    "not encrypted",
    "one login",
    "layoffs",
    "no segmentation",
    "any traffic",
    "salary",
    "merger",
    "open to the internet",
]


def stub_gate(note_text: str) -> dict:
    t = note_text.lower()
    hits = [w for w in SOFT_WORDS if w in t]
    if hits:
        return {
            "decision": "BLOCK",
            "spans": [{"text": h, "reason": "stub keyword"} for h in hits],
        }
    return {"decision": "PASS", "spans": []}


def model_gate(note_text: str) -> dict:
    key = os.environ.get("OPENAI_API_KEY", "")
    model = os.environ.get("RELAY_GATE_MODEL", "")
    if key in ("", "your_key_here") or model in (
        "",
        "the_real_model_name",
        "your_model_name",
    ):
        return stub_gate(note_text)
    try:
        from openai import OpenAI

        client = OpenAI(api_key=key, timeout=20, max_retries=2)
        resp = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": 'Reply only with JSON: {"verdict":"safe"|"unsafe"|"unsure"}. Unsafe if the note reveals client systems, people, findings or business details. When in doubt, unsure.',
                },
                {"role": "user", "content": "NOTE:\n<<<\n" + note_text + "\n>>>"},
            ],
        )
        verdict = json.loads(resp.choices[0].message.content)["verdict"]
    except Exception:
        return {"decision": "BLOCK", "spans": [], "error": True}
    return {"decision": "PASS" if verdict == "safe" else "BLOCK", "spans": []}
