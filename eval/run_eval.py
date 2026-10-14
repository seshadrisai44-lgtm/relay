import csv
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "data" / "project_relay_synthetic_120_notes.csv"
REPORT_FILE = BASE_DIR / "report.md"


def main():
    if not DATA_FILE.exists():
        print(f"Dataset not found: {DATA_FILE}")
        return

    with DATA_FILE.open("r", encoding="utf-8-sig", newline="") as file:
        rows = list(csv.DictReader(file))

    report = [
        "# Project Relay Evaluation Report",
        "",
        f"- Dataset: `{DATA_FILE.name}`",
        f"- Total rows: {len(rows)}",
        "- Status: Dataset loaded successfully.",
        "",
        "> This checks dataset loading only. It does not measure prediction accuracy.",
    ]

    REPORT_FILE.write_text("\n".join(report) + "\n", encoding="utf-8")

    print(f"Dataset rows loaded: {len(rows)}")
    print(f"Report saved to: {REPORT_FILE}")


if __name__ == "__main__":
    main()
