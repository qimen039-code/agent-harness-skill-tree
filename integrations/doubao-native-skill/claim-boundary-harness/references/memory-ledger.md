# Memory And Ledger Contract

## Fact/Hypothesis Split

Use `facts.json` only for statements with direct evidence. Use `hypotheses.json` for plausible but unverified explanations, predictions, or diagnoses.

Do not use hypotheses as premises for validated claims.

Do not hand-fill derived facts. Generate derived records from raw facts with scripts or keep them absent.

## Context-Complete Writes

Every durable memory item must include enough subject, action, object, scope, source, and time context to remain meaningful outside the original chat.

Reject orphan fragments such as "this was fixed" or "router problem" unless the record states what was fixed, where, why, and how it was verified.

## Source Dependency

When a memory capsule depends on a source file, chat, report, or test, preserve `derived_from` or equivalent source pointers.

If the source becomes invalid, deleted, or superseded, downgrade dependent claims instead of allowing orphan evidence to remain validated.

## Lane State

Use lane states:

- active: can be read and written.
- frozen_readonly: can be inspected for audit but not used as default context or written to.
- cleared: source intentionally removed; derived claims must be reviewed.

Freezing is different from deletion.

## Feedback Loop

The memory -> prediction -> verification -> calibration loop is an internalized reuse pattern for selected reusable records. It is not a request to make public predictions on every task.

Use it when a prior mistake, prevention rule, or explicit user correction is selected as relevant. Treat predictions as hypotheses until verified.
