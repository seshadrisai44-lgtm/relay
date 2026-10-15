import json

NOTES = "eval/data/notes.jsonl"
MAP = {"ACME-DEMO": "ENG-001", "RELAY-TEST": "ENG-002"}

notes = [json.loads(l) for l in open(NOTES, encoding="utf-8")]
for n in notes:
    n["engagement_code"] = MAP.get(n["engagement_code"], n["engagement_code"])
    n["submitted_by"] = "u_2001" if n["engagement_code"] == "ENG-001" else "u_2003"

with open(NOTES, "w", encoding="utf-8") as f:
    f.writelines(json.dumps(n) + "\n" for n in notes)
print("done")
