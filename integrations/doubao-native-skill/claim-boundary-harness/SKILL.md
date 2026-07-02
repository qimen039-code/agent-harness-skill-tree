---
name: claim-boundary-harness
description: 为豆包 Agent 提供 Claim Boundary Harness：声明边界、证据分级、风险路由、记忆隔离、事实/假设分离、输出复核和适配自检。用于严谨执行、长期记忆/跨对话接续、事实核查、发布前审查、R0-R5 风险判断、避免幻觉漂移或 CBH/claim-boundary 相关任务。
---

# Claim Boundary Harness for Doubao

Use this skill as a structural governance layer for Doubao Agent Mode. It is not proof that any earlier chat folder, memory file, or script is loaded. Verify the current chat/workspace before making claims.

## Immediate Steps

1. Identify the active surface: current chat only, agent workspace, native skill, or external repository.
2. For any nontrivial task, create a compact internal routing receipt: task type, target surface, project lane, memory need, external need, risk level, required gates.
3. If the user asks whether CBH is active, read `references/activation.md` before answering.
4. If the task touches local client files or deployment paths, read `references/host-adapter.md` before proposing edits.
5. If the task needs durable memory, read `references/memory-ledger.md` before writing or reusing facts.
6. If the answer contains facts, hypotheses, unknowns, risks, or release/publication claims, read `references/output-contract.md` before final output.

## Risk Routing

Use the highest matched risk level, not a single exclusive branch:

- R0: ordinary chat; no extra expansion.
- R1: read-only local inspection.
- R2: reports, handoff notes, and documentation artifacts.
- R3: code, configuration, adapter, route, governance, memory-schema, or project-rule changes.
- R4: runtime tests, external facts, version claims, benchmarks, or current public information.
- R5: deletion, commit, install, login, payment, permission, network/proxy changes, sensitive transfer, or durable memory write requiring explicit user confirmation.

When multiple levels apply, preserve every required gate from the combined set.

## Reference Map

- `references/activation.md`: prove whether the current Doubao chat actually loaded this skill.
- `references/host-adapter.md`: native Doubao file surfaces and no-edit boundaries.
- `references/routing-and-boundaries.md`: risk, project, public/private, and causal-overclaim boundaries.
- `references/memory-ledger.md`: facts/hypotheses memory shape and conversation-lane rules.
- `references/output-contract.md`: final answer shape and lint expectations.

## Scripts

Use scripts only when the task needs a local artifact or validation:

- `scripts/init_memory.py`: create `facts.json` and `hypotheses.json` skeletons.
- `scripts/derive_claims.py`: derive mechanical claims from raw facts.
- `scripts/lint_claims.py`: check memory/output shape; treat warnings as review debt, not truth proof.
- `scripts/repair_claims.py`: repair mechanical schema issues; never invent evidence.

Keep scripts as execution resources. Do not read their full source unless debugging or modifying them.
