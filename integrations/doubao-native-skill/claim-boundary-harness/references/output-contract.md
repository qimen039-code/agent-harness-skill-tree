# Output Contract

## Normal Answers

For simple chat, answer directly and keep overhead low.

For nontrivial execution, include only the boundary sections that help the user:

- Facts: verified local or external evidence.
- Hypotheses: plausible but unverified explanations.
- Unknowns: missing data or untested assumptions.
- Risks: safety, privacy, project-lane, or claim-boundary risks.
- Next steps: concrete actions or validation paths.

## Strong Claims

Before publishing or finalizing strong claims, check:

1. Is the evidence source named?
2. Is the scope limited to what was actually observed?
3. Are current-version or external facts verified?
4. Are causal claims separated from local observations?
5. Are host-owned guards distinguished from CBH-owned enforcement?

## Script Validation

Use `lint_claims.py` as a formatting and boundary smoke check. It does not prove that facts are true.

Use `repair_claims.py` only for mechanical schema repair. It must not invent evidence or fill unknowns.

If a script passes with warnings, report the warnings as review debt rather than a clean validation.
