# Activation And Continuity

## Required Activation Probe

When asked whether Claim Boundary Harness is active in the current Doubao chat, do not infer from an older chat directory. Verify this current surface:

1. Can the agent name this skill as `claim-boundary-harness`?
2. Can it cite these references by path under the native `.skills` folder?
3. Can it describe the current mode as native-client, skill-guided, or chat-demo-only?
4. Can it access the intended `facts.json` and `hypotheses.json` for this workspace, if memory is part of the task?

If any answer is missing, say `not loaded or not verified in this chat`.

## Session Boundary

`%USERPROFILE%\.doubao\chats\<date>\...` is a chat/workspace artifact lane. A complete folder there does not automatically affect later new chats.

The native runtime-expanded skill surface observed locally is:

`%USERPROFILE%\AppData\Local\Doubao\User Data\Default\.doubao\agent_mode\workspace\.skills\claim-boundary-harness`

This path must be verified on the target machine and client version before claiming support. A restart test showed that direct manual copying into `.skills` can be removed when Doubao refreshes the workspace. Treat this folder as a runtime-expanded surface unless the skill has been saved through the host's `sync_skill_folder_to_cloud_disk` path or another verified client-owned registration API.

## Continuity Rule

For long work:

- keep a short release receipt after each active phase;
- include current stage, completed steps, artifact paths, evidence refs, and next resume entry;
- release full skill context after task completion and keep only the receipt unless the task is still active.

Do not claim cross-chat continuity unless a memory lane or native skill surface was actually loaded in the new chat.

## Persistent Install Probe

For persistent install, the current evidence points to this required host-owned step:

```text
sync_skill_folder_to_cloud_disk(<complete skill folder path>)
```

This call must be made from inside a Doubao Agent context that exposes the tool. File-system copy alone is a deployment smoke check, not a durable install.

If the tool is not exposed, report:

```text
status: runtime-expanded only
persistent_install: not verified
reason: sync_skill_folder_to_cloud_disk unavailable in current host context
next_check: open a new chat after workspace refresh and rerun activation probe
```
