import pytest

from gate.pattern_gate import check_note

# Every example is invented: documentation IPs, example.com, made-up names.
CASES = {
    "PG-01": (
        [
            "Server reachable at 192.0.2.15 after the change.",
            "Firewall rule covers 198.51.100.0/24 for testing.",
            "Gateway address is 203.0.113.7 in the lab.",
        ],
        [
            "Version 1.2.3 was released this week.",
            "Completed 12 of 30 tasks.",
            "Meeting moved to 10.30 today.",
        ],
    ),
    "PG-02": (
        [
            "Patched fin-sql-prod02.corp.example before the call.",
            "Backup ran on SRV-APP-04 overnight.",
            "Domain controller DC01 needs a reboot.",
        ],
        [
            "Finished the design review.",
            "The team moved to production planning.",
            "Reviewed the local onboarding checklist.",
        ],
    ),
    "PG-03": (
        [
            "Contact alex.demo@example.com for the latest update.",
            "Details are at https://portal.example.com/status.",
            "Send the draft to qa.relay@example.org today.",
        ],
        [
            "Sent the update by email.",
            "Followed up on the access request.",
            "Scheduled a call for Monday.",
        ],
    ),
    "PG-04": (
        [
            r"Used account EXAMPLE\svc_backup for the job.",
            "Login failed for svc_reports on the server.",
            "Admin jdoe@example.local was locked out.",
        ],
        [
            "Reviewed the service account process.",
            "Service desk handled the request.",
            "Account access was approved.",
        ],
    ),
    "PG-05": (
        [
            "PASSWORD=SYNTHETIC_ONLY_ABCDE appears in the note.",
            "API_KEY = NOT_A_REAL_SECRET_67890 was pasted.",
            "Key AKIAABCDEFGHIJKLMNOP was shared in the draft.",
        ],
        [
            "Reviewed the password policy.",
            "Discussed the secret management approach.",
            "Key milestone reached this week.",
        ],
    ),
    "PG-06": (
        [
            "Hash d41d8cd98f00b204e9800998ecf8427e was logged.",
            "MAC address 00:1A:2B:3C:4D:5E was recorded.",
            r"Script saved at C:\Windows\Temp\x.ps1 on the host.",
        ],
        [
            "Review finished at 10:30 today.",
            "Version abc123 was deployed.",
            "Notes saved in the shared folder.",
        ],
    ),
    "PG-07": (
        [
            "Raised ticket INC0045821 for the access issue.",
            "Change CHG0031207 is awaiting approval.",
            "Request RITM0010456 was closed this week.",
        ],
        [
            "Incident review completed.",
            "Change request approved this week.",
            "Raised a ticket for access.",
        ],
    ),
    "PG-08": (
        [
            "Met the Examplecorp team about phase 2.",
            "Examplecorp's network review is scheduled.",
            "Waiting on EXAMPLECORP for access approval.",
        ],
        [
            "Met the client team about phase 2.",
            "Example slide deck was reviewed.",
            "Corporate review scheduled.",
        ],
    ),
    "PG-09": (
        [
            "Spoke with Maria Lopez about the schedule.",
            "John Carter approved the access request.",
            "Call with Priya Nair went well.",
        ],
        [
            "Spoke with the team about the schedule.",
            "Maria joined the call.",
            "Priya shared the agenda.",
        ],
    ),
    "PG-10": (
        [
            "Finding relates to CVE-2024-3400 on the gateway.",
            "Reviewed exposure to CVE-2023-4966 this week.",
            "CVE-2021-44228 was flagged in the scan.",
        ],
        [
            "Reviewed the vulnerability scan process.",
            "Discussed the CVE tracking approach.",
            "Planning for 2024 started.",
        ],
    ),
}

POSITIVE = [(rule, t) for rule, (pos, _) in CASES.items() for t in pos]
NEGATIVE = [(rule, t) for rule, (_, neg) in CASES.items() for t in neg]


def test_three_positive_and_three_negative_per_rule():
    assert len(CASES) == 10
    for rule, (pos, neg) in CASES.items():
        assert len(pos) == 3 and len(neg) == 3, rule


@pytest.mark.parametrize("rule,text", POSITIVE)
def test_positive_is_blocked_by_its_rule(rule, text):
    result = check_note(text)
    assert result["allowed"] is False
    assert rule in result["findings"]


@pytest.mark.parametrize("rule,text", NEGATIVE)
def test_negative_is_not_blocked(rule, text):
    result = check_note(text)
    assert rule not in result["findings"]
    assert result["allowed"] is True
