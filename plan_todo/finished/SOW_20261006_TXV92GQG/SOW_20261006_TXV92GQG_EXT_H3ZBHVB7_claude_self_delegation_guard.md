# SOW_20261006_TXV92GQG_EXT_H3ZBHVB7 - Claude Self-Delegation Guard

- Status: COMPLETED
- Approval: APPROVED by user
- create_dttm: 2026-10-06T05:16:00+07:00
- approve_dttm: 2026-10-06T05:16:00+07:00
- finish_dttm: 2026-10-06T05:19:00+07:00
- legacy_id: SOW_0099_EXT_01
- legacy_path: plan_todo/finished/SOW_0099_EXT_01_claude_self_delegation_guard.md
- migrated_dttm: 2026-10-08T12:48:51+07:00
- legacy_title: SOW_0099 EXT_01 - Claude Self-Delegation Guard
- Parent: [SOW_20261006_TXV92GQG](SOW_20261006_TXV92GQG_claude_code_delegate_transport.md)

## Preserved Contract And Historical Evidence

- **Status**: COMPLETED
- **Approval**: APPROVED by user
- **create_dttm**: 2026-10-06T05:16:00+07:00
- **approve_dttm**: 2026-10-06T05:16:00+07:00
- **finish_dttm**: 2026-10-06T05:19:00+07:00
- **Proposed-By**: Codex
- **plan**: None; bounded extension of SOW_0099
- **Parent**: SOW_20261006_TXV92GQG_claude_code_delegate_transport.md

## Task

Prevent Claude Code from delegating to another Claude Code session when the
current coordinator is Claude, and fail closed when coordinator identity is
unknown.

## Why / Baseline

SOW_0099 documents Claude as an explicit external transport but does not state
that the transport is eligible only for a non-Claude coordinator. Without this
guard, an agent can create a recursive Claude-to-Claude handoff or make an
unsupported assumption from the presence of the CLI alone.

## Location

- `skills/sow-delegate-flow/SKILL.md`
- `tests/skill_feedback_cases/sow-delegate-flow.json`
- This extension

## As-Is Diagram (ASCII)

```text
current coordinator
        |
        +--> Claude selected -> launch Claude CLI
        |                      (self-loop possible)
        `--> identity unknown -> launch may still be guessed
```

## To-Be Diagram (ASCII)

```text
current coordinator identity
        |
        +--> non-Claude + explicit Claude -> fresh Claude transport
        +--> Claude                    -> no Claude launch; local/non-Claude path
        `--> unknown                   -> no launch; report missing evidence
```

## Deliverables / Behavior Locks

1. Add the guard only to the canonical Claude transport section of
   `sow-delegate-flow`; consumer skills keep referencing that owner.
2. Permit Claude delegation only when current coordinator identity is proven
   non-Claude and Claude is explicitly selected.
3. When current identity is Claude or unknown, do not launch/resume Claude and
   do not silently substitute a provider; keep local or route only through an
   explicitly selected non-Claude path.
4. Add sanitized expected, negative and boundary scenarios for non-Claude,
   Claude self-delegation, and unknown identity.

## Done Criteria

- The canonical skill contains one clear eligibility guard with no duplicate
  provider logic in review, execution or router skills.
- The delegate fixture contains the three guard scenarios and remains valid.
- The previous Claude transport contract, GLM policy, SOW approval gate,
  isolation rule and coordinator verification remain unchanged.
- Structural validation, targeted feedback/sync tests, JSON parsing and
  `git diff --check` pass.
- Negative check proves Claude runtime cannot launch another Claude session and
  unknown identity cannot be treated as non-Claude.

## Out Of Scope

- Detecting provider identity through a new service, registry, environment
  mutation, CLI wrapper or telemetry system.
- Changing model selection for non-Claude coordinators or replacing GLM policy.
- Changes to consumer skill ownership, product code, credentials, or unrelated
  dirty/untracked files.

## Cautions / Risks

- Provider identity must come from the current runtime/session metadata; the
  CLI's availability is not identity evidence.
- Fail-closed unknown identity may require coordinator-owned local work until a
  trustworthy identity signal exists.
- This guard prevents same-provider recursion; it does not replace normal SOW,
  isolation, model-resolution or coordinator-verification gates.

## Verification / Closeout

- Implemented the canonical self-delegation guard and added the three feedback
  scenarios.
- Four skill validators, JSON parsing, targeted feedback/sync tests and
  `git diff --check` passed.
- No Claude runtime or provider identity was changed; sync/push are handled by
  the explicit user request after commit.
