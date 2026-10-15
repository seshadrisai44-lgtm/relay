import json

from audit.audit_log import append_event, verify


def test_chain_verifies(tmp_path):
    p = str(tmp_path / "a.jsonl")
    for i in range(3):
        append_event("u_1001", "approve", p, changeset="cs1", n=i)
    assert verify(p) is None


def test_edit_is_detected(tmp_path):
    p = str(tmp_path / "a.jsonl")
    for i in range(3):
        append_event("u_1001", "approve", p, n=i)
    lines = open(p, encoding="utf-8").read().splitlines()
    e = json.loads(lines[1])
    e["actor"] = "someone_else"
    lines[1] = json.dumps(e, sort_keys=True, separators=(",", ":"))
    open(p, "w", encoding="utf-8").write("\n".join(lines) + "\n")
    assert verify(p) == 2
