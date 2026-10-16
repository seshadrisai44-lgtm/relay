import json

import yaml

reg = {
    e["code"]: e
    for e in yaml.safe_load(open("registry/engagement.yaml", encoding="utf-8"))[
        "engagements"
    ]
}
notes = [json.loads(l) for l in open("eval/data/notes.jsonl", encoding="utf-8")]
gold = [json.loads(l) for l in open("eval/data/gold.jsonl", encoding="utf-8")]

for n, g in zip(notes, gold):
    if g["gate_verdict"] != "pass":
        continue
    e = reg[n["engagement_code"]]
    ops, kr = [], {}
    for m in n["milestones_done"]:
        ops.append({"op": "complete_task", "task_ref": m})
        k = e["kr_links"].get(m)
        if k:
            kr[k] = kr.get(k, 0) + 1
    ops += [{"op": "update_kr", "kr_id": k, "delta": d} for k, d in kr.items()]
    ops += [{"op": "create_task", "title": t} for t in n["next_week"]]
    ops += [{"op": "create_blocker", "summary": b} for b in n["blockers"]]
    if n["status"] == "red" or n["help_needed"]:
        ops.append({"op": "flag_for_lead"})
    g["parsed_note"] = {
        "milestones_done": n["milestones_done"],
        "tasks": n["next_week"],
        "blockers": n["blockers"],
    }
    g["changeset_ops"] = ops
    g["label_status"] = "draft, needs two reviewers"

with open("eval/data/gold.jsonl", "w", encoding="utf-8") as f:
    f.writelines(json.dumps(g) + "\n" for g in gold)
print(sum("changeset_ops" in g for g in gold), "notes labelled")
