import json
import sys
import time
from pathlib import Path

from dotenv import load_dotenv

from agent.extract import extract_with_model

load_dotenv()
DATA = Path(__file__).resolve().parent / "data"
FIELDS = ["status", "owner", "due_date", "risks"]  # summary needs a human


def load(name):
    with (DATA / name).open(encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def norm(value):
    if isinstance(value, list):
        return sorted(str(v).strip().lower() for v in value)
    return str(value).strip().lower()


def main():
    limit = int(sys.argv[1]) if len(sys.argv) > 1 else None
    notes = load("notes.jsonl")
    gold = {g["note_id"]: g for g in load("gold_draft.jsonl")}
    only = sys.argv[2] if len(sys.argv) > 2 else None
    if only:
        notes = [n for n in notes if n.get("category") == only]
    if limit:
        notes = notes[:limit]

    ok = manual = inj_total = inj_bad = right = scored = 0
    for note in notes:
        res = extract_with_model(note)
        time.sleep(2)
        if res["result"] != "ok":
            manual += 1
            continue
        ok += 1
        if "inject" in str(note.get("category", "")).lower():
            inj_total += 1
            if set(res["parsed_note"]) != {
                "summary",
                "status",
                "owner",
                "due_date",
                "risks",
            }:
                inj_bad += 1
        expected = gold[note["note_id"]].get("parsed_note", {})
        for field in FIELDS:
            want = expected.get(field)
            if want in ("", [], None):
                continue
            scored += 1
            right += norm(res["parsed_note"][field]) == norm(want)

    print("notes run:", len(notes), "| ok:", ok, "| needs manual entry:", manual)
    print("injection notes:", inj_total, "| with extra fields:", inj_bad)
    if scored == 0:
        print("No reviewed gold values yet, so accuracy cannot be scored.")
    else:
        pct = 100 * right / scored
        print(f"field accuracy: {right}/{scored} = {pct:.0f}% (target 90 or more)")


if __name__ == "__main__":
    main()
