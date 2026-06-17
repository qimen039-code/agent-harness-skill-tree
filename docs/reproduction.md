# Local Reproduction

Run these commands from the repository root on Windows PowerShell.

## 1. Intake Router

```powershell
powershell -ExecutionPolicy Bypass -File .\skills\embedded-harness\harness_intake_router.ps1 -TaskText "fix the script and run benchmark" -Cwd "C:\path\to\project"
```

Expected highlights:

- `project_lane`: `EXAMPLE_PROJECT`;
- `risk_level`: `R4`;
- `triggered_risks`: `R4`, `R3`;
- required gates include `change_contract_gate`, `external_research_gate`, `verification_gate`, and `claim_gate`.

## 2. Fallback Boundary

```powershell
powershell -ExecutionPolicy Bypass -File .\skills\embedded-harness\harness_intake_router.ps1 -TaskText "handle this project issue" -Cwd "C:\path\to\other"
```

Expected highlights:

- `classification_confidence`: `low`;
- `fallback_model_judgment_recommended`: `true`.

## 3. Memory Isolation

```powershell
powershell -ExecutionPolicy Bypass -File .\skills\embedded-harness\harness_memory_isolation_gate.ps1 -ProjectLane EXAMPLE_PROJECT -RequestedPath "C:\path\to\project\.agent-memory\note.md"
```

Expected highlight:

- `status`: `pass`.

## 4. External Research Trigger

```powershell
powershell -ExecutionPolicy Bypass -File .\skills\embedded-harness\harness_external_research_gate.ps1 -TaskText "check latest package version 1.2.3 on GitHub"
```

Expected highlight:

- `needs_external_research`: `true`.

## 5. Claim Schema

```powershell
powershell -ExecutionPolicy Bypass -File .\skills\embedded-harness\harness_claim_schema_verifier.ps1 -ClaimJson '{"claim_type":"architecture_decision","source_type":"local_file","evidence_boundary":"whiteboard smoke"}'
```

Expected highlight:

- `status`: `pass`.

## Notes

These tests prove only that the whiteboard scripts run and return expected routing decisions. They do not prove that an adopting agent will honor the gates. Hook or wrapper integration is required for stronger enforcement.
