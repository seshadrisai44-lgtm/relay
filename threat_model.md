Project Relay — Threat Model

1. Project Purpose

Project Relay processes weekly project status notes while protecting sensitive client information.

2. Assets to Protect

- Weekly status notes
- Client-sensitive information
- API keys and credentials
- Project records and proposed changes
- Audit logs

3. Potential Threats

Threat| Possible Impact| Planned Security Control
Sensitive information appears in a note| Information exposure| Pattern gate and model gate
A gate fails or gives an uncertain result| Unsafe information may continue| Fail-closed behavior
An unapproved change is written back| Incorrect or unauthorized update| Human approval before write-back
An API key is accidentally committed| Credential exposure| Secret scanning
Audit records are missing| Difficult to investigate actions| Audit logging

4. Trust Boundaries

- The consultant enters a weekly note.
- The pattern gate checks the note locally.
- The model gate checks for sensitive information based on meaning.
- Only notes that pass the required checks may continue.
- Proposed changes require human approval before write-back.

5. Prototype Safety

- Use synthetic sample data.
- Do not connect to real client laptops or networks.
- Do not include real client information or real secrets in tests.
- Stop processing when a required security check fails or is uncertain.

6. Verification Plan

Each security control must be tested separately. Record the test input, expected result, actual result, and pass/fail status. Do not mark a test as passed until it has been run and its result verified.
