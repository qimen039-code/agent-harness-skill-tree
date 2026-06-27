# Hybrid Memory Retrieval Contract

Hybrid retrieval in this framework means combining bounded lexical and
structural signals after the meta layer has selected a small candidate set. It
does not mean adopting a vector database, embedding store, SQL memory backend,
or always-on ranking service.

## Required Order

```text
memory_summary / _META_INDEX / router manifest
-> category index / point index / outer_retrieval_surface
-> lane, domain, time, source_tag, belief_status, and lifecycle filters
-> retrieval_terms, exact phrase, original-language keyword, Chinese character n-gram, and English term matching
-> optional lexical-rank adapter over the already bounded candidate set
-> matching capsule or ledger segment
-> derived_from / evidence_refs / raw source window only when needed
```

The first two steps are mandatory. Do not rank or scan deep payloads before the
meta surface has narrowed the lane and category.

## Router Integration

Hybrid retrieval is selected by the routing or dynamic decision layer after
`memory_need` is known:

| Profile | Trigger | Execution rule |
| --- | --- | --- |
| `none` | `memory_need: none` | Do not open memory. |
| `meta_first_hybrid_enhancement` | Any selected memory read where meta/index lookup is enough to bound candidates. | Run the existing meta-first path, then add retrieval terms, exact phrases, original-language keywords, Chinese character n-grams, English terms, and optional lexical ranking over the bounded candidate set. |
| `meta_first_hybrid_required` | Reusable capsules, ERR/SOL records, common-error records, conversation state, or memory links. | Treat the hybrid channels as part of the selected memory workflow, while still preserving lane/category filtering, source-monitoring, and claim gates. |

This profile increases recall inside the existing retrieval chain. It is not an
independent search stack, and it must not cover or replace the meta-first layer.

## Stage 1: Write For Retrieval

Stage 1 has no search dependency. It improves memory quality at write time:

- write context-complete memory content, not isolated fragments;
- preserve the original language in the content plane;
- keep English structure fields for machine stability;
- add `retrieval_terms`, `domain_tags`, time anchors, `source_tag`,
  `belief_status`, `confidence`, and `derived_from`;
- keep `non_applicable_boundary` when a memory could be over-applied.

If the memory is written well, cheap exact and term-based retrieval remains
useful even before any ranking adapter exists.

## Stage 2: No-Dependency Candidate Matching

Stage 2 uses local file/index reads only. A simple adapter can combine these
signals without creating a database:

| Signal | Purpose |
| --- | --- |
| `lane` / `memory_id` / `category` | Keep project and conversation boundaries intact. |
| `domain_tags` / `record_type` / `lifecycle` | Avoid opening irrelevant record families. |
| `source_tag` / `belief_status` | Keep evidence status visible during retrieval. |
| `retrieval_terms` | Route common bilingual or domain-specific aliases. |
| Exact phrase match | Preserve original-language wording and named terms. |
| Chinese character n-gram match | Catch short Chinese phrase overlap without translating content. |
| English term match | Preserve code, API, and architecture terms in their native form. |
| Time anchor match | Prefer the right decision window or continuation point. |

Return results with `score_method: none` unless a real ranking method computed a
numeric score. If a local lexical rank adapter exists, use a method name such as
`lexical_rank_adapter` or `bm25_adapter`. Do not call the score confidence.

## Optional BM25 Boundary

BM25 is not a default requirement. It may be considered later only as an
optional lexical-rank adapter when exact/term matching returns too many
candidates.

If adopted, BM25 must:

- run after meta-first lane/category filtering;
- rank original-language text without forcing translation;
- avoid a database or embedding backend as a default dependency;
- expose its value only as retrieval metadata, not truth or confidence;
- keep `source_tag`, `belief_status`, `confidence`, and `derived_from` intact;
- degrade cleanly to `score_method: none` when unavailable.

## Non-Goals

This contract does not introduce:

- SQL, SQLite, vector databases, or embedding stores as semantic-memory core;
- automatic cross-lane memory pooling;
- ranking-based claim validation;
- full history scans for ordinary lookup;
- translation-first memory normalization.
