# Skill complexity audit

Scope: all 14 skills registered in `skills/registry.json`; entrypoint review and
relevant workflow references. Not an audit of every bundled script, third-party
plugin or system skill. All 14 installed Codex entrypoints matched canonical
source at inspection; this is entrypoint parity, not full-package verification.

## Cause and evidence

Project `AGENTS.md` already requires KISS, reuse and no unnecessary wrappers.
Failure to apply those requirements is an agent execution failure. The skill
instructions below contribute conflicting incentives or leave gaps; source
inspection cannot prove which instruction caused every historical failure.

| Skill | Evidence | Finding and disposition |
| --- | --- | --- |
| task-router-flow | `SKILL.md:94–104`, Change Completeness Guardrail | Treats narrow scope as a tradeoff and encourages family-level fixes. Change inspection of adjacent code into evidence gathering; it is not authority to change adjacent code. Proposed SOW_0084 scope. |
| task-execution-flow | `SKILL.md:64–70,88–100,224–261` | Widen adjacent coverage; convert any gap into a repair; escalate only after three conditions. These can produce endless expansion and conflict with immediate authority stops. Classify in-scope defect, missing evidence and optional/out-of-scope enhancement first; preserve immediate authority stops. Proposed SOW_0084 scope. |
| task-review-investigate-compare | Comparison Frame and review/writeback rules | Complexity is a comparison dimension, not an approval condition. No required comparison with an existing simpler pattern or actual implementation drift. Proposed SOW_0084 scope. |
| task-poc-verification-flow | POC Code Review Checklist | Already forbids wrappers and encourages reuse, but does not require each added stage to prove the named hypothesis. A large custom runner can pass the checklist. Add a narrow proof-necessity check. Proposed SOW_0084 scope. |
| sow-delegate-flow | Rules and Flow steps 6–8 | Already preserves bounded scope and delegates verification to execution flow. Fix that owner; do not duplicate the full new checklist here. Existing portability issues belong to SOW_0082. |
| task-progress-report | Rules and Completion Discipline | Format/completion requirements can inflate reporting; not evidence of a code-generation cause. Inventory selection and duplicated completion rules already belong to SOW_0082. No new patch here. |
| skill-evolution-flow | Classify The Cause; Patch The Canonical Skill | Already requires the smallest general correction and prohibits installing unrelated skills. Preserve it; this audit must not become a blanket rewrite. |
| project-concept-governance-flow | Authority Activation; Mature Concept vs Inline Rule | Explicitly forbids inventing authority and inflating small rules into mature concepts. No actionable overengineering finding in the reviewed entrypoint. |
| datamart-design-review | Establish Authority; Report The Change; Mutation Boundary | Starts with current contracts and only requires the matrix for detailed impact reports. No actionable overengineering finding in the reviewed entrypoint. |
| apply-design-mirror | Workflow step 4 | Requires existing ownership and rejects redundant wrappers/themes. No actionable overengineering finding in the reviewed entrypoint. |
| extract-design-mirror | Workflow steps 3–6 | Requested deliverable is a design/evidence package; sampling is conditional. No evidence that its artifacts caused the migration failure. No patch. |
| verify-design-mirror | Workflow; Stop Conditions | Explicit verification artifact and read-only boundary fit its specialized request. No actionable overengineering finding in the reviewed entrypoint. |
| playwright-flow | Session cleanup | Default `close-all`/`kill-all` can affect other sessions. Concrete ownership defect, already scoped by SOW_0082; not a cause of migration code size. |
| taste-skill (design-taste-frontend) | `SKILL.md:9,46–57,267,531–534,912–914` | Contextual opening conflicts with mandatory dual mode, generated imagery and all-box completion. Potential unsolicited UI work; not evidence about this backfill. Record as a separate design-skill decision, without changing these imported design preferences under SOW_0084. |

## Interaction to repair

```text
router: adjacent scope should also be handled
  -> review: completeness without necessity gate
  -> execution: every gap becomes another repair
  -> POC review: safe/self-contained, but proof size not challenged
```

Replace those pressures with existing-baseline inspection, the smallest
sufficient implementation, and explicit separation of required repairs from
new work. Do not treat a documented failure as approval for a new subsystem.
Do not strip required safety or data semantics merely to reduce line count.

## Verification limits and next action

Read-only source and entrypoint comparison completed. No isolated model test,
production operation or skill implementation ran. Subagents are prohibited in
this side conversation. SOW_0084 carries the proposed four-skill correction;
SOW_0082 retains its existing ownership, reporting and portability fixes.
