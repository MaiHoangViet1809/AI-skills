# SOW_0090 - Review And Refine TEMPLATE_AGENTS.md

- **Status**: completed
- **Approval**: approved by user in the current task with the instruction “approve, làm SOW 090 giúp tôi”
- **create_dttm**: 2026-09-18T15:47:07+07:00
- **approve_dttm**: 2026-09-18T16:17:24+07:00
- **finish_dttm**: 2026-09-18T16:19:42+07:00
- **Task**: Review and refine the portable `TEMPLATE_AGENTS.md` contract for completeness, enforceability, and concise genericity, then mirror approved policy changes into `AGENTS.md`.
- **Location**: `TEMPLATE_AGENTS.md`, `AGENTS.md`, `plan_todo/skill_design_decisions.md`, `plan_todo/finished/SOW_0090_template_agents_hardening_review.md`
- **Why**: The shared policy must be strict enough that installed skills, SOWs, plans, and verification flows behave consistently across repositories without adding unnecessary context or project-specific rules.
- **Proposed-By**: Codex
- **plan**: `N/A`

## As-Is Diagram (ASCII)

```text
target repository
  -> agent reads AGENTS.md and applicable project rules
     -> routes task and applies SOW / verification policy
        -> current template has strong core guardrails
           -> some artifact coverage, conflict handling, and wording density remain unclear
```

## To-Be Diagram (ASCII)

```text
target repository
  -> agent reads AGENTS.md, principle authority, and applicable rules
     -> resolves conflicts explicitly or stops for clarification
     -> distinguishes code/config/runtime changes from docs-only work
        -> requires approved SOW before code/config/dependency/runtime changes
     -> executes only within scope
     -> verifies, performs negative check, and reports evidence
        -> one portable policy source without duplicated or project-specific rules
```

## Review Evidence And Vote

The coordinator and all three requested reviewers returned reviews: GLM-5.2
(`max`), GLM-5.3 Flash (`max`), and Astra (`low`). These were context-aware,
not blind independent reviews: `fork_turns: all` and the shared SOW exposed
the review arrangement. Some responses drifted into coordination. GLM-5.3
Flash's claim of additional delegated reviews is unverified and is not counted.

Votes below mean a reviewer explicitly raised the topic, not that it approved
the exact proposed wording. A dash means not raised, not a rejection. The line
references below point to the current 341-line post-patch policy. User decisions
take precedence over vote counts.

| Finding / current policy lines | GLM-5.2 | GLM-5.3 Flash | Astra | Disposition |
| --- | --- | --- | --- | --- |
| Authority and root/nested policy conflicts, 21, 42-51, 307-341 | Yes | Yes | Yes | Required; follow the active tool's instruction hierarchy and declared project scope, without inventing a provider-independent precedence order. |
| Explicit artifact coverage, 93-96 | Yes | Yes | Yes | Required clarification; name manifests, lockfiles, migrations, CI/deployment config and API/schema contracts. Existing config/contracts already cover some of these. |
| Actual approval versus editable status marker, 98-109, 300-303 | - | Yes | Yes | Required; actual user/authorized-approver approval must back the record. No agent self-approval. |
| Expanded implementation scope needs approval, 135-139 | - | - | Yes | Required, coordinator-confirmed gap; updating a SOW alone does not approve its extension. |
| Portable policy filename and complete rule discovery, 21, 34-40 | - | - | Yes | Required for existing cross-agent adoption scope. |
| Concrete verification evidence and applicable closeout, 233-254 | - | Yes | Yes | Required; preserve evidence while keeping docs-only closeout proportional. |
| Secret handling beyond hardcoding, 216-219 | - | Yes | - | Include bounded clarification; no new secret-scanning mechanism. |
| Overlapping abstraction rules and 172-177 | - | - | Yes | Include targeted consolidation preserving genuine-complexity/testing exceptions. |
| Tool cache versus external runtime output, 192-197 | - | - | Yes | Include boundary clarification; no blanket external-write exemption. |
| Version/date marker | Yes | - | - | Defer; Git history suffices for this change. |

## Proposed Patch Contract

1. **Approval and scope**: record the actual approving instruction or reference
   and approver when known. `IN_PROGRESS` is valid only with retained approval
   evidence; a status/marker alone never grants authority. Review approval does
   not imply implementation approval. Require approval of expanded code scope
   before implementing it, including regression extensions. For completed SOWs,
   retain original completion evidence and record the new extension's approval
   and verification separately within the existing lifecycle convention.
2. **Authority and discovery**: refer to "this policy file" and applicable
   ancestor/nested instruction files recognized by the active agent. Read
   `PRODUCT_PRINCIPLE_DESIGN.md` when present and `.agents/rules/` indexes,
   globally applicable rules, and task-relevant rules. Inspect rule content
   when filenames are insufficient; ask only when a material conflict remains
   unresolved after applying the tool hierarchy and declared project authority.
   A user-approved exception already in context must not trigger repeated asks.
3. **Code versus docs**: clarify code/config/dependency/runtime artifact coverage
   in the existing SOW gate. Keep docs-only edits exempt unless they change
   approved implementation scope. Editing policy, design docs, SOWs, or approval
   markers cannot itself authorize code execution or an exception. Do not add a
   duplicate Definitions block or routing diagram already owned by task routing.
4. **Verification**: retain commands or named manual checks, outcomes, failures,
   and unavailable checks in the SOW or closeout. Apply SOW done criteria only
   when a SOW governs the task. Distinguish implemented, simulated and unverified
   outcomes without requiring empty sections. API-only checks cannot establish
   rendered UI correctness. No claim of cross-provider behavior from text review.
5. **Secrets**: prohibit exposing or persisting secrets in logs, output, commits,
   or transmitted diagnostics; redact evidence. Do not inspect secret-bearing
   file contents without explicit task authorization. Ordinary authenticated
   tool use does not imply permission to inspect credentials.
6. **Concision and boundaries**: consolidate redundant abstraction bullets;
   apply the 2+ rule to extraction for reuse, preserving genuine complexity and
   necessary testing exceptions. Keep the full SOW field list; diagrams may be
   `N/A` with rationale when neither behavior nor architecture changes. Clarify
   that ordinary tool-managed caches/temp files for authorized checks differ
   from task-created persistent runtime outputs or deployment outside the repo.
   Preserve approval requirements for the latter and do not extend the cache
   clarification to global installs, configuration, or skill sync.

## Preserved And Rejected Decisions

- Preserve the full SOW template, conditional concept authority, Git safety,
  `NEVER create empty files`, and the `__init__.py` prohibition/explicit exception
  gate in the generic policy. Keep the existing conditional `uv` convention.
- Reject moving those bans to Project Overrides or weakening them for portability.
- Reject requiring a SOW for every policy/prompt/Markdown edit. The earlier chat
  consolidation overstated that proposal; docs-only exemption remains in force.
- Reject a universal "nested always wins" precedence rule and "only APPROVED
  status can execute" rule; neither follows from the existing contract.
- Defer arbitrary line-count targets, new version metadata, an adapter lifecycle
  framework, and a separate glossary of vague terms. Clarify relevant wording
  in place without adding mechanisms or unrelated policy requirements.

## Deliverables

- One coordinator review summary.
- Three model review summaries represented by the evidence/vote table above,
  with their context-contamination limitation disclosed.
- The concrete proposed patch contract and preserved/rejected decisions above.
- After explicit approval, a focused patch to `TEMPLATE_AGENTS.md` and the identical `AGENTS.md` copy.
- A decision-log update only when the patch changes a durable policy decision.

## Done Criteria

- All three requested reviewer outputs are accounted for; additional unverified
  reviews are not counted and topic agreement is not presented as blind consensus.
- Coordinator review checks coverage, conflict handling, enforceability, portability, and context cost.
- Findings identify exact template lines and distinguish confirmed gaps from preferences.
- Template edits occurred only after the user's explicit approval was recorded
  in this SOW.
- Check the resulting text against these manual scenarios: docs-only edit needs
  no SOW; fabricated approval grants no authority; previously approved in-progress
  work can continue; an unapproved scope extension cannot; approved exceptions
  are not asked for again; policy editing does not approve code work; a global
  rule with a non-obvious filename is discovered; tool caches do not authorize
  global installs; an API check is not reported as rendered UI verification.
- Preserve all existing required SOW fields and the empty-file/`__init__.py`
  bans; introduce no duplicate task-routing framework or automatic concept gate.
- After approval and patching, `cmp -s TEMPLATE_AGENTS.md AGENTS.md` passes.
- After approval and patching, `git diff --check` passes. Inspect untracked SOW
  whitespace separately because ordinary Git diff omits it. Stage nothing unless
  a commit is requested, and then stage only task-owned changes, including hunks
  in the already-dirty decision log.
- The final summary separates implemented, not implemented, and unverified items and references this SOW.

## Out-of-Scope

- Source code, tests, scripts, configuration, runtime contracts, generated code, dependency manifests, or lockfiles.
- Changes to any skill body, skill registry, installer, synchronizer, hooks, telemetry, or installed agent environment.
- Creating a new `create-agents-md` skill or changing policy distribution behavior.
- Rewriting existing unrelated dirty files or untracked SOWs.
- Commit or push unless the user explicitly requests it after review and patch approval.
- Additional delegated review runs or changes to delegation tooling.

## Cautions / Risks

- `AGENTS.md` and `TEMPLATE_AGENTS.md` must remain identical after an approved policy patch.
- A shorter policy must not remove strict SOW gates, principle-authority checks, verification, or Git safety.
- Reviewer recommendations may conflict; the coordinator must preserve evidence and avoid majority-vote changes that violate repository policy.
- The current worktree contains unrelated modifications; inspection and staging must remain file-scoped.

## Implementation Verification

- `cmp -s TEMPLATE_AGENTS.md AGENTS.md`: passed.
- `git diff --check`: passed for tracked changes; the untracked SOW was checked
  separately for trailing whitespace and passed.
- Manual structural scenarios passed: docs-only work remains SOW-exempt;
  fabricated status does not grant approval; approved active work is allowed;
  unapproved scope extensions are blocked; approved exceptions are not repeated;
  policy editing does not authorize code; globally applicable rules are read;
  tool caches do not authorize global installs; API evidence is not UI evidence.
- The first negative assertion was overly broad because it matched `skill` in a
  path name; the assertion was narrowed to forbidden file names and passed.
- No template or decision-log runtime behavior was changed. Cross-provider agent
  adherence remains unverified by this text-only implementation.

## Final Review

- Implementation and coordinator final review completed on 2026-09-18 after the
  user's approval. The template patch is mirrored exactly into `AGENTS.md`.
- The final policy preserves the full SOW field list, docs-only exemption,
  conditional concept authority, Git safety, empty-file and `__init__.py`
  prohibitions, and existing toolchain conventions.
- No actionable findings found. Remaining risk is provider-specific behavior,
  which requires exercising each agent's actual instruction loader.
