import hashlib
import json
import os
from datetime import UTC, datetime

LOG_PATH = "audit/audit.jsonl"


def create_audit_event(action: str, status: str) -> dict:
    """Create a minimal audit event without recording note contents."""
    return {
        "timestamp": datetime.now(UTC).isoformat(),
        "action": action,
        "status": status,
    }


def _canonical(entry: dict) -> str:
    return json.dumps(entry, sort_keys=True, separators=(",", ":"))


def _hash(prev_hash: str, entry: dict) -> str:
    return hashlib.sha256((prev_hash + _canonical(entry)).encode()).hexdigest()


def _last(path):
    if not os.path.exists(path):
        return 0, "0" * 64
    last = None
    with open(path, encoding="utf-8") as f:
        for line in f:
            if line.strip():
                last = json.loads(line)
    return (last["seq"], last["hash"]) if last else (0, "0" * 64)


def append_event(actor, event, path=LOG_PATH, **details):
    """Append a hash-chained entry. Never pass note text in details."""
    seq, prev = _last(path)
    entry = {
        "seq": seq + 1,
        "ts": datetime.now(UTC).isoformat(),
        "actor": actor,
        "event": event,
        **details,
        "prev_hash": prev,
    }
    entry["hash"] = _hash(prev, entry)
    with open(path, "a", encoding="utf-8") as f:
        f.write(_canonical(entry) + "\n")
    return entry


def verify(path=LOG_PATH):
    """Return None if the chain is intact, else the first broken seq number."""
    prev = "0" * 64
    if not os.path.exists(path):
        return None
    with open(path, encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            entry = json.loads(line)
            stored = entry.pop("hash")
            if entry["prev_hash"] != prev or _hash(prev, entry) != stored:
                return entry["seq"]
            prev = stored
    return None
