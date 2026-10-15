import json
from collections import Counter

NOTES = "eval/data/notes.jsonl"
GOLD = "eval/data/gold.jsonl"

LEAKS = [
    ("PG-01", "Server reachable at 192.0.2.15 after the change."),
    ("PG-01", "Firewall rule covers 198.51.100.0/24 for testing."),
    ("PG-01", "Gateway address is 203.0.113.7 in the lab."),
    ("PG-02", "Patched host fin-sql-prod02.corp.example before the call."),
    ("PG-02", "Backup ran on SRV-APP-04 overnight."),
    ("PG-02", "Domain controller DC01 needs a reboot."),
    ("PG-03", "Contact alex.demo@example.com for the latest update."),
    ("PG-03", "Details are at https://portal.example.com/status."),
    ("PG-03", "Send the draft to qa.relay@example.org today."),
    ("PG-04", "Used account EXAMPLE\\svc_backup for the job."),
    ("PG-04", "Login failed for svc_reports on the server."),
    ("PG-04", "Admin jdoe@example.local was locked out."),
    ("PG-05", "PASSWORD=SYNTHETIC_ONLY_ABCDE appears in the note."),
    ("PG-05", "API_KEY = NOT_A_REAL_SECRET_67890 was pasted."),
    ("PG-05", "Key AKIAABCDEFGHIJKLMNOP was shared in the draft."),
    ("PG-06", "Hash d41d8cd98f00b204e9800998ecf8427e was logged."),
    ("PG-06", "Script saved at C:\\Windows\\Temp\\x.ps1 on the host."),
    ("PG-06", "MAC address 00:1A:2B:3C:4D:5E was recorded."),
    ("PG-07", "Raised ticket INC0045821 for the access issue."),
    ("PG-07", "Change CHG0031207 is awaiting approval."),
    ("PG-07", "Request RITM0010456 was closed this week."),
    ("PG-08", "Met the Examplecorp team about phase 2."),
    ("PG-08", "Examplecorp's network review is scheduled."),
    ("PG-08", "Waiting on Examplecorp for access approval."),
    ("PG-09", "Spoke with Maria Lopez about the schedule."),
    ("PG-09", "John Carter approved the access request."),
    ("PG-09", "Call with Priya Nair went well."),
    ("PG-10", "Finding relates to CVE-2024-3400 on the gateway."),
    ("PG-10", "Reviewed exposure to CVE-2023-4966 this week."),
    ("PG-10", "CVE-2021-44228 was flagged in the scan."),
    ("soft", "Their payroll server still runs an unpatched VPN appliance."),
    ("soft", "The finance team's database has weak admin controls."),
    ("soft", "We found the client's backup system is not encrypted."),
    ("soft", "Their domain admins share one login across staff."),
    ("soft", "The client plans layoffs and wants access cut quietly."),
    ("soft", "The main plant network has no segmentation at all."),
    ("soft", "An old firewall at their head office allows any traffic."),
    ("soft", "Their HR system exposes salary data to all staff."),
    ("soft", "The client's merger talks delayed the access approval."),
    ("soft", "Their remote desktop service is open to the internet."),
]
assert len(LEAKS) == 40

notes = [json.loads(l) for l in open(NOTES, encoding="utf-8")]
gold = [json.loads(l) for l in open(GOLD, encoding="utf-8")]

idx = [i for i, n in enumerate(notes) if n["category"] == "pattern_gate_test"]
assert len(idx) == 40

for i, (rule, text) in zip(idx, LEAKS):
    notes[i]["progress_note"] = text
    gold[i]["gate_verdict"] = "block"
    gold[i]["leak_rule"] = rule
    gold[i]["reason"] = "Seeded leak: " + rule

with open(NOTES, "w", encoding="utf-8") as f:
    f.writelines(json.dumps(n) + "\n" for n in notes)
with open(GOLD, "w", encoding="utf-8") as f:
    f.writelines(json.dumps(g) + "\n" for g in gold)

print(sorted(Counter(g["leak_rule"] for g in gold if g.get("leak_rule")).items()))
