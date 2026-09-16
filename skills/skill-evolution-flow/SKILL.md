---
name: skill-evolution-flow
description: Diagnose misunderstood user intent, unexpected output, user corrections or frustration, and instructions not applied; evolve AISkills-owned skills when evidence and authorization support a change. Use for agent-detected mismatches or explicit evolution requests, not routine clarification or unrelated frustration.
---

# Skill Evolution Flow

Diagnose the failure, repair the task, then decide whether a reusable skill correction is justified. Diagnosis is not permission to edit or deploy.

## 1. Establish The Mismatch

Compare user intent and acceptance with observed behavior using nearby task evidence. A target skill need not be known yet.

- Work-directed anger, profanity, or repeated corrections prompt inspection, not proof of a skill defect or an emotional profile. Quoted profanity and intentional scope changes alone are not failures.
- Triage tool/test errors proportionally; environment faults alone do not warrant evolution.
- If the mismatch is unclear, keep it unresolved. Ask only what is needed to continue the requested work; do not force skill attribution or broad scanning.

Diagnose enough to repair the current task within its existing approval. Honor scope changes and user stops. A blocked repair can still yield a lesson; do not claim it succeeded or wait for full task completion to learn.

## 2. Find The Cause

Correct instructions can fail in selection, recovery, or application. Inspect available evidence rather than treating correct wording as success.

| Evidence-backed cause | Smallest useful response |
| --- | --- |
| Skill not selected or selected too broadly | Clarify frontmatter discovery cues |
| Relevant instruction lost during continuation | Use existing recovery to reread it; assess the missing recovery step |
| Available rule skipped | Repair the action; consider moving the rule to the decision point if evidence supports it |
| Rule misinterpreted or procedure incomplete | Clarify the decision or procedure |
| Repeated deterministic operation fails | Inspect the bundled script/resource |
| Interface metadata is stale | Align `agents/openai.yaml` |
| Environment or higher-priority policy explains the result | Address/report that cause; no skill patch |

Wrong output alone does not prove non-loading, compaction, or disregard. Mark the cause unknown when evidence cannot distinguish them. Do not repeat a clear rule or strengthen MUST wording without a supported reason that the change will help.

Keep no-patch findings in the existing discussion. Do not add telemetry, checkpoints, a failure store, or recursive evolution; revisit only with new evidence. Discovery cues cannot guarantee host selection.

## 3. Gate The Change

For a supported reusable correction, identify the target skill, expected/observed behavior, evidence, and general invariant.

- Resolve ownership through `AISkills/skills/registry.json` and its canonical folder. Never vendor or edit system, plugin-owned, or installed-only skills as AISkills sources.
- Compare a known installed origin with canonical before blaming the source. If canonical already fixes deployment drift, sync and retest only with an authorized target. Unknown origin permits diagnosis but not version attribution or guessed mutation.
- Read the target repo's instructions and git status. Reuse approval covering the exact edit; route new scope through its SOW gate. Behavior-bearing `SKILL.md` edits are not docs-only exemptions.

Proceed with an authorized correction; seek approval for uncovered material changes; abstain from mutation when ownership, evidence, or expected behavior is insufficient. Do not patch merely to improve wording.

## 4. Record And Patch

Before patching, add a sanitized case with a stable ID to `tests/skill_feedback_cases/`: expected, negative, and boundary scenarios. Exclude secrets, private transcript content, and machine-specific paths.

Use `skill-creator` to make the smallest general correction in canonical source. Keep instructions concise: concrete trigger cues, one decision flow, and each rule at its action point. Align stale UI/discovery metadata; do not add changelogs or duplicate guidance.

When updating this skill itself, finish the current run under its initial instructions. The revision applies on a later invocation.

## 5. Validate, Commit, And Optionally Deploy

- Run the available skill-creator structural validator and `uv run python -m unittest tests.test_skill_feedback_cases tests.test_skill_sync_scripts`.
- Review diff/scope and expected, negative, and boundary behavior. Use isolated forward-tests when available and authorized; do not require parallel candidates or repeated benchmarks. Structural tests and scenario review do not prove model behavior; report it unverified without behavioral evidence.
- Do not commit or sync failed validation. Otherwise commit only approved files; never push unless requested.

For one explicitly selected, authorized environment, sync only the changed skill using existing sync tooling:

1. Fix agent, scope, target, and skill; use `--overwrite` for replacements and preview with `--dry-run`.
2. Execute the same command, removing only `--dry-run`.
3. Run `scripts/skills/verify_skill_copy.py --skill <name> --target-root <skills-root>`; report missing, extra, or changed files.

Never use `--all` or sync multiple environments per feedback event. If deployment fails after commit, retain the commit and report partial deployment; leave unrelated installed skills untouched. With no authorized target, finish at the canonical commit.

## Closeout

Briefly report the finding/correction, target and case IDs if applicable, validation versus behavioral evidence, commit, deployment/parity status, and remaining uncertainty. A no-change outcome needs only the finding and reason.
