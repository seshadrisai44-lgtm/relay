import json

from agent.extract import extract_note
from agent.plan import load_registry, plan_note

reg = load_registry()


def load(name):
    with open(f"eval/data/{name}", encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


notes = load("notes.jsonl")
gold = {g["note_id"]: g for g in load("gold.jsonl")}


def shape(op):
    key = op.get("task_ref") or op.get("kr_id") or op.get("title") or op.get("summary")
    return (op["op"], str(key or "").strip().lower())


checked = same = 0
mismatches = []
for n in notes:
    g = gold[n["note_id"]]
    if g.get("gate_verdict") != "pass" or "changeset_ops" not in g:
        continue
    cs = plan_note(n, extract_note(n), reg)
    got = sorted(shape(o) for o in cs["ops"])
    want = sorted(shape(o) for o in g.get("changeset_ops", []))
    checked += 1
    if got == want:
        same += 1
    else:
        mismatches.append(n["note_id"])

print("notes checked:", checked, "| change sets match gold:", same)
print("mismatches:", mismatches[:10])
