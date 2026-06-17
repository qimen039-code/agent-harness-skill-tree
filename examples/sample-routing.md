# Sample Task Routing

| Request | Expected Route | Why |
| --- | --- | --- |
| `summarize this short note` | R0 | ordinary response |
| `inspect the local config` | R1 | read-only local inspection |
| `write a handoff report` | R2 | durable artifact |
| `fix the parser script` | R3 | code or config change |
| `run benchmark after the fix` | R4 | runtime and verification work |
| `delete old files and commit` | R5 | high-risk action |

The route is additive. If one request contains both `fix` and `benchmark`, the result should include both R3 and R4 gate sets.
