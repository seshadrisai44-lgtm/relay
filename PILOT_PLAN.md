# Project Relay: Pilot Plan

## Scope
- 2 to 3 consultants, 4 weeks
- Weekly structured note on a firm device only
- Engagement lead approves every change; nothing is auto-approved

## Prerequisites (all required before week 1)
1. OpenAI API key on the firm's account, with retention terms on file
   (including whether zero data retention is available)
2. Real model gate and real extraction replacing the stand-ins
3. Internal host for the Relay service
4. Entra ID single sign-on replacing the stub login
5. Microsoft Graph writes limited to one SharePoint site (Sites.Selected)
6. Teams channel and Workflows webhook (needs a Teams admin)
7. Security reviewer has signed threat_model.md and the gate results
8. Contracts checked: no client restricts even metadata (hours, milestone status)

## Success criteria (rerun with real models)
| Result | Target |
|---|---|
| Pattern leaks blocked | 30 of 30 |
| Soft leaks blocked by model gate | 9 of 10 or better |
| Clean notes wrongly blocked | 10% or less |
| Injection attempts that change any op | 0 of 10 |
| Extraction field accuracy | 90% or more |
| Ops approved without edits | 80% or more |
| Digest numbers match the database | 100% |
| Time to submit a note | under 5 minutes |
| Audit chain verifies | intact |

## Rollback
1. Switch the note form off
2. Make the tracker workbook read-only
3. Keep the audit log (3 years)
4. Delete stored note text older than 90 days, or all of it if requested

## Known gaps (prototype)
- Model gate and extraction are keyword and rule stand-ins
- Teams card is a terminal stub; no live webhook yet
- 90-day note-text delete job not built
- Daily audit anchor hash not posted to Teams
- Ops-approved-without-edits and time-to-submit not yet measured

## Gate 2 decision
**No-go until the OpenAI key, real model results and security sign-off are in place.**
Prototype status: pattern gate, review flow, workbook write-back, digest and
audit chain are working on synthetic data only.
