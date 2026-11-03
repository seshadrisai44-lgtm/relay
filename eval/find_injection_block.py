import json
import time

from dotenv import load_dotenv

load_dotenv()

from gate.model_gate import model_gate

with open("eval/data/notes.jsonl", encoding="utf-8") as f:
    notes = [json.loads(line) for line in f if line.strip()]

for n in notes:
    if n.get("category") != "injection":
        continue
    text = "\n".join(
        [n.get("progress_note", ""), *n.get("blockers", []), *n.get("next_week", [])]
    )
    r = model_gate(text)
    print(n["note_id"], r["decision"], r.get("verdict"), r.get("error"))
    time.sleep(1)
