# SOW_20260918_9TYIE2MO - Public Repo Privacy Hardening And Planning Boundary

- Status: DRAFT
- Approval: pending user approval
- create_dttm: 2026-09-18T11:21:14+07:00
- create_date: 2026-09-18
- create_dttm_source: original_creation_datetime
- create_dttm_confidence: explicit
- create_dttm_evidence: `plan_todo/finished/SOW_20261008_VO3LKN0L/creation-date-evidence.json` (record: SOW_20260918_9TYIE2MO)
- approve_dttm: null
- finish_dttm: null
- legacy_id: SOW_0089
- legacy_path: plan_todo/SOW_0089_public_repo_privacy_hardening.md
- migrated_dttm: 2026-10-08T12:48:51+07:00
- legacy_title: SOW_0089 — Public Repo Privacy Hardening And Planning Boundary

## Preserved Contract And Historical Evidence

## Lifecycle

- Status: DRAFT
- Approval: pending user approval
- create_dttm: `2026-09-18T11:21:14+07:00`
- approve_dttm: `null`
- finish_dttm: `null`
- Proposed-By: Codex GPT-6
- plan: Standalone; follows the 2026-09-18 public-repository privacy audit
  after commit `1cfa34c`.

## Task

Harden the public `AISkills` repository against accidental private-data
disclosure by sanitizing local/internal references, defining a public versus
local-only planning boundary, and adding repository-level secret-artifact
guardrails without changing skill runtime behavior.

## Why

The remote `MaiHoangViet1809/AI-skills` is public. The audit found no
high-confidence credential, private-key, or token-shaped value in the current
tree or reachable history, but it did find:

- tracked absolute paths containing the local username and sibling project paths;
- public planning documents naming internal projects and operational contexts;
- no `.gitignore` protection for common secret, credential, key, database, or
  archive file classes;
- an untracked `SOW_0056` containing local `codex-router` paths that could be
  committed accidentally.

## Planning Boundary Decision

The repository remains public unless the user explicitly changes that decision.

- **Recommended public model**: keep only sanitized, public-safe `plan_todo/`
  history tracked and pushed; move genuinely private plans to a separate
  private repository or a path outside this repository.
- A tracked file cannot be reliably “committed local-only” on the same branch:
  Git pushes commits, not individual files. A local commit on `main` becomes
  part of the next push unless the branch is kept unpushed or sanitized into a
  separate publish branch.
- A local-only untracked draft such as `SOW_0056` may be protected with
  `.git/info/exclude`; that local rule must not be committed to the repository.
- Ignoring all of `plan_todo/` is an alternative contract, not a safe default:
  it would require removing the directory from the public index and would not
  erase its existing public history. Use it only after explicit approval.

## Evidence

- Remote visibility: GitHub API reports `private: false` for the `main` remote.
- High-confidence secret scan: no API-key-shaped token, cloud access key,
  GitHub/Slack token, private-key block, credential URL, or bearer token found
  in the current tree, tracked binary strings, or reachable history.
- Current tracked `.env.example` contains placeholders only.
- Current working tree contains no `.env`, credential file, private key, local
  database, dump, or backup file; the untracked `SOW_0056` is the exception for
  local-path exposure, not credential exposure.

## Governing Principles

- `AGENTS.md`: preserve unrelated dirty work, keep edits scoped, use relative
  planning references where possible, and verify at the claimed layer.
- DRY/KISS: prefer path sanitization and simple ignore rules over a new privacy
  service, telemetry path, wrapper, or repository automation layer.
- Public-repository boundary: anything committed to `main` and its history is
  treated as public; local-only state must not depend on an unpushed commit.

## Location

- `.gitignore`
- `README.md`
- `INSTALL_FOR_AGENTS.md`
- `AGENTS.md`, only for the planning-boundary rule if a durable policy location
  is needed
- `darwinSkill/AGENT_GUIDE.md`
- `darwinSkill/README.md`
- `skills/registry.json`
- `skills/INDEX.md`
- `skills/spark-connect-debug/agents/openai.yaml`
- `skills/spark-connect-debug/SKILL.md`
- `tests/test_skill_feedback_cases.py`
- `tests/test_skill_sync_scripts.py`
- `tests/skill_feedback_cases/spark-connect-debug.json`
- `plan_todo/finished/SOW_20260917_V7HK7IAU/SOW_20260917_V7HK7IAU_review_end_to_end_outcome_trace.md`
- `plan_todo/finished/SOW_20260707_UUCT82PT/SOW_20260707_UUCT82PT_agent_instruction_file_targets.md`
- `plan_todo/finished/SOW_20260726_U6CHXKMS/SOW_20260726_U6CHXKMS_concept_compliance_execution_gates.md`
- `plan_todo/finished/SOW_20260809_WG7I2GYO/SOW_20260809_WG7I2GYO_visual_ui_review_skill_evolution.md`
- `plan_todo/finished/SOW_20260814_8MOLMSUP/SOW_20260814_8MOLMSUP_review_exact_runtime_contract_evidence.md`
- `plan_todo/finished/SOW_20260916_YMKJ2DLF/SOW_20260916_YMKJ2DLF_skill_evolution_failure_diagnosis.md`
- `plan_todo/finished/SOW_20260917_ORJ5FJT4/SOW_20260917_ORJ5FJT4_spark_connect_debug_skill.md`
- Preflight may identify additional files, but modifying any file not listed
  here requires an explicit SOW extension before editing.
- This SOW; `plan_todo/active/SOW_20260915_P1ZCTCHY/SOW_20260915_P1ZCTCHY_codex_router_claude_cli_native_subagent.md`
  remains user-owned and untracked unless separately authorized.

## As-Is Diagram (ASCII)

```text
public origin/main
  -> tracked skills + planning history + darwinSkill docs
  -> local absolute paths and internal project references remain
  -> .gitignore covers build/cache outputs only
  -> git add . can include secret artifacts or local-only drafts
```

```text
local-only SOW draft
  -> untracked today
  -> no repository-level boundary prevents accidental staging
```

## To-Be Diagram (ASCII)

```text
public-repo preflight
  -> classify each artifact: public-safe | sanitize | private/local-only
  -> scrub local paths and confirmed internal disclosure
  -> keep only public-safe plan_todo history tracked
  -> protect secret-artifact classes in .gitignore
  -> run redacted current-tree + reachable-history scan
  -> scoped review -> commit/push only after approval and clean gates
```

```text
private/local-only draft
  -> outside tracked tree or local .git/info/exclude
  -> never represented by a local-only commit on the pushed main branch
```

## Deliverables

1. **Public/private inventory**
   - Re-run a filename, path, URL, email, and internal-project scan over the
     current tree and reachable history.
   - Classify every confirmed finding as public-safe, sanitize-in-place, or
     private/local-only.
   - The preflight inventory is the effective write boundary. A newly
     confirmed finding outside `Location` requires an explicit SOW extension
     before editing.
   - Do not print, persist, or include secret values in the inventory.

2. **Path and project-reference sanitization**
   - Replace machine-specific absolute paths with repository-relative paths or
     neutral placeholders such as `/path/to/project` and `$HOME`.
   - Sanitize confirmed internal project/process references in public planning
     docs, preserving the procedural lesson while removing private context.
   - Public product/runtime terms such as `Spark Connect` remain in scope for
     sanitization only when they expose an internal project, owner, environment,
     or operational context.
   - Do not rewrite unrelated technical content or change skill behavior.

3. **Planning boundary policy**
   - Document that tracked public `plan_todo/` content must be public-safe.
   - Document that private plans belong outside this repo or in a separate
     private repository.
   - Keep `SOW_0056` out of the public commit unless its paths are scrubbed and
     the user explicitly authorizes adding it.
   - If requested, add only a local `.git/info/exclude` entry for that draft;
     never commit the local exclude file.

4. **Secret-artifact ignore guardrails**
   - Add narrowly scoped patterns for `.env`/local env files, credentials,
     private keys/certificates, local databases, dumps, backups, and archive
     artifacts.
   - Preserve an explicit exception for tracked `.env.example` templates.
   - Do not ignore source, docs, or public planning files broadly as a
     workaround for privacy classification.

5. **Redacted verification and closeout evidence**
   - Run a high-confidence secret scan over the current tree and reachable
     history with output limited to file paths, line numbers, categories, and
     remediation state.
   - Run `git diff --check`, inspect the final tracked/untracked boundary, and
     verify that no unrelated dirty files are staged.
   - Report remaining public-disclosure risk separately from credential risk.

## Done Criteria

1. Every confirmed absolute local path in the public scope is replaced with a
   relative path or neutral placeholder, or is explicitly documented as an
   intentional public example.
2. Public planning docs contain no confirmed private project/process detail
   beyond what the user has accepted as public; genuinely private material is
   moved outside the tracked public scope or separately approved for release.
3. `.gitignore` prevents accidental staging of the agreed secret-artifact
   classes while `.env.example` remains trackable.
4. `SOW_0056` is either kept local-only with no public commit, or is scrubbed
   and explicitly approved before tracking; no local-only commit is created on
   the pushed `main` branch.
5. The current-tree and reachable-history scan finds no unhandled
   high-confidence credential, token, private-key, or credential-URL finding.
   If a real secret is discovered, stop, report only its location/category,
   and require credential rotation before any push.
6. `git diff --check` passes, scoped files are reviewed, and unrelated dirty
   work remains untouched.
7. Closeout uses the finding table format and separates confirmed facts,
   sanitized public-disclosure risk, credential-scan evidence, and residual
   unverified scope.
8. No force-push or history rewrite is performed unless the user separately
   approves the exact commit/path impact and remote operation.

## Out-of-Scope

- Rotating credentials that are not found; if a real credential is found, stop
  and hand off the rotation as an explicit security action.
- Converting the GitHub repository from public to private without a separate
  user request.
- Broadly deleting or rewriting `plan_todo/` history without explicit approval.
- Modifying or committing the user-authored untracked `SOW_0056` without a
  separate ownership decision.
- Changes to skill selection, skill runtime behavior, telemetry, provider
  routing, external repositories, or installed Codex/Claude copies.
- Adding a new privacy service, secret store, hook framework, or dependency
  when a simple ignore rule and documented scan are sufficient.
- Reading, printing, or persisting `.env` contents or secret values.

## Cautions / Risks

- Scrubbing current files does not remove values already present in public git
  history; history removal requires a separately approved rewrite and force-push.
- A local `.git/info/exclude` protects only this checkout; it is not shared with
  collaborators or CI.
- `.gitignore` reduces accidental staging but is not a secret-management system.
- Internal project names may be intentionally public; classify them with the
  user-facing public/private decision rather than deleting them automatically.
- Regex and scanner output can miss encoded or provider-specific secrets; report
  the scan method and its residual limitations.

## Decision Log

Read the [binding extracted record](SOW_20260918_9TYIE2MO_decision.md) before execution; original authority is preserved there.

## Approval Gate

Before implementation, the user must approve this SOW and confirm the planning
boundary choice:

- **Option A (recommended)**: keep sanitized public `plan_todo/` content tracked;
  keep private plans outside this repo; keep `SOW_0056` local-only.
- **Option B**: make all of `plan_todo/` local/private, requiring index removal,
  a repository policy change, and explicit acceptance that existing public
  history remains unless a separately approved rewrite is performed.

No implementation, commit, push, history rewrite, or installed-environment sync
is authorized by this draft alone.
