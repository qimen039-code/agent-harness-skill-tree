---
name: agent-error-memory
description: Empty template for paired agent error memory. Use to record agent-caused execution, diagnosis, safety, routing, or process failures after they are solved and ready for reuse.
---

# Agent Error Memory

This file starts empty by design. Add real records only after a solved incident.

## Pairing Rule

- Error records live here.
- Solution records live in `bug-solution-memory`.
- Each error point must include `paired_solution_ids`.
- Do not hide agent-caused failure inside a success note.

## Error Point Index

| Error ID | Outer retrieval surface | Paired solution |
| --- | --- | --- |
| `ERR-EXAMPLE-YYYY-MM-DD` | example trigger words | `SOL-EXAMPLE-YYYY-MM-DD` |

## Error Point Template

```text
## ERR-EXAMPLE-YYYY-MM-DD

status:
point_kind: agent_error_solid_point
purpose_anchor:
meaning_anchor:
outer_retrieval_surface:
event_summary:
agent_fault:
why_it_was_wrong:
impact:
evidence:
applicable_boundaries:
non_applicable_boundaries:
risk_failure_conditions:
paired_solution_ids:
prevention_rule:
not_to_repeat:
```
