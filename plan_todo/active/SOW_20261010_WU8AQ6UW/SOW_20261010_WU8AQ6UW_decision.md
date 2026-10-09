# SOW_20261010_WU8AQ6UW — Decisions

- Parent: SOW_20261010_WU8AQ6UW_claude_code_glm_setup_skill.md

## D001 — Where the relay files live

- Date: 2026-10-10T04:48:31+07:00
- Status / Owner: decided by user 2026-10-10T04:55:17+07:00: (a); Claude Code
- Context: `glm-run` and `glm-worker.md` live in local codex-router `contrib/`,
  which the user chose not to push. A colleague cannot obtain them there.
- Options: (a) bundle them in the skill and make the skill the canonical
  source; repoint this machine's symlinks to the AISkills copies and leave
  the codex-router contrib copy unused; (b) bundle copies and keep codex-router
  contrib canonical (two copies that can drift); (c) publish codex-router
  somewhere and reference it.
- Recommended: (a) — one source of truth that colleagues can reach.
- Evidence: codex-router `origin` is the third-party upstream; push declined.
- Supersedes: None.

## D002 — Delivering the stream prefix fix

- Date: 2026-10-10T04:48:31+07:00
- Status / Owner: decided by user 2026-10-10T04:55:17+07:00: (a); Claude Code
- Context: Upstream codex-router (checked 2026-10-10, `00eed6eb`) still lets
  LiteLLM drop the content of mixed reasoning+content chunks, so GLM answers
  lose their opening words. The fix is local commit `3b9cb828` (MIT-licensed
  project).
- Options: (a) reference describes the probe, root cause and the fix design,
  and includes the transform source with MIT attribution for the colleague's
  agent to integrate after confirmation; (b) probe and symptom only, telling
  the colleague to raise it upstream; (c) ship a git patch file.
- Recommended: (a). A patch file (c) is likely not to apply on a fast-moving
  upstream; (b) leaves the colleague with truncated answers.
- Evidence: probe and fix verification in this session; upstream grep.
- Supersedes: None.

## D003 — GreenNode route on upstream codex-router (open evidence)

- Date: 2026-10-10T04:48:31+07:00
- Status / Owner: proposed; verification during implementation
- Context: Upstream has no GreenNode provider; its generic provider publishes
  models as `<endpoint>/<model id>`.
- Chosen: instruct `providers generic add greennode ... --adapter openai-chat`,
  a private credential prompt, and `add-model greennode glm-5.3`, so the id is
  `greennode/glm-5.3`. Upstream source confirms the subcommands
  (`providers.mjs`: `generic credential`, `generic add-model`) and the slug
  format (`user-models.mjs:116`). Implementation runs the add/add-model/list
  path in a detached upstream worktree with a temporary state directory,
  because this machine's fork reserves `greennode` as a built-in provider.
- Tradeoffs / Risks: unverified end to end on upstream; the skill states it.
- Evidence: upstream README "Custom: one provider, many endpoints".
- Supersedes: None.
