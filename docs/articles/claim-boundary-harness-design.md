# Claim Boundary Harness: A Meta-First Governance Layer For Coding Agents

Coding agents are getting better at editing files, running tests, and calling tools. The more practical problem is not that they fail openly. It is that they can turn weak evidence into confident claims: a partial run becomes "validated", a mocked check becomes "tested", a stale memory becomes current context, or a host hook is described as hard enforcement even though the runtime can bypass it.

Claim Boundary Harness is a small reference framework for that boundary. It is not a new agent runtime. It is a meta-first governance layer that can be adapted into agents that read workspace instructions, run local scripts, call hooks, or use wrapper/tool-proxy paths.

The framework focuses on four linked problems:

- claim verification: stop weak evidence from being reported as strong validation;
- project-scoped memory lanes: avoid cross-project memory bleed and context-compression loss;
- receipt-based risk routing: decide which gates are needed before opening large context;
- deployment realism: separate advisory guidance from actual hook, wrapper, tool-proxy, or sandbox enforcement.

## The Failure Mode

Many coding-agent failures are not caused by a missing tool. They are caused by a missing boundary before tool use or final reporting.

Common examples:

- The agent edits code before deciding whether the task is a simple fix, an experiment, a public-docs change, or a high-risk action.
- The agent reads the wrong memory lane because there is no project or conversation boundary.
- The agent says a result is "validated" after one smoke check, a mock-only run, or a failed partial execution.
- The agent claims a hook is hard enforcement even though the host runtime can still execute through a bypass path.
- The agent searches the web too late, or not at all, when the task depends on current versions, GitHub repositories, public APIs, prices, policies, or release notes.
- The agent keeps turning every useful lesson into a new skill, eventually making routing less predictable.

Claim Boundary Harness treats those as routing and evidence-boundary problems, not only prompt-writing problems.

## Design Principle: Meta First, Payload Later

The framework uses a cheap outer decision layer before opening expensive or risky context.

```text
user request
-> L0 microkernel
-> intake router
-> routing receipt
-> one matching gate or index
-> only the needed payload
-> final claim boundary review
```

The goal is not to make every task heavy. Ordinary chat should stay cheap. The router decides whether the task needs project instructions, memory, external research, claim checking, a skill matrix, or a runtime hard gate.

This is why memory retrieval is meta-first:

```text
memory summary or _META_INDEX
-> category index or outer retrieval surface
-> one matching capsule or paired record
```

The agent should not scan all memory files just because memory exists. It should find the smallest relevant capsule and stop.

## Routing Receipts

The core decision object is a routing receipt. It can stay internal for low-risk work, but it gives adapters a concrete contract.

Representative fields include:

```text
task_type
target_surface
audience
project_lane
risk_level
semantic_ambiguity
module_need
memory_need
memory_mode
memory_lane
record_intent
external_need
claim_risk
projectization_decision
conversation_memory_decision
link_intent
receipt_profile
required_gates
```

These fields are intentionally operational. They answer questions like:

- Is this public documentation, local harness maintenance, a project-memory update, a tool call, or a git action?
- Is the audience a public user, a local maintainer, a project operator, or only the current chat?
- Does this task require memory at all?
- If memory is needed, which lane owns it?
- Does this claim need evidence before it is reported?
- Does a hook need to stop execution, or is a compact advisory receipt enough?

## R0-R5 Risk Routing

The risk model is additive. If a task matches several categories, the highest risk and the union of gates should survive.

```text
R0 ordinary chat
R1 read-only local inspection
R2 reports, handoffs, and documentation artifacts
R3 code, config, governance, routing, trigger, or framework behavior changes
R4 experiments, runtime claims, current facts, external mechanisms, or performance work
R5 delete, submit, publish, install, login, payment, permission, network/proxy, sensitive transfer, or long-term memory writes
```

R0-R5 does not need to be shown to the user every time. The classification can stay silent by default. It should become visible only when it changes the execution path, cost, risk, permission requirement, memory behavior, search requirement, or final claim wording.

## Claim Boundaries

The framework separates artifact existence from truth claims.

For example:

- A file exists: artifact claim.
- A script ran once: execution claim.
- A smoke check passed: narrow validation claim.
- A benchmark is stable: stronger claim that needs repeated evidence.
- A public mechanism was read online: source-prior, not local validation.

The final answer should not promote weak evidence into a stronger class. A local smoke check is useful, but it is not the same as broad production validation. A public benchmark in another repository can inform design, but it does not prove the adapter works in a new host runtime.

## Memory Lanes

The framework uses separate memory lanes to avoid silent contamination.

Common lanes:

- project memory: owned by one project;
- conversation memory: isolated for a long-running projectless thread;
- referenced conversation memory: read through explicit links;
- common error corpus: repeated operational mistakes and their fixes;
- self-reflection matrix: higher-impact paired error and solution records;
- global archive: optional cold index, not active memory by default.

New conversations should continue old conversations through link-only edges by default. They should not mutate old conversation memory unless the user explicitly asks for a merge or update. Explicit merges should create a new merged memory with provenance rather than silently rewriting the old lane.

## Why Not Wrap Every Tool Call?

Hard runtime enforcement is only hard where the host runtime invokes it and honors the blocked result.

For example:

```python
decision = harness.runtime_enforcer(...)
if decision["status"] == "blocked":
    raise SandboxBlocked(decision["blocked_reasons"])
```

If the host runtime never calls the enforcer, or if another tool path bypasses the hook, that path remains advisory.

Claim Boundary Harness therefore recommends a split:

- use the control plane for every nontrivial task;
- keep ordinary tasks cheap with compact receipts;
- use hard gates only for critical boundaries such as R5 actions, high-risk tools, long-term memory writes, unresolved conversation links, or strong final claims;
- document bypass surfaces instead of pretending they do not exist.

## Why The SkillOpt-Style Layer Is Default-Off

The project includes a SkillOpt-style training layer, but it is not an always-on self-improvement loop.

It should be used only for:

- recurring skill or router improvements;
- candidate rule edits;
- rejected-edit review;
- textual learning-rate limits;
- slow updates;
- external skill-optimization mechanism intake.

It should not be used for ordinary chat, one-off fixes, direct memory writes, external fact checks, runtime enforcement, or claim gating. Those belong to the router, memory gate, research gate, runtime gate, or claim gate.

This boundary matters because uncontrolled skill generation can pollute project boundaries and make routing less predictable. The optimizer is subordinate to the existing skill matrix. It drafts candidate edits and gate reports; it does not directly mutate primary routers or claim local validation without evidence.

## Deployment Pitfalls

The current public repository includes deployment playbooks because the implementation details matter.

Examples of real failure classes the framework tries to make visible:

- an instruction file exists but the agent never loads it;
- a pre-tool hook returns `blocked`, but the host still executes the command;
- a prompt-stage hook does not preserve the original user task, so later tool checks lose context;
- a file-edit tool is blocked because the file content mentions a dangerous command in documentation;
- a current GitHub or release claim is made without external search;
- a conversation continuation reads the wrong memory;
- a final answer says "validated" without a matching evidence schema;
- a hook fails on non-ASCII or malformed surrogate payloads;
- Windows PowerShell reads JSON with the wrong encoding;
- a client update changes paths, launchers, hook behavior, or bundled runtimes.

The key rule is simple: do not call a deployment "hard enforced" until the covered execution path has a smoke test proving that a blocked decision actually stops execution.

## Local Reproduction Snapshot

The public repository includes lightweight checks rather than a full production test matrix.

At the time this article was added, the maintained smoke checks included:

- WorkBuddy-oriented Python adapter tests: `41 tests OK`;
- embedded harness policy validation: `status: pass`;
- JSON/JSONL parse check across repository examples;
- `git diff --check` for formatting regressions;
- public-sensitive-string scan for accidental local/private leakage.

These checks are narrow. They show that the reference package is internally consistent on the checked environment. They do not prove universal compatibility with every agent client, operating system, hook schema, or production workflow.

## What This Framework Is Not

Claim Boundary Harness is not:

- a replacement agent runtime;
- a universal sandbox;
- a guarantee that an agent cannot bypass instructions;
- a production-certified memory system;
- a claim that Codex, Claude Code, WorkBuddy, Hermes, or any other host is fully supported without local adaptation;
- an always-on optimizer that rewrites its own skills.

It is a reference framework for building a small, auditable governance path around coding agents.

## Suggested Listing Description

For curated lists, a compact description is:

> Claim Boundary Harness - A meta-first governance harness for coding agents that focuses on claim verification, project-scoped memory lanes, R0-R5 risk receipts, and adapter deployment playbooks. Reference framework with local Codex and WorkBuddy-oriented smoke checks; not a production-validated universal runtime.

## Repository

- GitHub: https://github.com/qimen039-code/claim-boundary-harness
- License: MIT
