# Project Relay - Threat Model

## 1. Project Purpose

Project Relay processes weekly project status notes while protecting sensitive client information. Consultants write a short structured note on a firm device. Two gates check that the note is client-safe, an agent pipeline turns it into proposed task and OKR updates, and a human approves every change before anything is written.

The one rule: no agent, connector, or file transfer touches a client environment.

## 2. Assets to Protect

- Weekly status notes
- Client-sensitive information
- API keys and credentials (OpenAI key, Teams webhook URL)
- Client denylist
- Project records and proposed changes (tracker workbook)
- Audit logs

## 3. Trust Boundary

Client laptops hold all client data. Relay runs only in the firm environment and only sees what a consultant types fresh on a firm device. Text must pass the pattern gate and the model gate before it reaches extraction.

## 4. Potential Threats and Controls

| # | Threat | Possible Impact | Planned Security Control | Verified By | Owner |
|---|--------|-----------------|--------------------------|-------------|-------|
| 1 | Consultant pastes client data into a note | Client information exposure | Dropdown-first form, length caps, attestation checkbox, pattern gate and model gate, fail closed | Seeded-leak notes in the eval set | Gate and security engineer |
| 2 | Client data reaches OpenAI | Confidential data leaves the firm | Pattern gate runs locally before any API call, so only passed text is sent; retention terms confirmed before the pilot | Code review of call order; terms on file | Gate and security engineer |
| 3 | Prompt injection inside a note | Model follows attacker instructions and changes ops | Note sent as delimited data; strict JSON schema; op allowlist; scope checks; human approval | Injection notes in the eval set | Agent engineer |
| 4 | Model echoes unsafe text into a change set | Unsafe text reaches the tracker | Change-set text re-scanned by the pattern gate | Unit tests with echoed identifiers | Agent engineer |
| 5 | Gate fails, times out, or returns "unsure" | Unsafe note continues through the pipeline | Fail-closed behavior: any error, timeout, or non-safe verdict blocks the note | Gate unit tests for error and timeout paths | Gate and security engineer |
| 6 | Unapproved change is written back | Incorrect or unauthorized update | Human approval for every operation before write-back; idempotency keys | Review page tests; apply-twice test | App engineer |
| 7 | Teams messages expose detail | Client detail visible in chat | Cards carry engagement codes, counts, and links only; never note text or task titles | Review of card templates | Integration engineer |
| 8 | Spoofed or cross-engagement submissions | Wrong person submits or approves for an engagement | Submitter taken from the login session; registry check that the user is on the engagement; stub login now, Entra ID SSO in the pilot | Negative tests | App engineer |
| 9 | Workbook tampering or bad manual edits | Corrupted or falsified tracker data | Only Relay writes in the prototype; in the pilot, sheets protected except status columns and Graph access limited to one site (Sites.Selected) | Permission review before the pilot | Integration engineer |
| 10 | Interns paste real data into ChatGPT while building | Real client data enters a chat tool | Synthetic data only, in the repo and in chats; firm ChatGPT workspace only, never personal accounts | Repo scan for denylist terms; ground rules agreed on Day 1 | Eval and data lead |
| 11 | Tampering with audit history | Actions cannot be investigated | Hash-chained audit log with a daily anchor hash posted to Teams | Chain verification script | App engineer |
| 12 | Blocked text leaks through logs | Client data persisted in logs | Blocked text never written; logs keep rule IDs, offsets, and a salted hash only | Log inspection test | App engineer |
| 13 | Denylist exposure | Client names exposed | Encrypted at rest, read only by the gate process, never logged or sent to a model | Code review | Gate and security engineer |
| 14 | API key or webhook URL is leaked or committed | Credential exposure | Local .env in the prototype, firm vault in the pilot; never committed or pasted into chats | detect-secrets pre-commit hook | App engineer |

## 5. Data Retention

| Data | Kept For | Reason |
|------|----------|--------|
| Blocked note text | Never stored | Could contain client data |
| Passed note text | 90 days, then deleted | Needed only for review and debugging |
| ParsedNote and ChangeSet records | Engagement length plus 1 year | Reporting history |
| Audit log | 3 years | Auditability |

## 6. Out of Scope

- Anything that runs on, connects to, or reads from client laptops or client networks
- Timesheet or billing integration
- Auto-approval of any change
- Production hosting and SSO integration (the prototype uses stub login)

## 7. Sign-off (Gate 1)

| Role | Name | Date | Signature |
|------|------|------|-----------|
| Gate and security engineer | | | |
| Security reviewer | | | |
