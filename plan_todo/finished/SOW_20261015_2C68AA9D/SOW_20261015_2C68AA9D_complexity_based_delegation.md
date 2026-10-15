# SOW_20261015_2C68AA9D - Complexity-Based Delegation

- Status: COMPLETED
- Approval: APPROVED by user
- create_dttm: 2026-10-15T11:49:50+07:00
- approve_dttm: 2026-10-15T12:24:22+07:00
- finish_dttm: 2026-10-15T12:37:24+07:00
- Proposed-By: Codex
- plan: None; bounded change to three skills.

## Task / Why

Require native GLM-5.3-max delegation for large/complex tasks, prohibit automatic
delegation for simple tasks, and retain explicit user selections. Current rules
force handoffs even for small local work, adding unnecessary coordination.

This is a requested policy change, not failure to follow the old rule. It
supersedes the blanket simplicity prohibition after approval and implementation;
completed planning records remain historical. Follow AGENTS.md and
skill-evolution-flow: SOW-first, DRY/SOLID/KISS, isolated ownership and evidence.
No project concept authority or PRODUCT_PRINCIPLE_DESIGN.md is declared/present.

## Location

- `skills/sow-delegate-flow/SKILL.md`, `references/claude-code.md`, `agents/openai.yaml`
- New canonical `skills/sow-delegate-flow/references/task-complexity.md`
- `skills/task-execution-flow/SKILL.md`, `agents/openai.yaml`
- `skills/task-review-investigate-compare/SKILL.md`, `agents/openai.yaml`
- Matching three JSON files under `tests/skill_feedback_cases/`
- `tests/test_mandatory_delegation_contract.py`
- `skills/registry.json`: only the new delegate reference manifest entry
- `INSTALL_FOR_AGENTS.md`: only companion-skill guidance for the shared rubric
- This SOW bundle, including review, verification and lifecycle records

Change only task-owned hunks. Existing dirty execution/Redmine/policy work is
not authorized by this SOW. Preserve existing registry/install-guide changes;
only the manifest entry and companion guidance above are in scope.

## As-Is Diagram (ASCII)

```text
review / implementation -> native exact GLM available?
  yes -> MUST delegate even simple work; no safe slice -> stop
  no / unknown -> main, with capability evidence
```

## To-Be Diagram (ASCII)

```text
task -> explicit user delegation / local-only selection? -> honor selection
     -> classify whole task
        simple -> MUST main; no automatic delegate or GLM lookup
        large / complex -> native exact GLM-5.3-max gate
          available -> MUST delegate meaningful authorized work / review
          absent / unknown -> main; no external-client discovery
          actual failure -> bounded repair + evidence-backed local fallback
```

## Deliverables / Behavior Locks

1. One shared classification contract in the delegate reference; execution and
   review locate it via supplied harness/project skill locations, not assumed
   sibling roots. Keep decision cues at their action points without copying a
   full rubric into each skill. Reading this reference is not activation of
   delegation and must not trigger model discovery. If the contract is missing, leave classification
   unresolved, report the missing resource and do not invent a simple exemption
   or auto-install it.
   Register the new reference in the exact file manifest. Declare
   sow-delegate-flow as the required rubric companion in the two consumer
   skills and install guide. Explicit subset installs must disclose a missing
   companion and obtain permission to add it, not silently widen the subset;
   no new installer/dependency-resolution mechanism is required.
2. A task is SIMPLE only when scope, method and acceptance are clear, its impact
   is bounded, and no complexity condition below applies. Examples:
   - Config review against a known schema/contract, without tracing interactions.
   - Localized one-file edit/review with no shared-contract or cross-module change.
   - One tool/MCP call with known inputs and directly inspectable output.
   - Mechanical wording, metadata or path updates with settled intent.
   - One targeted check and result report, without root-cause investigation.
   These tasks MUST run in main; MUST NOT spawn an automatic reviewer, worker
   or availability probe merely to satisfy delegation.
3. LARGE/COMPLEX means at least one demonstrated condition: coordinated changes
   across dependent modules; broad code-path investigation or competing root-cause
   hypotheses; architecture/ownership/API/schema/migration decisions; meaningful
   async/state/race/cancellation, security, data-correctness or performance risk;
   broad/high-risk review needing an independent perspective; or substantial
   independent workstreams. Ordinary edits/tests across a few files alone do not
   prove complexity. Explain the concrete condition, not a generic risk label.
4. Complexity overrides simple examples: one-file concurrency/auth/shared-API
   work, config requiring system-wide tracing, and a destructive one-call
   operation needing impact assessment are not automatically simple. Existing
   approval/safety gates still apply; complexity is not permission to mutate.
   If relevant uncertainty remains after bounded inspection, classify complex
   unless scope/authority itself is unresolved; unresolved authority stops work.
5. Classify the whole requested task before model discovery, not every tool call
   or implementation slice. Do not split complex work to evade delegation, or
   inflate simple work to manufacture it. Reclassify only on material new scope
   or risk evidence; record it in existing task evidence, not a new tracker.
6. For large/complex work, exact native `greennode/glm-5.3` with
   `reasoning_effort=max` available means MUST delegate a meaningful bounded
   workstream or independent review pass. This is mandatory, not a preference.
   Main retains integration and acceptance. No per-slice repeated handoffs or
   duplicate investigation solely for compliance. No safe authorized scope or
   isolation -> stop for clarification; do not invent a handoff/local exemption.
7. Preserve native-only lookup, one documented lookup when unknown, no alternate
   client/provider/credential discovery, unavailable/unknown local handling,
   concrete failure evidence and bounded repair. Preserve explicit user model,
   transport and local-only overrides, including requested independent reviews
   of simple work; the prohibition concerns automatic delegation, not those
   overrides. Preserve the Claude one-level guard and existing external transport.
8. Preserve clean task context (`fork_turns: "none"` in Codex), fresh external
   sessions, no nested-agent workaround, cleanup, coordinator verification,
   HITL progress, approval, verification and closeout requirements. Do not
   reinterpret stuck tasks as simple; existing task-escalation-flow is unchanged.
9. Align frontmatter, UI metadata, gate/loop/composition/closeout text and active
   fixtures/tests. Remove blanket anti-simple rules and per-slice enforcement;
   record simple-main or complex-delegation decisions briefly in existing task
   evidence without requiring capability evidence for simple work.

## Done Criteria

- Add sanitized expected/negative/boundary feedback cases before skill edits.
- Matrix: simple config review, localized one-file edit, one read-only MCP call,
  small diff and targeted check remain main even with native GLM available;
  meaningful multi-module implementation and broad review delegate when available.
- Counterexamples: one-file state machine, risky config interactions, destructive
  one-call operation; ambiguity; scope growing from simple to complex; explicit
  delegate/local-only overrides; native unavailable/unknown/Flash-only; observed
  failure; unsafe isolation/unapproved scope; Claude depth guard; missing rubric.
- Update deterministic contract assertions to enforce both branches, reject
  blanket mandatory/per-slice rules, and preserve native-only/isolation locks.
- Check the new reference is in the registry and both consumers declare its
  companion dependency; test an incomplete subset without inventing a rubric,
  automatic installation or an unauthorized subset expansion.
- Run structural skill validation for the three changed skills and
  `uv run python -m unittest tests.test_mandatory_delegation_contract tests.test_skill_feedback_cases tests.test_skill_sync_scripts`;
  inspect diff, scope and links; perform a negative stale-rule check.
- One isolated forward-test covering the simple and complex routing decisions
  when available; report model/effort and actual observations. Scenario/text
  checks alone do not prove runtime adherence. Missing behavioral evidence must
  remain explicitly unverified, not replaced with a fabricated success.
- Record gap-finding results and required repairs; lifecycle remains unfinished
  until required criteria pass. No deployment claim without authorized sync.
- For behavioral testing, distinguish a model's routing decision from an actual
  handoff. A complex-case decision-only test is not proof that delegation ran;
  report that boundary explicitly and request any needed runtime authority.

## Out Of Scope

- Implementing skills/tests before SOW approval.
- Provider setup, CLI/relay changes,
  benchmarks, new orchestration frameworks or changing escalation policy.
- Changing SOW/Plan requirements, migration of old records or unrelated dirty work.

## Authorized Delivery

User approved implementation followed by scoped commit, push and sync of the
three changed skills to both Codex and Claude. This explicit delivery request
supersedes the draft's sync/push exclusion and single-target evolution default.
Publish only task-owned commits; sync from the committed artifact, excluding
unrelated dirty policy/Redmine changes. Verify installed parity against that
artifact, not the mixed working tree.

## Execution Evidence

- Classification: complex; coordinated routing contracts across three skills,
  shared packaging and regression assertions. Native catalog exposes
  router_greennode_glm_5_3 at max; delegated a non-overlapping implementation
  workstream with fork_turns none. Coordinator owns mixed-file integration,
  verification and delivery. No nested delegation.

### Integration Gap Check

| Severity | Finding | Impact | Solution |
| --- | --- | --- | --- |
| Medium | Delegate workflow, review evidence and Claude entry point retained old unconditional routing cues. | Simple tasks could still trigger capability checks or unnecessary handoffs. | Align all decision/evidence entry points with whole-task classification; worker repair requested. |
| Medium | Updated old fixtures lacked a distinct case for this correction and did not assert the shared rubric directly. | New one-file/MCP boundary behavior could regress while string checks pass. | Add stable current-feedback cases and direct rubric/packaging/companion assertions. |
| Low | Simple-task trigger exclusion did not explicitly mention user-requested delegation. | An explicit request could be rejected before reaching the override. | Exempt explicit user delegation at the trigger itself. |

All three integration findings were repaired. A subsequent code review also
caught an execution anti-stale assertion accidentally moved into the companion
test; it was restored before final verification. No required repair remains.

### Verification

- Coordinator reran focused modules: 21 tests PASS. Full repository discovery,
  `uv run --offline --no-sync python -m unittest discover -s tests`: 54 PASS.
- Skill-creator quick_validate: PASS for all three skills. JSON/manifest tests
  and `git diff --check`: PASS.
- Negative in-memory mutations: removing simple-main, weakening the complex
  mandate and restoring per-slice enforcement were each rejected by the
  execution contract test. No source files were mutated by these probes.
- Fresh independent forward-test requested `gpt-6-luna`, effort `max`,
  fork_turns none. It read the actual skills and rubric without expected answers
  or prior findings; eight independent routing cases matched the contract:

| Case | Raw task | Observed routing |
| --- | --- | --- |
| A | Config integer against known range | Simple-main, no discovery |
| B | Local one-file greeting literal change | Simple-main, retain exact approval check |
| C | One read-only issue-status MCP call | Simple-main, no discovery |
| D | Scheduler/cancellation/UI stale-result race | Complex, meaningful GLM workstream |
| E | One-file concurrent cancellation/disposal ordering | Complex, independent GLM analysis |
| F | One-call production deletion, unresolved blast radius/approval | Stop before mutation/model gate for authority |
| G | Simple config with explicit independent GLM reviewer request | Honor explicit delegation override |
| H | Local edit reveals unapproved shared API/cross-module impact | Stop scope expansion, update SOW before execution |

The forward-test proves observed routing decisions, not execution of its
hypothetical operations or handoffs. This implementation itself used a real
native delegated workstream with returned scoped changes; model selection is
recorded from the tool catalog, not inferred from generic self-identification.
No claim of end-to-end Claude/main-session adherence is made.

Final gap pass: contract, affected entry points, boundary cases, packaging and
ownership checked; existing approval/isolation/native-only/verification/HITL
contracts preserved. No actionable findings remain. Latency/token savings are
not benchmarked and are not a done criterion.

### Clean Delivery Candidate

Only task hunks were staged from mixed files. Readback caught one zero-context
staging insertion in the wrong execution phase; contextual staging repaired it
before commit. The final staged execution places simple-main in Phase 2 and
excludes unrelated Redmine edits. Remaining unstaged mixed-file diffs match the
pre-task policy/Redmine changes.

Exported the staged Git tree to a temporary clean candidate: all 54 tests and
all three structural validators passed there too. Checked Phase 2 placement and
absence of unrelated Redmine content in its execution skill. Remote fetched;
no pre-existing local-only commits would be included in the requested push.
The upcoming source commit is verified; requested delivery is still pending,
so this SOW remains IN_PROGRESS with finish_dttm null until sync readback.

### Delivery And Closeout

- Source commit: `5c1a914` (whole-task complexity routing), pushed to origin/main.
- Exported that committed revision and verified each of the three skill trees
  against its Git blobs before sync; no mixed working-tree source was used.
- Previewed then overwrote only sow-delegate-flow, task-execution-flow and
  task-review-investigate-compare under `~/.codex/skills` and `~/.claude/skills`
  using the existing imported sync API, followed by the existing copy verifier.
- All six installed copies have zero missing, extra or changed files relative
  to the committed source. Other skills/configuration were not changed.
- Implementation, required checks and authorized delivery are complete. Actual
  client skill discovery/reload and end-to-end Claude/main-session adherence
  were not exercised; file parity is not a claim of those runtime behaviors.
- No actionable finding or required repair remains; preserve all unrelated
  pre-existing dirty policy/Redmine files. Close this standalone bundle under
  the existing finished lifecycle.

## Cautions / Risks

- File/tool counts are examples, not sufficient complexity tests.
- Broad labels could classify every task complex; require concrete evidence.
- A shared rubric must remain discoverable across separate harness installations.
- Old tests currently demand delegation of simple tasks; update their intended
  assertions, do not merely weaken coverage. Structural PASS is not model proof.

## References

- [Execution policy history](../../finished/SOW_20261001_ZJDHWCVU/SOW_20261001_ZJDHWCVU_EXT_U8XRPS06_mandatory_glm53_delegation.md)
- [Delegate](../../../skills/sow-delegate-flow/SKILL.md)
- [Execution](../../../skills/task-execution-flow/SKILL.md)
- [Review](../../../skills/task-review-investigate-compare/SKILL.md)

## Review Record

### Round 1 - Self-Review

Compared proposed scope with the three skills, Claude role reference, discovery
metadata, mandatory contract assertions and matching feedback cases.

| Severity | Finding | Impact | Solution |
| --- | --- | --- | --- |
| Medium | Loading the delegate-owned classification resource could be confused with activating its mandatory delegation gate. | Simple tasks could still probe/delegate before classification. | Lock reference reading as non-activating and require classification before discovery; patched Deliverable 1. |
| Low | A forward-test reporting a complex routing decision could be presented as an actual delegation test. | Verification would overstate runtime evidence. | Separate decision evidence from actual handoff evidence explicitly; patched Done Criteria. |

Both findings patched; no remaining self-review blocker. Independent review
recorded below; review does not grant implementation approval.

### Round 2 - Independent Review

Fresh native reviewer selected through `router_greennode_glm_5_3`, requested
reasoning effort `max`, `fork_turns: "none"`, read-only scope. Returned findings
were checked against registry content, the exact-file manifest assertion in
`tests/test_skill_sync_scripts.py`, and subset installation instructions.
No runtime tests ran. The agent self-reported a generic GPT-5 identity and
unexposed effort, conflicting with the selected role; exact backend identity is
not independently verified. This is a completed independent review, not verified
GLM model provenance or implementation approval.

| Severity | Finding | Impact | Solution |
| --- | --- | --- | --- |
| High | New rubric file was excluded from the registry scope. | Exact-file manifest tests fail and manifest-based installs omit the rubric. | Added the precise registry entry to Location, Deliverable 1 and acceptance checks. |
| Medium | Consumer-only subset installs lack the shared rubric. | Classification cannot resolve despite otherwise valid skill selection. | Require companion guidance in both consumers and install instructions; missing companion needs consent, never silent installation. |

Both findings patched in this SOW; no known remaining planning blocker after
coordinator reconciliation. The revised contract has not been independently
re-reviewed; implementation and behavioral adherence remain unverified.

## Progress

- progress_updated_dttm: 2026-10-15T12:37:24+07:00

| Item | Status | Evidence / Pending reason | Next action / Owner |
| --- | --- | --- | --- |
| T1: Draft contract | DONE | Current three skills, metadata, Claude reference and mandatory contract tests inspected; proposed scope recorded. | None / Coordinator |
| T2: Self-review | DONE | Scope/source/fixture review completed; two findings patched in Deliverable 1 and Done Criteria. | None / Coordinator |
| T3: Independent review | DONE | Independent static review returned two findings; coordinator verified evidence and patched SOW. Backend identity caveat recorded above. | None / Coordinator |
| T4: Implementation | DONE | Three skills, shared rubric, manifest/install guidance, metadata and fixtures integrated; gap repairs complete. | None / Coordinator |
| T5: Verification | DONE | 54 tests, three validators, three negative mutations and eight-case independent routing exercise passed; limits recorded. | None / Coordinator |
| T6: Delivery | DONE | Source 5c1a914 pushed; committed export synced to both clients; all six copies match exactly. | None / Coordinator |
