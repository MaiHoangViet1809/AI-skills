# SOW_0073 - Concept Compliance Execution Gates

- **Status**: done
- **Approval**: approved (user, 2026-07-26)
- **Task**: Make recorded project concepts mandatory implementation authority by adding concept compliance to the portable SOW contract and enforcing preflight and closeout gates through the task skills.
- **Location**:
  - `AGENTS.md`
  - `TEMPLATE_AGENTS.md`
  - `skills/task-router-flow/SKILL.md`
  - `skills/task-router-flow/references/scope-of-work.md`
  - `skills/task-review-investigate-compare/SKILL.md`
  - `skills/task-execution-flow/SKILL.md`
  - relevant skill metadata only when its description must change
  - `plan_todo/SOW_0073_concept_compliance_execution_gates.md`
- **Why**: Recorded concepts currently guide design but do not form a mandatory execution contract. An implementation can therefore introduce a conflicting abstraction without declaring that it changes project authority.

## As-Is Diagram (ASCII)

```text
concept catalog
      |
      +---- optional reading

approved SOW
      -> implementation
      -> verification
      -> closeout

Result:
implementation may drift without declaring a concept change
```

## To-Be Diagram (ASCII)

```text
concept authority
      |
      v
SOW: Concept Compliance
      |
      v
task-execution preflight
  -> read applicable concepts
  -> reject missing/conflicting mapping
      |
      v
implementation
      |
      v
task-execution closeout
  -> compare diff with declared concepts
  -> update changed concepts in the same SOW
  -> reject silent drift
      |
      v
verified closeout
```

## Deliverables

- Add a portable concept-authority rule to `AGENTS.md` and
  `TEMPLATE_AGENTS.md`:
  - concept enforcement activates only when the target repository has a
    canonical concept catalog or concept-authority document;
  - recorded project concepts are implementation authority while that gate is
    active;
  - implementation must follow them unless an approved SOW explicitly declares
    a concept change;
  - concept changes and their implementation belong to the same SOW;
  - a SOW must never silently override, bypass, or postpone its concept update.
- Add explicit portable Project Overrides keys to `AGENTS.md` and
  `TEMPLATE_AGENTS.md` so discovery is deterministic:
  - `Concept authority docs:`
  - `Concept authority index:`
  - skills may only activate concept-specific SOW fields and execution gates
    from these declared authority locations or from an equivalent repository
    documented canonical concept index;
  - if neither key nor canonical concept index exists, concept-specific routing,
    SOW fields, preflight, and closeout checks are skipped.
- Define generic concept-authority discovery without hardcoding one product
  repository:
  - prefer concept paths declared by the target repository in `AGENTS.md`
    Project Overrides;
  - otherwise accept a repository-documented canonical concept index;
  - do not infer a concept catalog from arbitrary design notes, historical
    plans, or finished SOWs;
  - when no concept authority exists, skip concept-specific SOW fields,
    preflight, and closeout checks without changing the existing workflow.
- When concept authority exists, extend the required code-change SOW definition
  with a concise `Concept Compliance` section:

```md
## Concept Compliance

- Applicable Concepts: <stable IDs or authority paths, or None with rationale>
- Concept Change: No | Yes
- Required Concept Updates: <None or exact concept IDs/files and intended change>
```

- Keep the contract portable:
  - project-specific concept locations and ID conventions remain Project
    Overrides;
  - repositories without concept authority are explicitly unaffected;
  - `None` is allowed only after concept authority was detected and requires a
    concrete task-specific rationale, so it cannot become an automatic bypass.
- Update `task-router-flow` so every code-change SOW:
  - first determines whether concept authority exists;
  - requires `Concept Compliance` only when that authority exists;
  - identifies applicable concepts before approval;
  - distinguishes following a concept from changing one;
  - routes undeclared conflicts back to authority review.
- Update `skills/task-router-flow/references/scope-of-work.md` so the portable
  SOW template itself includes `Concept Compliance` only when concept
  authority exists.
- Update `task-review-investigate-compare` so SOW and implementation reviews:
  - leave concept compliance out of scope when the repository has no concept
    authority;
  - treat missing or false concept mapping as an actionable finding;
  - patch low-ambiguity SOW mapping gaps;
  - route material concept changes for explicit approval.
- Add two explicit gates to `task-execution-flow`:
  - when concept authority exists, **Concept Preflight** before implementation
    reads mapped concepts, extracts invariants and forbidden designs, and stops
    on missing or conflicting authority;
  - when concept authority exists, **Concept Closeout** after gap-finding
    compares the final diff with the SOW mapping, requires same-SOW concept
    updates when semantics changed, and blocks completion while drift remains;
  - when concept authority does not exist, both gates are skipped rather than
    simulated through another document type.
- Preserve the existing SOW-first, verification, gap-finding, commit, and
  finished-file lifecycle.
- Record the activation and negative walkthroughs directly in this SOW under a
  dedicated verification section so the evidence has a fixed location.

## Done Criteria

1. Both portable AGENTS contracts define concept authority and the required
   `Concept Compliance` SOW fields consistently, including the exact Project
   Overrides keys used for authority discovery.
2. Router, review, and execution skills use the same terms and decision rules.
3. Repositories without concept authority do not gain mandatory concept fields
   or concept-specific execution gates.
4. When concept authority exists, execution cannot proceed if a concept-covered
   implementation lacks a valid mapping or conflicts with its declared
   concepts.
5. When concept authority exists, execution cannot close if the implementation
   changed a concept but the approved SOW and concept files were not updated
   together.
6. A declared concept change requires explicit SOW approval; updating an
   existing SOW does not require another SOW.
7. Skill validation and repository scans find no contradictory legacy wording.
8. `skills/task-router-flow/references/scope-of-work.md` includes the same
   conditional `Concept Compliance` contract used by the skills.
9. A documented activation walkthrough inside this SOW proves a repository
   without concept authority follows the existing execution flow unchanged.
10. A documented negative walkthrough inside this SOW proves that a silent architecture drift,
   such as introducing an undeclared root-manifest model, is stopped by the
   preflight or closeout gate.

## Verification Walkthroughs

### Activation Walkthrough: Repo Without Concept Authority

1. Read `AGENTS.md` Project Overrides.
2. If `Concept authority docs:` and `Concept authority index:` are both unset
   and no canonical concept index is documented, router omits `Concept
   Compliance`.
3. Review and execution skills skip concept-specific mapping, preflight, and
   closeout gates.
4. Existing SOW-first execution flow remains unchanged.

### Negative Walkthrough: Silent Drift Under Concept Authority

1. A target repository declares concept authority through Project Overrides or
   a canonical concept index.
2. A code-change SOW omits `Concept Compliance`, declares a false mapping, or
   changes concept semantics without same-SOW concept updates.
3. `task-router-flow` stops approval-ready routing until the mapping is fixed.
4. `task-review-investigate-compare` reports the gap and patches it only when
   low-ambiguity; otherwise it routes for explicit approval.
5. `task-execution-flow` blocks implementation at Concept Preflight or blocks
   completion at Concept Closeout while drift remains.

## Out-of-Scope

- Building a standalone validator, CI job, hook, or orchestration process.
- Implementing AgentHangar enforcement; AgentHangar may later extract these
  gates into an independent process.
- Changing any product project's concept catalog or implementation.
- Defining project-specific concept IDs inside the portable skills.
- Requiring a second SOW merely to update an existing SOW or its concept
  declaration.

- **Proposed-By**: Codex GPT-5
- **Plan / Reference**: Portable concept-governance extension of the existing
  SOW-first task workflow.

## Cautions / Risks

- A permissive `None` value could become a bypass; router and reviewer must
  require a concrete rationale after concept authority has been detected.
- Over-broad discovery could misclassify historical design notes as canonical
  concepts; activation must rely on repository-declared authority.
- Repeating full concept documents inside SOWs would create competing
  authorities; SOWs should reference concepts and describe only intended
  changes.
- Concept checks must not become a standalone validator disguised inside the
  skill; this phase is procedural enforcement only.
- Closeout must distinguish implementation drift from harmless wording or
  formatting changes.
- Project-specific paths must stay in Project Overrides so the AISkills
  contract remains reusable.
