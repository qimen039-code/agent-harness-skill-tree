# Content Reading Contract

Retrieval and reading are related, but they are different operations.

Retrieval selects a candidate lane, file, record, or snippet. Reading consumes
that selected source with enough source-local context to support or downgrade a
claim.

## Required Reading Chain

```text
selected candidate from meta-first retrieval
-> source-shape identification
-> structure map or no-map fallback
-> source context header
-> bounded evidence window
-> context-completeness check
-> middle-safe evidence layout when multiple windows or long sources are involved
-> targeted expansion only when needed
-> unread-zone and verification-debt note
```

This contract does not introduce vector stores, databases, prompt-compression
models, small local classifiers, or automatic whole-file reading.

## Routing And Trigger Profiles

The route and decision layer should select the smallest reading profile that can
support the task. Do not enable every reading strategy for every source read.

Recommended routing fields:

```text
reading_need: none | candidate_read | evidence_read | strong_claim_read | full_audit
reading_profile: baseline | evidence_window | middle_safe | full_audit
source_shape: markdown | json | jsonl | code | raw_session | test_output | web | unknown
source_length: tiny | normal | long | huge
source_structure: mapped | partially_mapped | unmapped
evidence_need: none | local_context | exact_wording | multi_hop | strong_claim
position_risk: none | low | middle_sensitive | unresolved_middle
```

### Always-On Baseline

Use this for any nontrivial source read:

| Strategy | Trigger | Cost boundary |
| --- | --- | --- |
| Source-shape identification | Always for nontrivial reads. | May be a tiny sample for unknown files. |
| Retrieval-reading boundary | Always when retrieval selected the source. | A snippet or score never counts as having read the source. |
| Native reading unit | Always when a source shape is known. | Read a heading block, object, record, symbol, raw line window, or error block instead of arbitrary fragments. |
| Structure map first | Mandatory when a map/index exists and is cheap. | If no map exists, use no-map fallback; do not fabricate a durable map. |
| Source context header | Mandatory for windows that may support a claim. | Can be omitted for purely exploratory scratch reads. |

### Conditional Evidence Profile

Use this when the answer, patch, memory, report, or decision will rely on the
opened source:

| Strategy | Trigger |
| --- | --- |
| Progressive evidence window | Source content will support or limit a claim. |
| Context-completeness check | The claim needs subject, action, object/scope, time, version, or provenance. |
| Targeted expansion | The first window is missing a required boundary. |
| Unread-zone note | The source is only partially read and the unread area could affect the claim. |
| Verification-debt note | Exact wording, test coverage, external currentness, or linked evidence remains unresolved. |

### Strong-Claim And Middle-Safe Profile

Use this only when the task has higher claim risk or evidence complexity:

| Strategy | Trigger |
| --- | --- |
| Evidence inventory plus original-window dual anchor | Two or more evidence windows, public-facing statement, memory promotion, release note, or R4/R5 decision. |
| Segment conclusion cards | Three or more windows, conflicting windows, multi-step reasoning, or long raw sessions/logs. |
| Key evidence reminder | Strong final claim, memory promotion, release note, or evidence far from the final answer. |
| Multi-hop adjacency | One claim depends on several linked pieces of evidence. |
| Position risk marker | Long, sequential, dense, or sparsely read source where middle-only facts could matter. |
| Bounded middle reread gate | Head/tail or sparse windows are insufficient for fact, scope, time, or relevance, and the result would otherwise become a strong claim. |

### Full Audit Profile

Use this only when the user asks for a full audit, migration, cleanup,
backfill, or exhaustive verification. Full audit may read much broader source
areas, but it should still preserve source headers, unread boundaries for any
skipped zones, and claim limits.

## Source-Shape Identification

Before reading deeply, identify the source shape and choose a native reading
unit:

| Source shape | Preferred first read | Evidence window |
| --- | --- | --- |
| Markdown or text manual | Headings, nearby anchors, table of contents when present | Heading block plus adjacent paragraph only when needed. |
| JSON | Top-level keys and the selected complete object | Complete object, not a partial line fragment. |
| JSONL | Matching record IDs, timestamps, or event kinds | Selected record plus bounded adjacent records when sequence matters. |
| Code | File map, symbol names, imports, or test names | One function, class, config block, or call chain segment. |
| Raw session log | Session/turn/segment/evidence ref index | Selected raw line window with small before/after margin. |
| Test or command output | Failing test name, exit code, traceback anchor | Error block plus the command/context line that produced it. |
| Web or external source | Title, publisher, date, section heading | Relevant section with source URL and date. |

If the source shape is unknown, read only a small sample to classify it, then
switch to the matching unit. Do not continue as a blind full-file scan unless
the user asked for a full audit or no smaller structure exists.

## Structure Map First, With No-Map Fallback

Prefer the smallest available structure map:

```text
_META_INDEX.md
_STATIC_KNOWLEDGE_INDEX.md
_LEDGER_INDEX.md
domain_index.json
table of contents
Markdown headings
JSON keys
JSONL record IDs
code symbol list
test names
```

Many useful sources do not have a separate map. In that case, create a temporary
micro-map from the source itself:

```text
file name + size
first visible heading or top-level key
selected line/record anchors
nearby heading/key/symbol boundary
known evidence refs or derived_from links
```

The micro-map is a reading aid, not a new memory record and not a fact source.

## Source Context Header

Every evidence window that may support a claim should carry a compact context
header:

```text
source_ref: path, URL, record_id, or evidence_ref
source_shape: markdown | json | jsonl | code | raw_session | test_output | web
anchor: heading, key, symbol, line range, turn_id, or timestamp
source_tag: optional source-monitoring value when known
belief_status: optional status when known
read_scope: exact object, heading block, function, line window, or section
unread_boundary: what adjacent area was not opened
```

The header adapts the chunk-context idea to this framework without requiring
embeddings, BM25, generated contextual chunks, or a database.

## Progressive Evidence Window

Start with the smallest window that preserves the native unit:

```text
Markdown -> one heading block
JSON -> one complete object
JSONL -> one complete record
code -> one symbol or config block
raw session -> selected evidence ref line window
test output -> failing block and command context
web -> one relevant section
```

Then check whether the window contains:

```text
subject or actor
action, claim, decision, error, or observation
object and scope
time, version, or environment when relevant
source or provenance boundary
non-applicable boundary when needed
```

If any required context is missing, expand only the missing boundary: previous
heading, following paragraph, referenced definition, adjacent JSONL record,
linked `derived_from`, `evidence_refs`, import, call site, fixture, or command
line.

## Middle-Safe Evidence Layout

Long contexts can make decisive middle evidence easier to miss. This contract
does not try to solve the model's internal attention behavior. It reduces the
risk by changing how evidence is selected, anchored, and reviewed.

Use these rules when multiple evidence windows, long files, raw sessions, long
logs, or multi-hop claims are involved:

```text
evidence_inventory first
-> original evidence windows with source context headers
-> per-window conclusion cards
-> synthesis from conclusion cards and cited windows
-> key evidence reminder near the final claim
```

### Evidence Inventory Plus Original-Window Dual Anchor

Before analysis, create a compact evidence inventory:

```text
E1: source_ref + anchor + claim_scope + read_scope + unread_boundary
E2: source_ref + anchor + claim_scope + read_scope + unread_boundary
```

Then keep the original evidence windows available with their context headers.
The inventory is a navigation anchor; the original window remains the evidence.

### Segment Reading, Segment Conclusion, Then Synthesis

For several windows, do not immediately synthesize from raw snippets. Read each
window into a small conclusion card:

```text
evidence_id
local_claim
supports_or_limits
source_ref
unread_boundary
verification_debt
```

Only synthesize after the individual cards are available. This prevents a later
window from overwriting or blurring a weaker earlier boundary.

### Repeat Key Evidence Near The Question Or Claim

When making a strong answer, repeat only a short key-evidence reminder near the
question or final claim:

```text
final evidence reminder: E1 and E3 support the claim; E2 is background only;
unread zone remains the rest of raw session.
```

Do not duplicate long source excerpts. The reminder is a pointer, not a new fact
source.

### Keep Multi-Hop Evidence Adjacent

When one claim requires several pieces of evidence, keep those windows or
conclusion cards adjacent as a cluster:

```text
claim A cluster: E1 -> E2 -> E3
claim B cluster: E4 -> E5
```

Do not rank windows globally in a way that splits one claim's evidence across
the prompt. For code and logs, preserve causal or chronological order inside
the cluster.

### Position Risk Marker And Middle Reread Gate

Use a position risk marker when a long source has been read only through a few
bounded windows:

```text
position_risk: none | low | middle_sensitive | unresolved_middle
head_tail_anchor: head_read=<range or record ids>; tail_read=<range or record ids>
middle_reread_required: true | false
middle_reread_reason: head/tail evidence insufficient, fact missing, relevance weak, or source likely has middle-only state
```

Head and tail anchors prove only that those zones were read. They do not prove
that the middle is irrelevant.

Set `middle_reread_required: true` when all of these hold:

- the source is long, sequential, or structurally dense;
- only head/tail or sparse windows have been read;
- the opened windows do not contain enough fact, scope, time, or relevance for
  the claim;
- the answer would otherwise become a strong claim, memory promotion, release
  note, R4/R5 decision, or public-facing statement.

When triggered, reread the middle with anchors rather than by blind scanning:

```text
use heading/key/symbol/record anchors near the missing fact
or term hits inside the middle span
or midpoint and quarter-point structural samples when no better anchor exists
-> open bounded middle windows
-> update position_risk and verification_debt
```

If the middle reread still does not find enough evidence, downgrade the claim or
keep `position_risk: unresolved_middle`.

## Unread Zones And Verification Debt

When a response uses bounded reading, it must not imply full-source coverage.
Track the remaining boundary explicitly:

```text
read: selected heading block and linked evidence ref
not_read: rest of file, unrelated record families, or full raw session
verification_debt: exact wording, full regression run, external currentness, or unresolved linked source
claim_limit: local to the opened window
```

Use unread-zone notes especially before:

- strong factual claims;
- memory promotion;
- public docs or release notes;
- R4/R5 decisions;
- external-source conclusions;
- cross-lane memory references.

If the unread zone could change the answer, downgrade the claim or keep reading
within the same progressive chain.

## Boundary With Retrieval

Hybrid retrieval may rank or filter candidates. Reading must still open and
inspect the selected source window. A retrieval score, generated summary,
ledger capsule, or route summary is not proof that the original source was
read.
