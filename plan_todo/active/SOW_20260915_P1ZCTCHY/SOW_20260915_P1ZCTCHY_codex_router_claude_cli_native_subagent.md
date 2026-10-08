# SOW_20260915_P1ZCTCHY - Codex Router Claude CLI Native Sub-Agent

- Status: DRAFT
- Approval: Not approved for implementation
- create_dttm: 2026-09-15T22:59:06+07:00
- create_date: 2026-09-15
- create_dttm_source: filesystem_birthtime
- create_dttm_confidence: filesystem_proxy
- create_dttm_evidence: `plan_todo/finished/SOW_20261008_VO3LKN0L/creation-date-evidence.json` (record: SOW_20260915_P1ZCTCHY)
- approve_dttm: null
- finish_dttm: null
- legacy_id: SOW_0056
- legacy_path: plan_todo/SOW_0056_codex_router_claude_cli_native_subagent.md
- migrated_dttm: 2026-10-08T12:48:51+07:00
- legacy_title: SOW_0056 — Codex Router Claude CLI Native Sub-Agent

## Preserved Contract And Historical Evidence

## Status / Approval

- **Status**: DRAFT
- **Approval**: Not approved for implementation
- **Task**: Evolve Codex Router's existing Claude CLI subscription-agent bridge
  into a native Codex v2 sub-agent route whose Claude-owned harness performs
  its own tools inside an isolated worktree.
- **Proposed-By**: Codex
- **Plan / Reference**:
  - `plan_todo/skill_design_decisions.md` sections 8–19
  - `plan_todo/finished/SOW_20260411_LBRWFO9M/SOW_20260411_LBRWFO9M_claude_delegate_probe.md`
  - `plan_todo/finished/SOW_20260425_9IUCS05O/SOW_20260425_9IUCS05O_sow_delegate_flow_log_parser.md`
  - `/Users/maihoangviet/Projects/tools/codex-router/docs/HOW-IT-WORKS.md`
  - `/Users/maihoangviet/Projects/tools/codex-router/docs/SUBAGENT-CERTIFICATION.md`

## Why

Codex Router already publishes proven external Responses routes as native Codex
v2 sub-agents and relays the encrypted delegated task payload. It also has an
experimental Claude Code subscription-agent bridge, but deliberately keeps that
bridge outside Codex's model picker and native sub-agent catalog.

The desired direction is to promote that Claude bridge through the existing
Codex Router collaboration path, rather than modifying Codex host internals or
writing a separate proxy lifecycle. Claude CLI remains the owner of its own
agent harness, permissions and tools; Codex receives normalized progress and
final-result events through its normal routed-child lifecycle.

## As-Is Diagram (ASCII)

```text
Codex native parent
    |
    +-- routed Responses model (registry v2)
    |       |
    |       +-- Codex Router encrypted task relay
    |               |
    |               +-- native Codex child lifecycle
    |
    `-- Claude CLI subscription bridge (experimental)
            |
            +-- official `claude` process + Claude-owned session
            +-- not in Codex picker
            +-- not a native Codex sub-agent route
            `-- permission requests rejected by default
```

## To-Be Diagram (ASCII)

```text
Codex native parent
    |
    | spawn_agent(model="claude-cli/<route>")
    v
Codex Router v2 Claude CLI route
    |
    +-- reuse encrypted delegated-task relay
    +-- create isolated worktree for the child
    +-- start official Claude CLI with stream-json
    |       |
    |       +-- Claude-owned Bash/Edit/MCP + permission policy
    |
    +-- normalize progress / final / failure / follow-up events
    v
Codex routed-child Responses stream
    |
    `-- native wait, follow-up, interrupt and FINAL_ANSWER lifecycle
```

## Intended Location

- Planning record: this file in `AISkills`.
- Future implementation authority, after a separate explicit approval:
  `/Users/maihoangviet/Projects/tools/codex-router/` only, including the
  existing Claude subscription bridge, routed catalog publication, v2
  certification and their tests/documentation.
- No Codex desktop/host source change is intended.

## Deliverables

### Phase A — read-only feasibility POC

1. Map the existing Claude subscription bridge's session and `stream-json`
   events to the exact routed-child Responses events Codex Router expects.
2. Run an isolated, read-only Claude child with no write-capable tools and
   confirm these independent properties:
   - streamed progress reaches the routed child stream;
   - final result maps to `FINAL_ANSWER`;
   - one same-thread follow-up resumes the same Claude session;
   - cancel terminates the Claude child without leaving a live process;
   - an external failure maps to a visible failed child, not a false success.
3. Prove the existing native collaboration prerequisites for the exact route:
   encrypted delegated-payload relay, marker return and same-thread follow-up.
   Do not claim native v2 eligibility merely because a direct Claude CLI call
   streams successfully.

### Phase B — read-only native route

4. Add a distinct Claude CLI route to the Codex Router catalog only after Phase
   A proves the full native child contract for the exact account, route and
   runtime. It must be explicitly selectable as a Codex native sub-agent and
   must not impersonate a hosted Anthropic API model or expose a fake Claude
   subscription model broadly in another client's picker.
5. Route `spawn`, `wait`, same-child follow-up and `interrupt` through Codex
   Router's existing native collaboration transport. Preserve child identity and
   event ordering across a reconnect.
6. Run Claude in a per-child isolated worktree. Claude owns its own tools and
   permission policy. Its tool activity is observational progress only; Codex
   must not present it as a Codex-native tool execution or assume a Codex tool
   result exists.
7. Capture bounded, redacted lifecycle metadata only: child ID, parent ID,
   Claude session ID, state transitions, elapsed time and terminal category.
   Do not persist prompts, full transcripts, credentials, payloads or raw tool
   output by default.

### Phase C — separately approved write capability

8. Write-capable Claude tools, allowed-tool policy, worktree promotion,
   commit/push/deploy authority, raw-log retention and cross-provider fallback
   are out of this SOW. They require a follow-up SOW after the read-only native
   child is production-proven.

## Done Criteria

- Phase A produces redacted runtime evidence for every listed lifecycle case;
  a direct CLI-only success is insufficient.
- The exact Claude CLI route passes Codex Router's native v2 collaboration
  certification, including encrypted relay and same-thread follow-up, before it
  can be advertised as spawnable.
- A native Codex parent can spawn, observe streamed progress from, follow up
  with, interrupt and receive a terminal result from the Claude child.
- The child is read-only and isolated: an attempted write or permission request
  fails closed and leaves the parent workspace unchanged.
- Router documentation distinguishes hosted model routes from the Claude CLI
  harness route and states the ownership boundary for tools and permissions.
- Negative check: if event translation loses a terminal state, cannot preserve
  child identity on follow-up, or bypasses Claude's permission boundary, the
  route remains unavailable as a native sub-agent.

## Out-of-Scope

- Editing Codex desktop/host internals.
- Making Claude CLI a generic `/responses`, `/complete` or hosted Anthropic API
  compatibility provider.
- Replacing Codex Router's existing hosted-model routing path.
- Any write-capable tool, repository mutation, Git remote action, deployment or
  credential migration.
- Changing the current native Codex sub-agent flow for other providers.

## Cautions / Risks

- Codex Router currently documents the Claude subscription bridge as separate
  from the native catalog. Implementation changes that policy and therefore
  require an explicit Codex Router architecture decision and documentation
  update; this SOW alone records intent only.
- Claude CLI agent-loop events and Codex Responses events are not equivalent.
  Event translation must preserve terminal state and follow-up identity without
  pretending Claude-owned tool execution was performed by Codex.
- Native v2 certification may be blocked by the active Codex account mode or
  the exact Claude CLI entitlement. A failed/deferred certification is evidence
  to stop, not justification to relax the gate.
- A worktree isolates filesystem writes but does not independently establish
  permission, secret-redaction, cancellation or process-cleanup correctness.
