---
name: bug-solution-memory
description: Empty template for paired bug/problem solution memory. Use to record investigation order, fix path, rollback, validation, caveats, and reuse rules for solved incidents.
---

# Bug Solution Memory

This file starts empty by design. Add real solution records only after the corresponding incident is understood.

## Pairing Rule

- Solution records live here.
- Agent error records live in `agent-error-memory`.
- Each solution point must include `paired_error_ids`.

## Solution Point Index

| Solution ID | Outer retrieval surface | Paired errors |
| --- | --- | --- |
| `SOL-EXAMPLE-YYYY-MM-DD` | example solution trigger words | `ERR-EXAMPLE-YYYY-MM-DD` |

## Solution Point Template

```text
## SOL-EXAMPLE-YYYY-MM-DD

status:
point_kind: bug_solution_solid_point
purpose_anchor:
meaning_anchor:
outer_retrieval_surface:
problem_class:
solution_summary:
investigation_order:
fix_path:
rollback:
validation:
caveats:
applicable_boundaries:
non_applicable_boundaries:
paired_error_ids:
future_reuse_rule:
references:
```
