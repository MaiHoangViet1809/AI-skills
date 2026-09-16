# SOW_0086 — Evidence-Based Failure Diagnosis for Skill Evolution

## Lifecycle

- Status: completed
- Approval: approved by user
- create_dttm: `2026-09-16T15:48:42+07:00`
- approve_dttm: `2026-09-16T15:53:57+07:00`
- finish_dttm: `2026-09-16T15:57:14+07:00`
- Proposed-By: Codex GPT-6
- plan: Standalone; follows [SOW_0071](SOW_0071_skill_evolution_feedback_loop.md).

## Task

Extend `skill-evolution-flow` to diagnose agent-detected mismatches and user
corrections, including failures to apply correct instructions, before deciding
whether an evidence-backed, authorized skill change is justified.

## Why

The current flow requires explicit feedback or an evolution request and assumes
a target skill can be named early. It already normalizes expected/observed
behavior, checks deployment drift, classifies causes, and supports abstention.
The missing behavior is broader diagnostic entry and explicit investigation of
instruction selection, recovery, and application when the instruction is right.
Correct instruction text does not prove that the agent applied it.

The user rejected duplicate SOW checkpoints, progress memory, and per-SOW
telemetry because existing SOW/chat mechanisms already cover those responsibilities
and metric attribution boundaries are unclear. This change reuses task evidence
and the existing evolution process instead.

## Governing Principles and Baseline

- AISkills `AGENTS.md`: DRY/KISS/SOLID, canonical-first edits, scoped approval,
  preservation of unrelated work, and verification at the claimed layer.
- No project principle file, nested AGENTS, additional `.agents/rules` files,
  or declared canonical concept index was found in the inspected AISkills tree.
  AgentHangar product concepts do not become AISkills implementation authority.
- Canonical `skills/skill-evolution-flow/SKILL.md` matches its installed Codex
  copy at drafting time; the registry owns its two shipped files.
- Existing regression fixtures cover self-update activation and deployment drift.
- Baseline: `uv run python -m unittest tests.test_skill_feedback_cases
  tests.test_skill_sync_scripts` passed all 13 tests. This is structural/sync
  evidence, not model-behavior verification.
- This is a new diagnostic capability, not a proven regression in SOW_0071;
  its completed historical scope remains unchanged.

## Location

- `skills/skill-evolution-flow/SKILL.md`
- `skills/skill-evolution-flow/agents/openai.yaml`
- `skills/registry.json`: only this skill's description
- `skills/INDEX.md`: only this skill's row
- `tests/skill_feedback_cases/skill-evolution-flow.json`
- This SOW, later `plan_todo/finished/SOW_0086_skill_evolution_failure_diagnosis.md`

No shared fixture schema or Python implementation changes are planned. Existing
`trigger` and `decision_procedure` cause classes describe the meta-skill's
regression cases; they do not assert the diagnosed task's root cause.

## As-Is Diagram (ASCII)

```text
explicit feedback / evolution request + target skill
  -> normalize -> ownership / parity / approval
  -> classify -> patch or abstain
  -> regression / validation / commit / selected sync
```

## To-Be Diagram (ASCII)

```text
explicit feedback OR agent detects mismatch OR dissatisfaction signal
  -> bounded check: user intent / expected / observed / evidence
  -> identify mismatch or stop diagnosis without inventing one
  -> enough cause diagnosis to repair the task within its authorized scope
  -> assess reusable lesson: content AND selection / recovery / application
  -> reusable skill correction supported?
       no / unknown -> explain concrete finding or uncertainty; no patch
       yes -> existing ownership / parity / approval / regression flow
           -> smallest correction -> validation -> commit
```

## Deliverables

### D1. Broaden diagnosis triggers without granting mutation authority

- Cover agent recognition of misunderstood user intent, output failing explicit
  acceptance, user correction/repeated correction, and dissatisfaction directed
  at the agent's work, including anger or profanity.
- Treat dissatisfaction as a signal to inspect nearby evidence, not proof of a
  skill defect, a diagnosis of the user's emotions, or permission to mutate.
- Routine clarification, intentional scope changes, quoted profanity, and
  unrelated frustration do not by themselves establish an agent failure.
- Tool/test failure warrants proportional triage; environment failure alone
  does not justify evolution. Do not trigger a full audit on every tool error.
- The initial diagnosis may have no known target skill. Do not fabricate one
  or force attribution to a single skill when evidence is insufficient.
- Move ownership/parity prerequisites to the point where a candidate skill is
  identified for evolution. Unknown installed origin does not block task-level
  diagnosis, but prevents claims about which skill version caused the behavior.
- Replace the current explicit-feedback-only diagnostic restriction consistently
  across frontmatter, body, UI metadata, registry description, and index row.
  Preserve explicit authorization and repository gates for mutations.
- These are declarative skill-selection cues, not a guaranteed host event hook.
  Discovery depends on the host exposing/selecting the skill; this change must
  not claim that every mismatch or compaction will automatically invoke it.

### D2. Diagnose correct-but-unapplied instructions

- Compare expected versus observed behavior against current user intent and
  applicable authority, using the minimum relevant task evidence.
- Distinguish incorrect/incomplete instructions, selection/retrieval failure,
  continuity/recovery failure, execution non-adherence, misapplication,
  deployment drift, policy conflict, and non-skill/environment causes.
- Do not infer compaction, non-loading, or deliberate disregard from a wrong
  output alone. Report observable non-application with unknown cause when needed.
- Correct wording may still need better trigger criteria or placement at the
  actual decision step if evidence supports that intervention. Prefer moving or
  clarifying an existing rule over repeating it or adding stronger MUST wording.
- Correct text is not an automatic dismissal; investigate application. Conversely,
  failure is not automatic evidence that another instruction will fix it.
- Reuse existing recovery/reading mechanisms; no new hooks, checkpoints, runtime
  enforcement, logs, or cross-skill edits are introduced by this SOW.

### D3. Keep task repair and durable evolution distinct

- Prioritize correcting the current task within existing authority. Reuse prior
  approval; do not make an upset user reapprove already-authorized repair.
- Perform enough diagnosis to choose a sound repair; do not require completing
  the whole task before learning from its failure. A blocked repair can still
  yield a supported improvement without claiming that the task was repaired.
- If repair needs new scope, apply that project's approval rules. Diagnosis
  cannot bypass the active SOW or an explicit stop from the user.
- Only enter canonical mutation when evidence identifies an actionable reusable
  correction, an AISkills-owned target, and sufficient approved scope.
- Unknown cause and no skill change are valid outcomes. Keep the finding in
  existing task discussion/evidence; do not mandate a new persistent record.
- Preserve canonical ownership, installed-parity checks, regression-before-patch,
  validation, scoped commit, optional selected deployment, and self-update rules.
- Detecting deployment drift does not itself authorize sync. Use an existing
  authorized target/scope or report the deployment finding without mutation.
  Ask only for information needed to continue the user's requested action;
  autonomous diagnosis alone must not force an ownership questionnaire.
- A trigger does not recursively start another evolution run. Self-update applies
  only on a later invocation; the current run keeps its initial instructions.

### D4. Regression coverage using the existing fixture format

Add compact sanitized cases, each with expected, negative, and boundary scenarios:

| Proposed case ID | Behavior to cover |
| --- | --- |
| `failure-diagnosis-entry-001` | Self-detected intent/output mismatch; ordinary clarification or scope change; unknown target skill |
| `dissatisfaction-evidence-001` | Work-directed frustration prompts bounded inspection; quoted/unrelated profanity; anger without enough evidence |
| `instruction-selection-recovery-001` | Known selection omission versus evidence-backed recovery loss; no inferred compaction from output alone |
| `instruction-adherence-interpretation-001` | Available rule skipped versus misapplied; justified placement correction versus duplicate wording; unresolved cause |
| `diagnosis-mutation-boundary-001` | Authorized task repair first; diagnosis without edit authorization; environment/policy causes and no-patch outcome |

Preserve self-update semantics. Align the existing deployment-drift fixture so
sync has explicit authority and unknown origin blocks attribution/mutation,
not bounded diagnosis; avoid contradictory old expected behaviors. Scenario
inputs must not leak expected answers into any later model evaluation. The conversation is real
design/correction evidence; proposed scenarios are regression contracts, not
fabricated observations of runtime failures.

## Done Criteria

0. Keep the skill concise and easy for the agent to interpret. Use concrete
   discovery cues for misunderstood intent, unexpected output, user correction/
   frustration, and unapplied instructions. Keep one decision flow; every
   sentence must change selection, action, or a necessary boundary. Remove
   repeated advice instead of copying this SOW into the skill. Review wording
   and placement for useful behavioral cues, not claims of changing model weights
   or guaranteed triggering. Report before/after size as context, not a target.
1. All shipped discovery descriptions and the body agree that diagnosis may
   begin proactively but mutation remains evidence-based and authorized.
2. The flow covers misunderstood intent, failed acceptance, repeated correction,
   dissatisfaction, and correct-but-unapplied instructions without forced causes.
3. Unknown target/cause does not force registry lookup, patch, or broad scanning;
   ownership must still be established before any skill edit.
4. Negative review confirms that anger alone cannot authorize edits, every tool
   error does not start evolution, and correct skill text cannot dismiss an
   observed application failure.
5. Only the listed skill/metadata/fixture surfaces change; no new skill, runtime
   component, telemetry, memory, dependency, schema, or adjacent skill edits.
6. Skill-creator structural validator, existing feedback/sync unit tests, and
   `git diff --check` pass. Inspect scenario expectations against final wording.
7. Report structural validation and scenario review separately from actual model
   behavior. No parallel candidate runs or repeated benchmark requirement.
   Without fresh-context behavioral evidence, mark behavioral reliability
   unverified; do not claim agent forgetting has been eliminated.
8. Commit only scope-owned implementation files after approval and validation.
   Close the implementation SOW with the behavioral-evidence limitation explicit,
   then move it to `finished/` and update its relative SOW_0071 reference.

## Out-of-Scope

- Implementing this draft before approval.
- Creating a separate learning-from-failure skill or orchestration/reviewer layer.
- New SOW checkpoints, progress copies, mandatory failure store, metrics, reward
  scalar, automatic transcript mining, or persistent user profiling.
- Fixing other skills merely because diagnosis points to them; each needs its
  own authorized scope. Existing unrelated router changes remain untouched.
- Changes to AgentHangar, host compaction, native skill selection, or memory.
- Running parallel candidates, repeated benchmarks, or claiming causal efficacy
  from structural tests or non-comparable production tasks.
- Installed-environment deployment in this SOW: no destination has been selected
  by the user. Canonical update/commit is the delivery boundary; later exact-skill
  sync requires a selected target. No push or remote publication.

## Cautions / Risks

- Broad triggers can distract from task delivery; keep diagnosis bounded and
  reuse existing evidence, with no repeated unchanged diagnosis.
- Frustration is an ambiguous signal; use task facts, not tone, to attribute cause.
- An agent's introspective explanation is a hypothesis unless evidence supports it.
- Correct instructions can fail in application; more words may add cost without
  changing behavior. Require a plausible evidence-backed intervention.
- Existing fixtures validate structure, not actual trigger selection or adherence.
- Diagnosis permission must not silently become blanket future mutation approval.
- Local task-router skill and fixture are already modified, and an unrelated
  SOW_0056 is untracked; preserve them and exclude them from this task's commit.

## Review Summary

- Pass 1 — baseline and authority: corrected the premature ownership/parity
  gate, required matching updates to the old drift fixture, distinguished sync
  permission from diagnosis, clarified blocked-task handling, and split
  application cases to avoid hiding four failure modes in one scenario.
- Pass 2 — adversarial acceptance: aligned the diagram with diagnosis-before-
  repair, made host-selection limitations explicit, and checked the following
  counterexamples against D1-D4 and the done criteria. No remaining actionable
  planning findings after these corrections; this is not behavior verification.

| Counterexample | Required outcome |
| --- | --- |
| Agent detects misunderstood intent; user has not requested evolution | Diagnose and repair within task scope; no implicit skill-mutation authority |
| User swears but the mismatch is unclear | Inspect nearby task evidence; do not invent failure, emotion diagnosis, or patch |
| Correct rule was not applied | Investigate selection/recovery/application; neither dismiss nor add duplicate wording |
| Wrong output but no evidence of loading or compaction | Record observed mismatch and unknown cause; no fabricated attribution |
| Installed source is stale or unidentified | Preserve parity/ownership constraints for mutations without blocking bounded diagnosis |
| Repair is blocked or user changes scope | Report task state accurately; no forced full repair or mislabeling scope change as failure |
| Structural tests and scenario review pass | Canonical implementation may close; actual behavioral reliability remains unverified |

Both passes were sequential reviews by the author; no independent-agent review
or model forward-test was performed during SOW preparation.


## Implementation and Verification

- Added the approved concise-writing criterion before implementation and kept
  one five-step flow with explicit discovery cues and decision-point rules.
- Updated canonical skill, UI metadata, registry description, and index row.
- Added five regression cases and aligned deployment-drift expectations:
  `failure-diagnosis-entry-001`, `dissatisfaction-evidence-001`,
  `instruction-selection-recovery-001`,
  `instruction-adherence-interpretation-001`, and
  `diagnosis-mutation-boundary-001`. Existing self-update behavior is retained.
- Seven cases contain 21 expected/negative/boundary scenarios; schema unchanged.
- Skill structural validator: PASS. Feedback/sync suite: 13 tests PASS.
- Metadata parsing, UI description length, skill invocation reference, registered
  file references, and `git diff --check`: PASS.
- Author scenario walkthrough: checked self-detected mismatch without edit
  permission, frustration without evidence, correct-but-unapplied rules,
  unobservable compaction, policy/environment causes, blocked repair, and stale
  installation. These are static contract checks, not model executions.
- Gap-finding: compared final instructions with D1-D4 and the original feedback;
  preserved canonical ownership, authorization, regression-before-patch,
  self-update boundary, exact overwrite dry-run parity, and optional deployment.
  No remaining actionable implementation finding within approved scope.
- Unrelated router skill/fixture and SOW_0056 hashes remained unchanged.
- Size: 865 -> 829 whitespace-separated words; 132 -> 72 lines. This measures text size, not tokens or trigger reliability.
- Delivery: canonical source implementation only. Installed copies were not
  synced and no remote push occurred, as approved in Out-of-Scope.
- Behavioral reliability remains unverified: no isolated model forward-test or
  live post-update task was run. The approved done criteria permit canonical
  implementation closure with this limitation; future authorized real usage
  can provide evidence without a mandatory benchmark or monitoring mechanism.
