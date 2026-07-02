# Routing And Boundaries

## Routing Receipt

For nontrivial work, maintain a compact internal receipt:

```text
task_type
target_surface
project_lane
risk_level
memory_need
memory_lane
external_need
claim_risk
required_gates
```

Expose the receipt only when useful, when boundaries are ambiguous, or when the user asks.

## Project And Memory Isolation

Default to the current chat or current project lane. Do not mix memories across unrelated projects.

Only link lanes when the user explicitly asks for continuation, merge, backfill, or cross-project migration.

If the user asks to continue a previous long conversation, create or update the current conversation lane and link it to the previous lane; do not silently overwrite the older lane.

## External Evidence

Use external search or official sources when the task depends on current versions, public mechanisms, policy, price, law, GitHub state, open-source behavior, or unfamiliar external claims.

If external evidence was not checked, mark the claim as unverified instead of treating internal reasoning as proof.

## Causal Attribution

Before final output, downgrade overbroad causal statements:

- mechanism_property: structural rule of the framework itself.
- empirical_record: local observation, case, or history; must carry scope.
- causal_hypothesis: plausible cause without controlled validation.
- validated_causality: controlled, reproducible evidence.

Local observations and examples do not prove global causality.
