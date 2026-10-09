# SOW_20261001_ZJDHWCVU_EXT_23PA4E5R - Native-Client GLM Gate

- Status: COMPLETED
- Approval: Approved by user; implement, commit, push and sync Codex/Claude.
- Proposed-By: Codex
- create_dttm: 2026-10-09T04:59:07+07:00
- approve_dttm: 2026-10-09T09:29:22+07:00
- finish_dttm: 2026-10-09T09:43:20+07:00
- Parent: [SOW_20261001_ZJDHWCVU](SOW_20261001_ZJDHWCVU_task_execution_delegate_preference.md)
- Order: Second EXT; narrows the automatic availability rule of
  [EXT_U8XRPS06](SOW_20261001_ZJDHWCVU_EXT_U8XRPS06_mandatory_glm53_delegation.md).
  Explicit user approval now authorizes this scope and parent reopening.

## Task / Why

Limit mandatory GLM delegation to the current client's native sub-agent
capabilities. User reports Claude Code searches for GLM, then discovers Codex
as an external client, wasting time. Source rules permit native catalog OR
provider transport; this is a contract defect, not proven non-loading.

## Location

- `skills/sow-delegate-flow/SKILL.md` and
  `skills/sow-delegate-flow/agents/openai.yaml`.
- `skills/task-execution-flow/SKILL.md` and
  `skills/task-execution-flow/agents/openai.yaml`.
- `skills/task-review-investigate-compare/SKILL.md` and
  `skills/task-review-investigate-compare/agents/openai.yaml`.
- Corresponding entries only in `skills/registry.json` and `skills/INDEX.md`
  if discovery text requires alignment.
- Corresponding three `tests/skill_feedback_cases/*.json` files and
  `tests/test_mandatory_delegation_contract.py`.
- This EXT and parent lifecycle/order/reference updates; approved reopening
  and closeout move the whole bundle and repair affected incoming links.

## As-Is / To-Be (ASCII)

```text
as-is: auto gate -> native catalog OR external provider/client search -> GLM
to-be: auto gate -> current client's native capability only
                  -> exact GLM + max supported: delegate natively
                  -> no native target/interface/max support: local execution
explicit user-selected external delegation -> existing explicit route
Codex -> selected Claude Code delegation -> existing fresh CLI session
Claude Code -> no native GLM -> local (no reverse Codex search)
```

## Deliverables / Behavior Locks

1. Automatic execution, review and open-model delegation inspect only the
   active client's exposed native catalog and supported reasoning efforts.
   Exact `greennode/glm-5.3` plus max, or a currently registered native role
   proven to map to that identity/effort, remains mandatory when available.
   Custom-provider models exposed natively qualify; branding alone does not.
2. When native delegation is unsupported or the exact target/max capability is
   absent, record a short `native-unavailable` reason and continue locally.
   Use that same label with the specific reason: interface unsupported,
   exact model absent, or max effort unsupported; do not invent more states.
   An unavailable catalog is not proof of model absence: use at most one
   documented native capability lookup, or record `native-capability-unknown`
   and continue locally without claiming absence or requesting a GLM setup.
3. Automatic GLM gating MUST NOT search other installed clients, Codex CLI/app,
   Claude CLI, routers, provider endpoints, credentials or external catalogs;
   no cross-client launch, installation, configuration or repeated probing.
   Claude Code without native GLM continues locally even if Codex has GLM.
   This restriction is scoped to automatic GLM enforcement, not a blanket ban
   on cross-client delegation: the existing Codex -> Claude Code route remains
   allowed when Claude is selected under its governing user/skill contract.
   Do not select Claude merely to replace missing native GLM or infer a new
   automatic Claude default from this exception.
4. Explicit human model/transport selection still wins. A user-requested
   external GLM/Claude delegation retains its documented fresh-session route;
   failure is reported without silently substituting a model. Automatic native
   launch failures retain bounded repair/local-fallback evidence and cleanup.
5. Preserve task isolation, exact model/max checks, coordinator verification,
   scope/approval gates and existing dirty edits. Use `fork_turns: none` for
   Codex `spawn_agent`; other native interfaces retain their documented
   equivalent clean-context guarantees. Do not require a Codex-only argument
   on another client or discover Codex to satisfy it. Unproven isolation still
   rejects the handoff under the existing failure/local-fallback rule.
   Do not make non-native availability a blocker for automatic local execution.

## Done Criteria

- All three flow rules, execution-loop decision point and relevant discovery
  wording agree; no automatic external GLM provider/client discovery remains.
- Sanitized expected/negative/boundary fixtures: native GLM+max delegates;
  Claude Code without GLM stays local; Codex on disk is ignored; max absent or
  catalog unknown stays local with truthful evidence; explicit external
  delegation and selected Codex -> Claude Code delegation remain available;
  neither becomes an automatic substitute for missing GLM. Native
  failure/isolation checks remain intact, including non-Codex native interfaces
  that isolate tasks without a `fork_turns` parameter.
- Deterministic assertions distinguish `native-capability-unknown` from
  confirmed `native-unavailable`, cover each absence reason and enforce at
  most one native lookup. Negative fixtures reject discovering/launching
  Codex merely to satisfy `fork_turns` on another client's native interface.
- Structural validators and targeted/full package tests pass; inspect mixed
  diffs to preserve unrelated edits. Static contract tests do not prove actual
  Claude Code behavior; label unavailable host-runtime proof unverified.
- Gap check and closeout evidence recorded; no installed-skill sync or push
  without a separate explicit request.

## Out Of Scope / Risks

- No new model discovery tool, transport, router/client setup or dependencies.
- No weakening of explicit external delegation or existing isolation guards.
- No unrelated policy/bootstrap edits, broad staging or historical rewrites.
- Product principles: DRY/SOLID/KISS; reuse native capabilities and existing
  fixtures. No root principle document or declared concept authority was found
  in the prior repository preflight; re-check before implementation.

## Preflight Evidence

- Read all three source gate sections and existing EXT; found the same native
  OR provider-transport path in each. Current gate tests: 6/6 PASS, establishing
  only the old contract. User-reported Claude behavior is not independently run.
- Working tree has unrelated policy/bootstrap and skill edits; preserve them.
- Explicit user approval subsequently authorized implementation and delivery.

## Review Resolution (Before Approval)

- One independent GLM-5.3-max pass with `fork_turns: none`, plus coordinator
  consolidation. Metadata paths are now explicit; capability labels/reasons
  and deterministic negative-test requirements clarified. The coordinator
  also scoped `fork_turns` to Codex without weakening other clients' isolation.
- Draft links and whitespace checked. This is contract review only; changed
  skill behavior and actual Claude Code runtime remain unverified. No skills,
  tests, approval state, commit, push or installed copies changed.

## Implementation / Verification

- Implemented native-only automatic gates in all three flows and discovery
  metadata. Explicit external selection and selected Codex -> Claude remain;
  absence/unknown no longer trigger cross-client GLM searches. Registry/index
  wording needed no changes; unrelated working-tree edits remain excluded.
- Delegation: isolated native GLM-5.3-max worker owned fixtures/tests; another
  isolated GLM-5.3-max reviewer read the clean candidate without golden cases.
  Coordinator retained implementation, verification and delivery ownership.
- Clean HEAD-based candidate with only approved source/test changes:
  `uv run --project <repo> --no-sync --offline python -m unittest discover -s tests -q`
  passed 47/47. Three skill structural validators passed; whitespace check passed.
  Initial isolated environment lacked PyYAML; rerun used the existing repo
  environment without adding dependencies. Two deliberate negative checks
  rejected missing unknown-state wording and restored legacy external discovery.
- Forward simulation covered six branches: Claude native absence, Codex exact
  target/max, inconclusive catalog, max unsupported, equivalent non-Codex
  isolation, explicit selected Claude route. Traces matched behavior locks;
  these are simulated decisions, not actual Claude host runtime evidence.
- Gap check found generic `fork_turns` wording in diagram/workflow/prompt.
  Repaired all occurrences to distinguish Codex from other native clients;
  added negative assertions and reran the clean candidate: 47/47 PASS.
  No remaining actionable findings found in the scoped contract inspection.
- Residual unverified scope: actual Claude Code automatic behavior and external
  CLI route were not exercised. Native GLM delegation itself ran successfully
  in this Codex session. This completes skill packaging/contract scope, not a
  claim of verified behavior on every host.
- Delivery authorized: scoped commit -> push -> sync exactly these three
  committed skills to Codex and Claude; exclude unrelated dirty edits.
