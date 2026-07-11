---
name: skill-evolution-flow
description: Evolve an AISkills-owned skill from explicit real-usage feedback. Use when a user says a skill triggered incorrectly, chose the wrong mode, followed the wrong procedure, needs a durable behavioral correction, or should be merged back into the canonical AISkills repository and synced to one local agent environment.
---

# Skill Evolution Flow

Turn explicit user feedback into a canonical, regression-backed skill update without bypassing repository governance or editing installed copies as source.

## Invariants

- Treat `AISkills/skills/<skill>/` as source of truth.
- Treat installed skill directories as deployment targets only.
- Require explicit user feedback or a direct evolution request; do not infer permission from ordinary task friction.
- Obey the target repository's `AGENTS.md`, SOW, approval, and git rules before editing.
- Never vendor or mutate system, plugin-owned, or installed-only skills as though AISkills owned them.
- Sanitize regression evidence. Exclude secrets, private transcript content, and machine-specific absolute paths.

## Workflow

### 1. Normalize The Feedback

Capture:

- target skill
- triggering request and relevant context
- observed behavior
- expected behavior
- reusable invariant behind the correction
- evidence reference when available

Do not copy a user comment literally into a skill when a narrower general rule explains the failure.

### 2. Verify Ownership

Locate the canonical AISkills checkout and read `skills/registry.json`.

- Continue only when the target is registered and its canonical folder exists.
- Stop and report ownership when the target exists only under an installed, system, or plugin path.
- Do not import an unowned skill into AISkills merely to make it editable.

### 3. Apply The Repository Policy Gate

When the installed path that produced the behavior is known, compare it with canonical source before rewriting anything.

- If the installed copy is stale and canonical already expresses the expected behavior, sync the canonical skill and retest instead of patching it.
- Continue diagnosis only when parity is confirmed or the canonical source itself is still wrong.

Then read repository instructions and inspect git status.

- Continue when an approved scope covers the change.
- Route or draft the required SOW when repository policy requires one.
- Wait for approval before behavior-bearing edits when the policy requires approval.
- Do not classify `SKILL.md` as docs-only merely because it is Markdown.

### 4. Classify The Cause

| Cause | Change surface |
| --- | --- |
| Skill did not trigger or triggered too broadly | YAML frontmatter `description` |
| Skill chose the wrong mode or decision | `SKILL.md` decision rules |
| Skill followed an incomplete procedure | `SKILL.md` workflow |
| Repeated deterministic operation failed | bundled script or resource |
| UI metadata no longer matches behavior | `agents/openai.yaml` |
| Higher-priority system or project policy caused the result | no skill patch; explain the conflict |

Choose one update mode:

- `authorized correction`: low ambiguity, preserves purpose, and approved scope permits the edit
- `material change`: changes purpose, authority, safety, or major scope; request approval
- `abstain`: ownership, expected behavior, or evidence is insufficient

### 5. Record A Regression Case

Before patching, add or update the target's sanitized JSON fixture under `tests/skill_feedback_cases/`.

Include one scenario of each kind:

- `expected`: behavior that must occur
- `negative`: request that must not trigger or apply the new rule
- `boundary`: nearby ambiguous case and its safe handling

Use a stable case ID and report it at closeout. Structural fixture tests do not prove model behavior.

### 6. Patch The Canonical Skill

Use `skill-creator` for the target skill. Make the smallest general correction that satisfies the invariant.

- Update `agents/openai.yaml` when interface text becomes stale.
- Do not add changelogs or auxiliary documentation to the skill folder.
- If this skill updates itself, finish the current run with the start-of-turn instructions. The revised version applies only on a later invocation.

### 7. Validate Before Commit

Run:

- the available `skill-creator` structural validator for every changed skill
- `uv run python -m unittest tests.test_skill_feedback_cases tests.test_skill_sync_scripts`
- targeted positive, negative, and boundary forward-tests when a clean isolated context is available
- git diff and scope review

Report forward-test evidence separately from deterministic checks. Mark behavior unverified when isolated testing is unavailable.

Do not commit or sync when validation fails.

### 8. Commit Then Deploy One Skill

Commit only the exact approved AISkills files, including the canonical skill, regression fixture, and aligned test or metadata changes. Do not push unless explicitly requested.

For one explicitly selected agent environment:

1. Build the exact sync command with agent, scope, target, `--skill <name>`, and `--overwrite` when replacing an existing target.
2. Preview that exact command by adding `--dry-run`.
3. Execute the same command by removing only `--dry-run`.
4. Run `scripts/skills/verify_skill_copy.py --skill <name> --target-root <skills-root>`.
5. Report missing, extra, or changed relative paths if parity fails.

Never use `--all` or sync multiple environments from one feedback event.

If commit succeeds but deployment fails, keep the canonical commit, report partial deployment, and leave unrelated installed skills untouched.

## Closeout

Report:

- target skill and regression case ID
- generalized behavior correction
- deterministic validation results
- forward-test status
- canonical commit
- selected sync target and parity result
- anything not verified
