import json

from dotenv import load_dotenv

load_dotenv()
from gate.model_gate import model_gate

notes = [json.loads(l) for l in open("eval/data/notes.jsonl", encoding="utf-8")]
gold = [json.loads(l) for l in open("eval/data/gold.jsonl", encoding="utf-8")]

soft = [n for n, g in zip(notes, gold) if g.get("leak_rule") == "soft"]
clean = [n for n in notes if n["category"] == "clean"]

blocked = sum(model_gate(n["progress_note"])["decision"] == "BLOCK" for n in soft)
wrong = sum(model_gate(n["progress_note"])["decision"] == "BLOCK" for n in clean)
print(f"soft leaks blocked: {blocked}/10 (target 9+)")
print(f"clean wrongly blocked: {wrong}/70 (target 7 or fewer)")
