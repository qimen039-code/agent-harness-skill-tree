# Examples

## Example 1: Mixed Code And Benchmark Task

Input:

```text
fix the script and run benchmark
```

Expected route:

- risk label: `R4`;
- triggered risks: `R4`, `R3`;
- required gates include change contract, claim gate, external research gate, and verification gate.

## Example 2: Vague Project Task

Input:

```text
handle this project issue
```

Expected route:

- risk label: `R0`;
- confidence: low;
- fallback review recommended.

The point is not to treat vague work as safe. The router marks uncertainty so the agent should do a small boundary review.

## Example 3: Memory Boundary Check

Input:

```text
Project lane: EXAMPLE_PROJECT
Requested path: C:\path\to\project\.agent-memory\note.md
```

Expected route:

- status: pass;
- reason: requested path is inside active project memory roots.

## Example 4: Strong Claim Check

If a final answer says a result is validated without a claim record, the claim verifier should block it. Add a claim object with source type and evidence boundary before making strong claims.
