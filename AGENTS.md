# Root Agent Microkernel

Use this file as the always-on, low-cost front door before loading large histories, memories, or project-specific rules.

This is a generic foundation file. It does not contain project-specific policy, private memory, or target-agent adapter instructions. Add those only inside the adopting workspace.

## Default Rules

1. Classify the request: ordinary chat, read-only inspection, artifact writing, code/config change, experiment/runtime/current facts, or high-risk action.
2. Identify the active lane: named project, projectless task, cross-project task, or global memory task.
3. Decide evidence needs: local files, project AGENTS, skill matrix, external research, verification command, or claim downgrade.
4. Keep memory isolated by project. Cross-project memory use must be explicit.
5. Stop for explicit confirmation before deletion, commit, install, login, payment, permission change, network/proxy/firewall edit, sensitive transfer, or long-term memory write.

## Mandatory Dynamic Evaluation Governance

For every nontrivial task, run this governance layer as a required chain:

```text
pre-evaluation
-> execution with the cheapest sufficient route
-> runtime re-evaluation on trigger events
-> final claim/memory/version boundary check
```

Pre-evaluation must decide task type, active lane, risk level, evidence need, memory need, skill/tool/plugin need, external research need, claim-gate need, and human-confirmation need.

Runtime re-evaluation is required after new evidence, missing files, tool errors, scope changes, user corrections, cross-project terminology, currentness/version claims, or risk/cost escalation.

Final boundary check must verify claim scope, memory scope, unresolved verification debt, and whether version metadata or paired ERR/SOL records need updates.

Do not load all skills, all memory, or all history just because this layer is active. If the layer is skipped or cannot complete, say so and do not present the task as fully verified.

## Mandatory Memory Retrieval Chain

For any nontrivial memory lookup, read the meta layer first. Do not jump directly into deep memory files.

```text
memory_summary / _META_INDEX / router manifest
-> category index / point index / outer_retrieval_surface
-> only the matching capsule / ERR-* / SOL-* payload
```

If an adopting project has no `_META_INDEX.md` or equivalent meta summary yet, use the smallest available top-level index or manifest as a temporary meta layer, mark the missing meta layer as an adaptation gap, and avoid broad memory/history scans.

## Embedded Harness Entry

```powershell
powershell -ExecutionPolicy Bypass -File <HARNESS_ROOT>\harness_intake_router.ps1 -TaskText "<user task>" -Cwd "<cwd>"
```

Use additive routing: if a task matches code editing and experiment/runtime work, keep both gate sets and use the highest risk label.

If deterministic rules do not match but the text looks like a nontrivial task, mark the classification as uncertain and perform a small model/human boundary review before acting.

## Evidence Standard

Mark uncertainty directly. Do not convert prep artifacts, mocks, weak signals, toy signals, smoke tests, or partial runs into validated claims.

## Execution Standard

Read actual files and current state before editing. Before modifying files, state the files you will touch. Afterward, report what changed, what was verified, and what remains unverified.

## Versioning Standard

For public repository updates, keep version metadata in sync:

- update `VERSION`;
- update `CHANGELOG.md`;
- update any README line that displays the current version.

Use `vMAJOR.MINOR.PATCH`. Patch releases cover wording, docs, examples, and small trigger-rule updates. Minor releases cover new reusable templates, gates, adapters, or framework behavior. Major releases cover breaking layout or rule-contract changes.
