# Doubao Host Adapter Notes

## Observed Local Surfaces

These surfaces were observed on a Windows Doubao desktop client:

- `AppData\Local\Doubao\Application`: client binaries and manifests. Do not modify.
- `AppData\Roaming\Doubao\public_config.json`: small public config observed for text picker behavior. Not a CBH skill surface.
- `AppData\Local\Doubao\User Data\Default`: Chromium profile area. Do not edit Preferences, IndexedDB, Local Storage, cookies, or browser databases directly.
- `AppData\Local\Doubao\User Data\Default\.doubao\agent_mode\workspace\.skills`: native Agent Mode runtime skill folder observed locally.
- `%USERPROFILE%\.doubao\chats\<date>\...`: chat/workspace artifacts. Useful for outputs, not a global loader.

## No-Edit Boundaries

Do not write into browser profile storage directly. Use native skill folders or user-visible workspace files only.

Do not edit `.skill_meta_list.md` unless a client-owned API or verified local evidence shows it is required. In the inspected client it was empty while built-in skills existed, so manual edits are not justified.

Do not modify application binaries, manifests, cache databases, cookies, auth files, or telemetry stores.

## Deployment Shape

Preferred package structure:

```text
.skills/
  claim-boundary-harness/
    SKILL.md
    references/
    scripts/
    templates/
```

Keep a canonical copy in the repository. Directly copying it into `.skills` can be useful as a same-session smoke check, but a restart test showed that Doubao may regenerate this folder and remove manually copied custom skills.

For durable registration, use the host-owned skill save path described by `skill-creator-for-task`: call `sync_skill_folder_to_cloud_disk` with the complete skill folder path from inside Doubao Agent Mode. If that tool is not exposed, direct copy remains `runtime-expanded only` and must not be reported as persistent. If the client update rewrites `.skills`, redeploy or resync from the repository copy and rerun the activation probe.
