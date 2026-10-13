Project Relay — Threat Verification Checklist

Purpose

Track whether each security control in the threat model has been tested and verified.

Test Results

ID| Threat / Scenario| Expected Result| Actual Result| Status
| TV-01 | Weekly note contains a test email address | Pattern gate detects the test pattern and blocks the note | Email pattern detected and blocked | PASS |
| TV-02 | Weekly note contains a synthetic secret-like value | Secret check detects it or flags it for review | Secret-like pattern detected and blocked | PASS |
TV-03| A required security gate fails| Processing stops; the note does not continue| Not tested yet| NOT RUN
TV-04| A security check returns an uncertain result| Processing stops for safety| Not tested yet| NOT RUN
TV-05| A proposed change has no human approval| Write-back is not performed| Not tested yet| NOT RUN
TV-06| Audit event is generated for a test action| The event records the action and outcome without exposing sensitive content| Not tested yet| NOT RUN
TV-07| A test credential is placed in a test file| Secret scanning flags it; no real credential is used| Not tested yet| NOT RUN
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
