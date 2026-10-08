# SOW_20260918_9TYIE2MO - Scope Decisions

- legacy_id: SOW_0089
- legacy_path: plan_todo/SOW_0089_public_repo_privacy_hardening.md
- migrated_dttm: 2026-10-08T12:48:51+07:00
- Parent: [SOW_20260918_9TYIE2MO](SOW_20260918_9TYIE2MO_public_repo_privacy_hardening.md)

## Preserved Contract And Historical Evidence

## Decision Log

- D001 — 2026-09-18 — proposed: do not use a tracked-plus-local-only commit
  model on pushed `main`; keep public-safe planning tracked and move private
  planning outside the public repo.
- D002 — 2026-09-18 — proposed: treat history rewrite/force-push as a separate
  explicit operator gate, not an automatic consequence of path sanitization.
