# SOW_20260920_9851QRQ4 - Scope Decisions

- legacy_id: SOW_0092
- legacy_path: plan_todo/SOW_0092_codex_router_external_subagent_message_compat.md
- migrated_dttm: 2026-10-08T12:48:51+07:00
- Parent: [SOW_20260920_9851QRQ4](SOW_20260920_9851QRQ4_codex_router_external_subagent_message_compat.md)

## Preserved Contract And Historical Evidence

## Implementation Decision

- Apply `agentMessagesAsUserMessages()` immediately after
  `normalizeRoutedAgentInput()` has recovered collaboration plaintext, before
  aging, compaction preparation, image bridging, tool-history rewriting, or
  provider request construction.
- Apply the same normalized representation to ordinary turns and routed
  compaction so replay cannot reintroduce the private item.
- The direct Responses branch bypasses this compatibility boundary and remains
  byte-compatible with its existing native contract.
- Do not add provider IDs, model-name conditions, prompt injection, duplicate
  task messages, fallback delivery, or another converter.
- Extend the existing helper only to retain a stable item `id` for router-side
  compaction correlation while omitting private sender fields; do not preserve
  `author` or `recipient` as provider-facing fields.
- The reverse routed-child-to-native normalization is verification-only in this
  SOW; its implementation is not changed unless review finds a separate proven
  defect and the SOW is explicitly extended.
