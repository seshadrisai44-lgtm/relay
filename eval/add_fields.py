import json

NOTES = "eval/data/notes.jsonl"
notes = [json.loads(l) for l in open(NOTES, encoding="utf-8")]

for i, n in enumerate(notes):
    n["hours"] = {"delivery": 30, "meetings": 6, "travel": 0, "admin": 4}
    n["milestones_done"] = ["M1"] if i % 3 == 0 else []
    n["blockers"] = ["Waiting on access approval"] if i % 4 == 0 else []
    n["next_week"] = ["Review phase 2 runbook"] if i % 2 == 0 else []
    n["help_needed"] = i % 10 == 0

with open(NOTES, "w", encoding="utf-8") as f:
    f.writelines(json.dumps(n) + "\n" for n in notes)
print(len(notes), "notes updated")
