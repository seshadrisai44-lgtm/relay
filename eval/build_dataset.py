import csv
import json
from collections import Counter

SRC = "eval/data/project_relay_synthetic_120_notes.csv"
with open(SRC, encoding="utf-8-sig") as f:
    rows = list(csv.DictReader(f))

notes, gold = [], []
for i, r in enumerate(rows, 1):
    nid = (r["note_id"] or "").strip() or f"n{i:03d}"
    exp = r["expected_result"].strip().lower()
    verdict = "block" if any(w in exp for w in ("block", "fail", "reject")) else "pass"
    notes.append(
        {
            "note_id": nid,
            "engagement_code": r["engagement"].strip(),
            "week_ending": r["week"].strip(),
            "submitted_by": r["owner"].strip(),
            "status": r["status"].strip().lower(),
            "progress_note": r["progress_note"],
            "category": r["category"].strip(),
        }
    )
    gold.append(
        {
            "note_id": nid,
            "gate_verdict": verdict,
            "expected_result_raw": r["expected_result"],
            "reason": r["expected_reason"],
        }
    )

with open("eval/data/notes.jsonl", "w", encoding="utf-8") as f:
    f.writelines(json.dumps(n) + "\n" for n in notes)
with open("eval/data/gold.jsonl", "w", encoding="utf-8") as f:
    f.writelines(json.dumps(g) + "\n" for g in gold)

print(len(notes), "notes written")
print(Counter(n["category"] for n in notes))
print(Counter(g["gate_verdict"] for g in gold))
