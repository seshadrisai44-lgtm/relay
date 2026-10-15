import json
import re
from collections import Counter

NOTES = "eval/data/notes.jsonl"
GOLD = "eval/data/gold.jsonl"

RULES = [
    ("PG-03", r"[\w.+-]+@[\w-]+\.[\w.]+|https?://"),
    ("PG-05", r"PASSWORD=|API_KEY|SECRET|AKIA|password|credential"),
    ("PG-10", r"CVE-\d{4}-\d+"),
    ("PG-07", r"\b(INC|CHG|RITM)\d+"),
    ("PG-01", r"\b\d{1,3}(\.\d{1,3}){3}\b"),
    ("PG-04", r"\b[A-Z]+\\[A-Za-z_]+|svc_"),
    ("PG-06", r"[0-9a-fA-F]{32,64}|[A-Za-z]:\\|/etc/|/var/"),
    ("PG-02", r"SRV-|DC01|-prod-|\.corp\.|\.local\b"),
]

notes = [json.loads(l) for l in open(NOTES, encoding="utf-8")]
gold = [json.loads(l) for l in open(GOLD, encoding="utf-8")]

for n, g in zip(notes, gold):
    if n["category"] != "pattern_gate_test":
        continue
    g["leak_rule"] = "UNTAGGED"
    for rule, rx in RULES:
        if re.search(rx, n["progress_note"]):
            g["leak_rule"] = rule
            break

with open(GOLD, "w", encoding="utf-8") as f:
    f.writelines(json.dumps(g) + "\n" for g in gold)

print(sorted(Counter(g.get("leak_rule") for g in gold if g.get("leak_rule")).items()))
