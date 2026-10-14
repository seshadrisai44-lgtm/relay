import csv
from pathlib import Path

from gate.pattern_gate import check_note


def test_synthetic_dataset():
    dataset = (
        Path(__file__).parent.parent
        / "eval"
        / "data"
        / "project_relay_synthetic_120_notes.csv"
    )

    with dataset.open(encoding="utf-8", newline="") as file:
        rows = list(csv.DictReader(file))

    assert len(rows) == 120

    correct = 0
    for row in rows:
        result = check_note(row["progress_note"])
        actual = "ALLOW" if result["allowed"] else "BLOCK"
        expected = row["expected_result"]

        if actual == expected:
            correct += 1

    print(f"\nDataset notes: {len(rows)}")
    print(f"Correct predictions: {correct}/{len(rows)}")
    print(f"Accuracy: {correct / len(rows) * 100:.1f}%")
