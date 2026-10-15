# Project Relay Evaluation Report

**Read this first:** the model gate and extraction are keyword and rule stand-ins, not real models. Only the pattern-gate row is a real result. Soft-leak, false-positive, injection and extraction rows must be rerun once an OpenAI key is available.

| Key result | Target | Measured | Status |
|---|---|---|---|
| Pattern leaks blocked | 30 of 30 | 30 of 30 | MET (real) |
| Soft leaks blocked | 9 of 10 | 10 of 10 | stand-in |
| Clean notes wrongly blocked | 10% or less | 0.0% | stand-in |
| Injection notes producing a bad op | 0 of 10 | 0 of 10 | stand-in |
| Extraction field accuracy | 90% or more | not measured | needs real model |
| Ops approved without edits | 80% or more | not measured | needs lead review data |
| Digest numbers match hand calculation | 100% | digest unit test | MET |
| Time to submit a note | under 5 min | not measured | needs 3 volunteers |
| Audit chain verifies | intact | intact | MET |
