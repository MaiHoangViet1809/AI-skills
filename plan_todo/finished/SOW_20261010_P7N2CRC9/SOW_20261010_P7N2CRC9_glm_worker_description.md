# SOW_20261010_P7N2CRC9 — glm-worker Description For Automatic Gates

- Status: DONE
- Approval: approved by user; explicit request ("sửa xong commit, push giúp tôi") to the proposed description change
- create_dttm: 2026-10-10T12:27:16+07:00
- approve_dttm: 2026-10-10T12:27:16+07:00
- finish_dttm: 2026-10-10T12:28:29+07:00
- Proposed-By: Claude Code (claude-opus-5-5)
- plan: Standalone; follow-up recorded in SOW_20261010_WU8AQ6UW closeout
- Decision Log: SOW_20261010_P7N2CRC9_decision.md

## Task / Why

Change the `glm-worker` agent description so it no longer says "Use only when
the user asks", which contradicts the automatic delegation gates added in
SOW_20261010_CV7I1SN0 and could make Claude Code skip a gate-selected call.

## Location / Deliverables

- `skills/claude-code-glm-setup/assets/glm-worker.md`: frontmatter
  `description` line only.
- This SOW bundle and its decision log.

## As-Is / To-Be

```text
As-Is  description: "... Use only when the user asks to hand work to GLM ..."
         -> a delegation gate selects glm-worker -> description discourages the call
To-Be  description: "... Use when the user asks, or when a delegation gate selects it
         from the interactive top-level session; never from claude -p, a delegate
         or a sub-agent ..." -> gate and description agree; one-level rule restated
```

## Done Criteria

- Only the `description` line changes; agent body, model, effort and tools unchanged.
- `~/.claude/agents/glm-worker.md` (symlink) shows the new description and
  the agent still runs: one call returns `effort=max ok=True`.
- Full AISkills suite passes; `git diff --check` passes.
- Commit only this SOW's files; push `main`; sync the skill to Claude only.

## Out-of-Scope

The relay script, the delegation skills, codex-router, Codex skills.

## Cautions / Risks

- The relay copy in codex-router `contrib/` keeps the old text; it is no
  longer canonical (SOW_20261010_WU8AQ6UW D001) and is not used on this machine.

## Verification / Closeout

- Only the `description` line of `assets/glm-worker.md` changed (1+/1-).
- `~/.claude/agents/glm-worker.md` (symlink to the AISkills asset) shows the
  new text; a call afterwards returned `effort=max ok=True` with the
  expected result.
- Full suite 47/47; `git diff --check` pass.
- Not verified: whether an open session re-reads the description without a
  restart (new sessions read it at start).
