# Project AGENTS Template

Replace placeholders before use.

## Project Boundary

- project_id: `EXAMPLE_PROJECT`
- root: `<PROJECT_ROOT>`
- memory roots: `<PROJECT_ROOT>/.agent-memory`, `<PROJECT_ROOT>/memory-bank`

## Execution Rules

- Read this file before nontrivial project work.
- Read only the memory/status files needed for the task.
- Keep project memory isolated unless the user explicitly requests cross-project synthesis.
- Before edits, state which files will be touched.
- After edits, report changes, verification, and unresolved risks.

## Evidence Labels

Use explicit labels such as `unverified`, `source_prior`, `prep_artifact`, `mock_only`, `weak_signal`, `toy_signal_positive`, `strong_candidate`, and `validated`. Do not overclaim.
