# Conversation State

```yaml
memory_id: CONVERSATION_TEMPLATE
memory_type: conversation
lane: CONVERSATION_TEMPLATE
status: TEMPLATE
scope: one isolated long-running conversation or thread
title: Replace with a short title
created_at: YYYY-MM-DDTHH:MM:SS+00:00
updated_at: YYYY-MM-DDTHH:MM:SS+00:00
last_reviewed: YYYY-MM-DD
retrieval_terms: []
semantic_anchors: []
continues_from: []
merged_from: []
merged_into: null
link_policy: link_only_by_default
max_continuation_depth: 5
active_successor_memory_id: null
redirect_read_to: null
```

## Current Focus

Short summary of what this conversation is about.

## Durable Decisions

- No real decisions recorded yet.

## Open Loops

- No open loops recorded yet.

## Boundaries

- This lane is not project memory.
- This lane is not global memory.
- Cross-conversation writes require explicit user instruction.
- Continuing an older conversation uses link-only continuation by default.
- Merging conversations requires explicit user instruction and creates a merged memory record.

## Continuation Note

Read `_META_INDEX.md` first, then this file, then `memory_links.jsonl` or only the matching JSONL records.
