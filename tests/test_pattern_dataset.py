import json
from collections import Counter
from pathlib import Path

from gate.pattern_gate import check_note

DATA = Path(__file__).resolve().parent.parent / "eval" / "data"


def _leaks():
    notes = [json.loads(l) for l in open(DATA / "notes.jsonl", encoding="utf-8")]
    gold = [json.loads(l) for l in open(DATA / "gold.jsonl", encoding="utf-8")]
    return [
        (n, g["leak_rule"])
        for n, g in zip(notes, gold)
        if g.get("leak_rule", "").startswith("PG")
    ]


def test_each_rule_has_three_dataset_notes():
    counts = Counter(rule for _, rule in _leaks())
    assert counts == {f"PG-{i:02d}": 3 for i in range(1, 11)}


def test_all_30_dataset_leaks_blocked_by_their_own_rule():
    for note, rule in _leaks():
        result = check_note(note["progress_note"])
        assert result["allowed"] is False, note["note_id"]
        assert rule in result["findings"], (note["note_id"], rule)
