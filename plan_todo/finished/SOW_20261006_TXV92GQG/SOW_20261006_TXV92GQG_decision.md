# SOW_20261006_TXV92GQG - Scope Decisions

- legacy_id: SOW_0099
- legacy_path: plan_todo/finished/SOW_0099_claude_code_delegate_transport.md
- migrated_dttm: 2026-10-08T12:48:51+07:00
- Parent: [SOW_20261006_TXV92GQG](SOW_20261006_TXV92GQG_claude_code_delegate_transport.md)

## Preserved Contract And Historical Evidence

## Decision

Approved by the user. Use one canonical Claude CLI contract in
`sow-delegate-flow`; consumer skills reference it but do not duplicate it.
Claude is an explicit transport/model choice, with `opus` for thinking/review
and `sonnet` for approved implementation; GLM-5.3-max remains the open-choice
default. EXT_01 additionally forbids Claude-to-Claude self-delegation.
