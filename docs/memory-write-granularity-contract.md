# Memory Write Granularity Contract

Reusable memory should be compact, but it must not become ambiguous. A memory
capsule that survives outside the current context needs enough local context to
remain understandable without rereading the full conversation.

## Core Rule

Every durable memory item should contain a context-complete statement:

```text
actor or source
-> action, claim, decision, or observed event
-> object and scope
-> time anchor or version when relevant
-> evidence/provenance boundary
-> non-applicable boundary when it prevents misuse
```

Do not write isolated fragments such as "BM25 later", "adapter works", or
"memory issue fixed" as reusable memory. They are too short to route safely and
too easy to misread after context compaction.

## Router Integration

Write granularity is selected by the routing or dynamic decision layer after
`memory_mode` is known:

| Profile | Trigger | Write rule |
| --- | --- | --- |
| `none` | `memory_mode: none` or read-only memory lookup. | Do not create durable memory content. |
| `context_complete_required` | Any selected durable memory `write` or `update`. | The written item must include enough actor/source, action or decision, object/scope, time/version when relevant, and provenance boundary to stand alone. |
| `strict_capsule_required` | Explicit reusable memory, conversation-memory, or cross-conversation memory write. | Use source-preserving capsule shape, preserve `derived_from`, and reject orphan fragments or ledger summaries as fact sources. |

This profile constrains the shape of a memory write. It does not authorize a
memory write by itself and does not override lane isolation or R5 confirmation
requirements.

## Structure And Content Language

Use English for stable structure and code-facing fields:

```text
memory_id
source_tag
belief_status
confidence
derived_from
retrieval_terms
domain_tags
source_monitoring
lifecycle
```

Preserve the original language for the content plane. Chinese source content
should remain Chinese. English source content should remain English. Do not
translate or normalize memory content only to make it look uniform.

Recommended content-plane fields for reusable semantic memory:

```json
{
  "content": {
    "language": "zh-CN",
    "original_text": "维护者在 2026-06-26 明确决定，某记忆框架的检索策略应保持元摘要先行，并且混合检索只能作为候选集内的增强通道。",
    "context_complete_summary": "2026-06-26 的检索策略更新要求先通过元摘要、lane、分类和来源状态缩小候选集，再使用原文关键词、中文字符 n-gram、英文术语或可选词法排序增强召回；这些增强不能替代元摘要先行规则。",
    "key_terms": [
      "元摘要先行",
      "混合检索",
      "候选集增强"
    ],
    "non_applicable_boundary": "This does not authorize opening all memory payloads, using a vector database as the memory core, or merging unrelated project lanes."
  }
}
```

`original_text` may be a short original-language restatement when the full
source is too long for the capsule. The complete source still belongs in a raw
log, ledger evidence reference, source note, or archive payload.

## Bad And Good Shapes

Bad reusable memory:

```text
BM25 can wait.
```

Good reusable memory:

```text
On 2026-06-26, the user decided that BM25 must not become the default memory
retrieval core for this framework. If it is considered later, it may only be an
optional lexical-rank adapter over a meta-first, source-preserving candidate
set, and it must not introduce a database, vector store, or confidence score.
```

Bad reusable memory:

```text
database direction invalid.
```

Good reusable memory:

```text
On 2026-06-26, the framework rule was clarified: SQL, SQLite, vector
databases, and database-centered semantic memory are not default core
directions for this framework's semantic memory. These mechanisms may appear
only as explicitly approved, non-semantic operational bookkeeping outside the
default memory contract.
```

## Promotion Boundary

Ledger capsules and compact route summaries may stay short because they are
navigation records. When a ledger summary is promoted into reusable semantic
memory, rewrite it into a context-complete memory capsule and preserve
`derived_from` links to the ledger segment, evidence refs, raw session line
window, artifact, or source note.

Do not let a route summary become the fact source. The capsule may make the
fact findable; the evidence boundary still comes from source-monitoring fields
and `derived_from`.
