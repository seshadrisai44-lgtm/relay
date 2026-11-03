import json
import logging
import os
import time
from pathlib import Path

PROMPT_VERSION = "gate_v1"
PROMPT_PATH = (
    Path(__file__).resolve().parent.parent
    / "agent"
    / "prompts"
    / f"{PROMPT_VERSION}.txt"
)

TIMEOUT_SECONDS = 20
MAX_RETRIES = 2
TEMPERATURE = 0

log = logging.getLogger("relay.model_gate")

VERDICT_SCHEMA = {
    "name": "gate_verdict",
    "strict": True,
    "schema": {
        "type": "object",
        "properties": {
            "verdict": {
                "type": "string",
                "enum": ["safe", "unsafe", "unsure"],
            },
            "spans": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "text": {"type": "string"},
                        "reason": {"type": "string"},
                    },
                    "required": ["text", "reason"],
                    "additionalProperties": False,
                },
            },
        },
        "required": ["verdict", "spans"],
        "additionalProperties": False,
    },
}

PLACEHOLDERS = {
    "",
    "your_key_here",
    "the_real_model_name",
    "your_model_name",
}

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
    """Keyword-based fallback used when model configuration is missing."""
    text = note_text.lower()
    hits = [word for word in SOFT_WORDS if word in text]

    if hits:
        return {
            "decision": "BLOCK",
            "spans": [{"text": word, "reason": "stub keyword"} for word in hits],
            "mode": "stub",
        }

    return {
        "decision": "PASS",
        "spans": [],
        "mode": "stub",
    }


def _make_client(api_key: str, base_url: str | None = None):
    from openai import OpenAI

    base_url = base_url or os.environ.get("RELAY_GATE_BASE_URL") or None

    return OpenAI(
        api_key=api_key,
        base_url=base_url,
        timeout=TIMEOUT_SECONDS,
        max_retries=MAX_RETRIES,
    )


def _prompt() -> str:
    """Load the model-gate instructions."""
    return PROMPT_PATH.read_text(encoding="utf-8")


def model_gate(note_text, api_key=None, model=None, base_url=None) -> dict:
    """Second gate. Any API error or non-safe verdict blocks the note."""
    key = (
        api_key
        or os.environ.get("RELAY_GATE_API_KEY")
        or os.environ.get("OPENAI_API_KEY")
        or ""
    ).strip()
    model = (model or os.environ.get("RELAY_GATE_MODEL", "")).strip()

    if key.lower() in PLACEHOLDERS or model.lower() in PLACEHOLDERS:
        return stub_gate(note_text)

    started = time.monotonic()
    verdict = "error"
    spans = []

    try:
        client = _make_client(key)

        extra = {} if TEMPERATURE is None else {"temperature": TEMPERATURE}

        response = client.chat.completions.create(
            model=model,
            response_format={
                "type": "json_schema",
                "json_schema": VERDICT_SCHEMA,
            },
            messages=[
                {
                    "role": "system",
                    "content": _prompt(),
                },
                {
                    "role": "user",
                    "content": f"NOTE:\n<<<\n{note_text}\n>>>",
                },
            ],
            **extra,
        )

        if not response.choices:
            raise ValueError(
                f"No choices: {getattr(response, 'error', None) or response}"
            )

        message = response.choices[0].message

        if message is None or not message.content:
            raise ValueError("Model returned empty response content")

        result = json.loads(message.content)

        verdict = result.get("verdict")

        if verdict not in ("safe", "unsafe", "unsure"):
            raise ValueError("Unknown or missing model verdict")

        raw_spans = result.get("spans", [])

        if not isinstance(raw_spans, list):
            raise TypeError("Model returned invalid spans")

        spans = [
            {
                "text": str(item.get("text", "")),
                "reason": str(item.get("reason", "")),
            }
            for item in raw_spans
            if isinstance(item, dict)
        ]

    except Exception as exc:
        # Do not log the note text, API key, or flagged spans.
        print(
            f"Model API error: {type(exc).__name__}: {exc}",
            flush=True,
        )
        verdict = "error"
        spans = []

    latency_ms = int((time.monotonic() - started) * 1000)

    log.info(
        "model_gate model=%s prompt=%s latency_ms=%d verdict=%s",
        model,
        PROMPT_VERSION,
        latency_ms,
        verdict,
    )

    passed = verdict == "safe"

    return {
        "decision": "PASS" if passed else "BLOCK",
        "spans": [] if passed else spans,
        "mode": "model",
        "model": model,
        "prompt_version": PROMPT_VERSION,
        "latency_ms": latency_ms,
        "verdict": verdict,
        "error": verdict == "error",
    }
