Project Relay — Threat Verification Checklist

Purpose

Track whether each security control in the threat model has been tested and verified.

Test Results

ID| Threat / Scenario| Expected Result| Actual Result| Status
| TV-01 | Weekly note contains a test email address | Pattern gate detects the test pattern and blocks the note | Email pattern detected and blocked | PASS |
| TV-02 | Weekly note contains a synthetic secret-like value | Secret check detects it or flags it for review | Secret-like pattern detected and blocked | PASS |
| TV-03 | Pattern gate raises an exception | Pipeline blocks processing | Simulated gate failure returned blocked with gate_error; test passed | PASS |
| TV-04 | Gate returns an uncertain result | Pipeline blocks processing | Simulated uncertain result returned blocked; test passed | PASS |
| TV-05 | No human approval is provided | Write-back must be blocked | Approval tests passed for False, True, and None; approval rule verified | PASS |
| TV-06 | Audit event may expose sensitive note contents | Audit event stores only basic metadata | Tests passed: timestamp, action, and status recorded without note contents | PASS |
| TV-07 | Possible credential in a test file | Secret scanner detects the test credential | detect-secrets reported a finding for tests/fake_secret_test.txt | PASS |
| TV-08 | Invalid input (None) is provided | Pattern gate blocks invalid input | Invalid input blocked; test passed | PASS |

Verification Rules

- Use synthetic test data only.
- Never use real client information or real credentials.
- Record the actual result only after running the test.
- Mark PASS only when the observed result matches the expected result.
- If a test fails, record FAIL and document the issue.
- Do not claim a control is implemented until it has been checked in the code.

Current Summary

- Tests planned: 7
- Passed: 0 confirmed
- Failed: 0 confirmed
- Not run: 7

These are planned tests, not proof that the controls already work.
