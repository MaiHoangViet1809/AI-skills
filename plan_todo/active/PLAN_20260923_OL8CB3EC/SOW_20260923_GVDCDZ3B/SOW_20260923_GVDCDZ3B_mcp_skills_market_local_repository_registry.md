# SOW_20260923_GVDCDZ3B - MCP Skills Market With A Local Registered-Repository Registry

- Status: DRAFT
- Approval: null
- create_dttm: 2026-09-23T03:49:01+07:00
- create_date: 2026-09-23
- create_dttm_source: original_creation_datetime
- create_dttm_confidence: explicit
- create_dttm_evidence: `plan_todo/finished/SOW_20261008_VO3LKN0L/creation-date-evidence.json` (record: SOW_20260923_GVDCDZ3B)
- approve_dttm: null
- finish_dttm: null
- legacy_id: SOW_0093
- legacy_path: plan_todo/SOW_0093_mcp_skills_market_local_repository_registry.md
- migrated_dttm: 2026-10-08T12:48:51+07:00
- legacy_title: SOW_0093 - MCP Skills Market With A Local Registered-Repository Registry

## Preserved Contract And Historical Evidence

## Lifecycle

- **Status**: DRAFT
- **Approval**: null
- **create_dttm**: 2026-09-23T03:49:01+07:00
- **approve_dttm**: null
- **finish_dttm**: null
- **Proposed-By**: Codex
- **plan**: `plan_todo/active/PLAN_20260923_OL8CB3EC/PLAN_20260923_OL8CB3EC_mcp_skills_market_plan.md`

## Task

Design and implement a local, `stdio`-transport MCP service that lets an agent
explicitly register approved skill repositories, indexes only those
repositories, and discovers or returns their skills to Codex and Claude through
one shared protocol contract. Other MCP-capable hosts may consume the protocol,
but first-party verification in this SOW is limited to Codex and Claude.

## Why

The current skill distribution model assumes repository cloning and host-local
installation. A shared MCP catalog can make skills discoverable at task time,
but the catalog must remain user-controlled: it must not become an Internet-wide
skill crawler, silently import unapproved repositories, or mutate native host
skill directories. The selected design is a universal protocol over an explicit
local allowlist of registered repositories.

## Scope Boundary

This SOW covers the read/discover path and the explicit local registry mutation
needed to register, refresh, and remove skill repositories. It does not grant
authority to install skills into `~/.codex`, `~/.claude`, or another host's
native skill directory. It does not make `skills.sh` or any public catalog a
default source.

## Location

- `mcp_skills_market/` (new local MCP service and registry implementation)
- `tests/mcp_skills_market/` (unit, fixture, security, and protocol tests)
- `docs/mcp-skills-market-architecture.md` (architecture authority for this
  SOW's MCP service)
- `docs/mcp-skills-market.md` (operator and host configuration contract)
- `pyproject.toml` and `uv.lock` for the selected `mcp>=2,<3` dependency
- `plan_todo/active/PLAN_20260923_OL8CB3EC/SOW_20260923_GVDCDZ3B/SOW_20260923_GVDCDZ3B_mcp_skills_market_local_repository_registry.md`
- `plan_todo/active/PLAN_20260923_OL8CB3EC/PLAN_20260923_OL8CB3EC_mcp_skills_market_plan.md`
- `plan_todo/finished/mcp_skills_market_plan.md` (lifecycle destination)
- `plan_todo/finished/SOW_0093_mcp_skills_market_local_repository_registry.md` (lifecycle destination)

No existing skill body, native host installation, provider credential, or
unrelated planning artifact is in scope. Existing dirty files outside the
task-owned SOW and plan must remain untouched; the task-owned planning files
may be updated during review. Dependency manifest changes require this SOW's
runtime/dependency decision and remain limited to the listed manifests.

## Baseline Evidence

- The repository currently ships skills and a repository registry, but no
  `mcp_skills_market/` service or MCP registry implementation was found.
- The existing `skills/registry.json` records supporting files in some skill
  packages, so a discovery result must distinguish a `SKILL.md` entry from its
  registry-declared support bundle. A repository without this registry is not
  a supported source.
- The current Python project has no MCP SDK dependency; this SOW now selects the
  official `mcp>=2,<3` SDK and covers its dependency manifest updates.
- Current host distribution is file-based and host-specific; it is not a
  runtime discovery service.
- The decided source boundary is user-registered repositories only.
- A local MCP process is required for an MCP write operation to persist into
  local storage. A remote MCP endpoint cannot directly and safely write the
  user's filesystem.
- `skills.sh` may be consulted later for metadata, search, or audit design, but
  it is not an initial source provider.

## As-Is Diagram (ASCII)

```text
AISkills Git repository
  -> skill files + registry.json
  -> clone/copy/sync into a host-local skill directory
  -> host discovers installed files
  -> no shared runtime registry for user-approved external repositories
```

## To-Be Diagram (ASCII)

```text
user asks agent to add a repository URL
  -> local MCP register_repository()
  -> writable stdio profile stores canonical URL, ref, and pinned commit
  -> indexer validates skills/registry.json and discovers its declared packages
  -> discover_skills(query) searches the active profile's registered repositories
  -> read_skill(...) returns a bounded manifest-backed bundle + provenance
  -> Codex / Claude launch the same service contract with explicit profiles
```

## Design Decisions Locked By This SOW

1. **Universal protocol, not per-host marketplaces**: Codex and Claude use the
   same local MCP service contract. Each host may launch an isolated `stdio`
   process/profile; host-specific work is limited to MCP connection
   configuration, not skill catalog logic.
2. **Registered repositories are the source boundary**: no global Internet
   search and no automatic import from `skills.sh` or another public directory.
3. **Explicit local writes**: `register_repository`, `unregister_repository`,
   and `refresh_repository` are the only registry mutations. They are exposed
   only by an explicitly writable local profile; host approval/HITL policy must
   protect the mutation tools. The model must not be trusted to self-report a
   `user_confirmed` flag.
4. **Discovery is separate from installation**: the service returns matching
   skill metadata or a bounded manifest-backed bundle; it does not install into
   native Codex/Claude skill roots and does not execute repository scripts.
5. **Pinned and inspectable sources**: repository identity, requested ref,
   resolved commit, skill path, checksum, license, and fetch/index status are
   visible to the caller.
6. **Local topology**: v1 uses `stdio` only. A host starts the service with a
   configured state root and profile; shared registry files use locking and
   atomic replacement. A `localhost` daemon or hosted MCP service is not part of
   this SOW.
7. **Untrusted skill content**: returned skill text cannot override system,
   user, `AGENTS.md`, SOW, or host policy instructions and cannot authorize
   scripts, credentials, deployments, or unrelated file writes.
8. **Scope identity is process-bound**: a profile has a `scope` of either
   `global` or `project`. A project profile receives an explicit canonical
   `scope_root` at process startup; the model cannot choose or override it per
   call. Missing, non-canonical, or symlink-ambiguous scope roots fail closed
   with `scope_denied`. The launch `mode` (`readonly` or `writable`) is
   independent of scope; profile identity is the `(mode, scope)` tuple.
9. **Profiles do not fall through**: a project profile searches only its own
   registered repositories; it never inherits registrations from the global
   profile or another project profile.

## Tech Stack And Runtime Contract

- **Runtime**: Python 3.10+ managed by `uv`, matching the repository's existing
  toolchain.
- **MCP implementation**: the official Model Context Protocol Python SDK from
  `modelcontextprotocol/python-sdk`, installed as the PyPI package `mcp` with a
  major-version constraint `mcp>=2,<3`. This is the protocol SDK, not an
  Anthropic-, OpenAI-, Codex-, or Claude-specific client library. The exact
  resolved minor version is recorded in `uv.lock` during implementation.
- **Server API**: use the SDK v2 `MCPServer` with typed Python/Pydantic input
  and output models. The application entrypoint is the importable
  `mcp_skills_market.server:serve_stdio()` function. The SDK's CLI extra is a
  development/Inspector aid only; the runtime does not depend on `mcp[cli]`.
- **Transport**: `stdio` only in v1. Do not add FastAPI, Uvicorn, a localhost
  daemon, or a hosted HTTP endpoint to this SOW.
- **Repository ingestion**: invoke the system `git` executable through a
  controlled subprocess environment. Do not add GitPython, Dulwich, or a
  second Git implementation. Git credentials remain owned by the user's
  configured helper.
- **State storage**: use versioned JSON metadata and JSON index generations,
  atomic replacement, and a cross-process lock adapter. Do not use SQLite in
  v1; the registry is intentionally small, inspectable, and generation-swapped.
- **Tests**: use the repository's `unittest` convention plus the SDK's in-memory
  `Client(server)` path for protocol assertions. Use the SDK CLI/Inspector only
  for manual protocol smoke, not as the production runtime.

## MCP I/O Contract

- A host launches one child process and exchanges newline-delimited JSON-RPC
  messages over the child's stdin/stdout. The service writes protocol frames to
  stdout only; diagnostics, Git stderr, and audit-safe logs go to stderr.
- Every tool input is a typed model. The SDK publishes the JSON Schema and
  rejects invalid arguments before the handler runs.
- Successful calls return typed structured JSON in `structuredContent`, with
  the same compact JSON mirrored as model-readable text content. The
  `read_skill()` result contains skill identity, source/ref/commit, package
  path, license state, per-file checksums, and a bounded array of file records
  containing relative path, UTF-8 text, size, and checksum.
- Expected domain failures use the SDK tool-error path with a stable JSON error
  payload in the error content: `{ "error_code": "...", "message": "..." }`.
  Protocol-invalid input remains SDK schema validation. Unexpected exceptions
  are sanitized by the SDK and written with traceback only to stderr.
- MCP tools are the only v1 public surface. Do not add resources, prompts,
  arbitrary file reads, or a generic write tool until an SOW extension defines
  their ownership and security contract.

## Runtime State Storage

The service source lives in this AISkills repository, but runtime registry state
and Git caches do **not** live in Git and are not committed to the project.
`MCP_SKILLS_MARKET_STATE_ROOT` is the explicit parent directory. Defaults are:

- macOS: `~/Library/Application Support/AISkills/mcp-skills-market`
- Linux: `$XDG_STATE_HOME/aiskills/mcp-skills-market`, falling back to
  `~/.local/state/aiskills/mcp-skills-market`
- Windows: `%LOCALAPPDATA%/AISkills/mcp-skills-market`

The state layout is:

```text
<state-root>/
  profiles/<profile-id>/
    registry.json                 # registrations and active generation
    indexes/gen-<n>.json          # immutable trusted index generations
    repos/<repo-id>/repo.git/     # bare Git object cache, no checkout hooks
    staging/<operation-id>/       # candidate data, never served directly
    locks/registry.lock           # cross-process single-writer lock
```

`profile-id` is a stable hash of `(mode, scope, canonical scope_root)`; the
canonical root is empty for a global scope. State directories are created with
user-only permissions, registry/index files are not secret-bearing, and no
credential values or raw Git prompts are persisted. A project scope is isolated
by its profile hash and does not create a `.aiskills/` directory in the source
repository unless a future SOW explicitly chooses that deployment mode.

## Registered Repository Layout

The registered source is a Git repository addressed by canonical `https://` or
`ssh://` URL. The recommended layout is:

```text
repository-root/
  skills/
    <skill-id>/
      SKILL.md
      references/...
      scripts/...
  skills/registry.json                 # required manifest
  LICENSE                               # optional, reported as unknown if absent
```

The repository format is strict: `skills/registry.json` must exist, validate
against the supported schema, and declare every package. Each declared package
must contain one `SKILL.md`; additional support files must be explicitly
allowlisted by that registry. A repository without the registry, with a
malformed registry, with an undeclared package, or with an invalid package is
rejected and never indexed. Missing or malformed `skills/registry.json` returns
`index_failed`; malformed package metadata returns `invalid_skill`. Other
manifest sources are unsupported and cannot make an otherwise invalid
repository usable. There is no manifest-free `SKILL.md` scan. All paths are
repository-relative POSIX paths, cannot contain `..`, and must resolve inside
the package.

## Host Wiring And Startup

The service is started from this repository during v1; it is not globally
installed or copied into `~/.codex` or `~/.claude`. After implementation, the
direct smoke command is:

```text
uv run --project <AISkills_ROOT> python -m mcp_skills_market.server
```

Codex CLI registers the same stdio command with `codex mcp add <name> -- ...`
and stores the host configuration under `~/.codex/config.toml`; verify with
`codex mcp list` and `codex mcp get <name>`. Claude Code registers it with
`claude mcp add <name> --scope project -- ...` or `--scope user`; project scope
is represented by `.mcp.json`, while user scope is kept in Claude's user
configuration. The checked-in repository contains documentation/examples, not
machine-specific host config with absolute paths.

Use a read-only server name/profile by default. Create a separate writable
profile only for an explicitly approved registration/refresh/removal task, and
keep host approval/HITL enabled for those three mutation tools.

## Proposed MCP Contract

### Explicit write operations

- `register_repository(url, ref?)`
- `unregister_repository(repo_id)`
- `refresh_repository(repo_id)`

### Read and discovery operations

- `list_registered_repositories()`
- `get_registry_info()`
- `get_repository_status(repo_id)`
- `discover_skills(query, repo_id?, cursor?, limit?)`
- `get_skill_manifest(repo_id, skill_id)`
- `read_skill(repo_id, skill_id)`

`read_skill()` returns `SKILL.md` plus only support files explicitly listed by
the registered repository's required `skills/registry.json`. The registry must
validate before the repository can be indexed; missing or invalid registry or
package data rejects the repository. It always reads the active trusted
indexed commit; there is no caller-selected revision or arbitrary path
argument. Every tool has an explicit JSON input/output schema and
machine-readable error taxonomy.

A package is a normalized repository-relative directory containing one
`SKILL.md`; registry-listed support paths must remain inside that package.
Manifest fields such as `raw_url` are metadata only and are ignored for reads;
all bytes come from the pinned Git checkout. Conflicting registry mappings
fail with `index_failed`, malformed package metadata fails with `invalid_skill`,
path containment failures fail with `invalid_path`, and unsupported binary
support files fail with `binary_not_supported`. A repository that does not
meet the complete format is rejected rather than partially exposed.

`skill_id` is the normalized POSIX package path relative to the registered
repository; `(repo_id, skill_id)` is the globally unique identity. Discovery
uses trimmed Unicode case-folded substring tokens over skill id, name,
description, and declared capability fields. An empty query means all indexed
skills in stable `(repo_id, skill_id)` order. The default page size is 20 and
the maximum is 100. Cursors are opaque and bound to profile identity,
normalized query, optional `repo_id` filter, page size, and index generation.
A mismatched cursor returns `invalid_cursor`; refresh or unregistration
invalidates the generation with `cursor_stale`.
Each discovery result includes `repo_id`, `skill_id`, `name`, `description`,
`capabilities`, profile, source ref/commit, package path, checksum, license
state, and index generation. The initial error taxonomy is
`invalid_source`, `scope_denied`, `not_registered`, `not_indexed`,
`invalid_skill`, `invalid_path`, `fetch_failed`, `index_failed`,
`drift_detected`, `source_unavailable`, `registry_corrupt`,
`permission_denied`, `size_limit_exceeded`, `busy`, `invalid_cursor`,
`cursor_stale`, `binary_not_supported`, and `registration_conflict`.

The first implementation must not expose a generic filesystem-write tool,
arbitrary URL fetch tool, native skill installer, or `get_install_hint()` as a
core operation.

## Local Registry Contract

Each entry must preserve, at minimum:

- canonical repository URL and stable repository id
- requested ref and resolved commit SHA
- active profile id `(mode, scope)`, scope type, canonical scope root, and state root
- index status and last refresh time
- discovered skill ids and manifest-allowlisted package files
- source license/provenance and content checksum
- registry schema version and last trusted index generation

Repository URLs are restricted to `https://` and `ssh://` (including a
canonicalized SSH form); `file://`, local paths, `git://`, and plain `http://`
are rejected. SSH `git@host:path` is normalized to `ssh://git@host/path`, host
names are lower-cased, and the default port 22 is omitted. `repo_id` is a
stable derivation from the canonical URL: the same canonical URL and ref return
the existing registration, a different ref returns `registration_conflict`,
and HTTPS and SSH forms are not assumed equivalent unless their canonical URL
is identical. Project-local registry state is bound to the configured
canonical `scope_root`, so a private repository approved for one project does
not automatically appear in another project's discovery scope. Git
credentials must come from the existing credential helper; tokens must not be
copied into registry files, logs, or MCP responses.

Registry mutations are idempotent and use a single-writer lock plus staged
index files and atomic replacement. A failed load or corrupted registry fails
closed and leaves the last trusted index available only when its integrity
check passes. The lock is cross-process; a second writer returns `busy` after a
fixed timeout. Unknown registry schema versions return `registry_corrupt`; a
future migration requires a separate SOW.

The initial abuse limits are a 100 MiB repository cache, a 1 MiB complete skill
bundle, and a 256 KiB individual support file. A result over a limit fails with
`size_limit_exceeded`; limits are configuration, not model-controlled input.

The host launch contract supplies `MCP_SKILLS_MARKET_MODE` (`readonly` or
`writable`), `MCP_SKILLS_MARKET_SCOPE` (`global` or `project`),
`MCP_SKILLS_MARKET_STATE_ROOT`, and `MCP_SKILLS_MARKET_SCOPE_ROOT` when the
scope is `project`. It also supplies
`MCP_SKILLS_MARKET_GIT_TIMEOUT_S`, `MCP_SKILLS_MARKET_MAX_REPO_BYTES`,
`MCP_SKILLS_MARKET_MAX_BUNDLE_BYTES`, and
`MCP_SKILLS_MARKET_MAX_SUPPORT_FILE_BYTES`. These values are process
configuration, not tool arguments. Git fetches set `GIT_TERMINAL_PROMPT=0`,
use `GIT_SSH_COMMAND` with `BatchMode=yes` and `StrictHostKeyChecking=yes`,
disable `GIT_ASKPASS` and `SSH_ASKPASS` through a non-interactive deny helper,
reject unknown host keys, and use a 30-second default timeout.

## Deliverables

1. A local `stdio` MCP service with the contract above and explicit read-only or
   writable profile configuration.
2. A versioned, schema-validated local repository registry.
3. Repository registration, refresh, removal, pinned revision, and discovery
   behavior with deterministic fixture repositories.
4. Strict manifest-backed skill bundle loading with source path, commit,
   per-file checksum, license/provenance, and rejection of incomplete
   repositories.
5. Explicit profile-bound behavior for global versus project-local registries,
   including canonical scope-root handling.
6. Codex and Claude MCP connection examples pointing to the same service
   contract, plus protocol-level smoke evidence.
7. One exact service launch/configuration contract, including the importable
   `mcp_skills_market.server:serve_stdio()` entrypoint, mode/scope/state-root
   variables, Git timeout, size limits, and host examples.
8. Security and negative-path tests for unregistered repositories, URL/path
   escape, symlink/submodule/hook behavior, drift, token leakage, malicious
   instructions, and script execution.
9. Operator documentation covering lifecycle, storage, refresh, removal,
   offline/cache behavior, and recovery from a failed refresh.
10. An architecture specification covering the fixed stack, stdio I/O,
    profile-bound state, repository layout, startup wiring, security
    invariants, verification evidence, and deferred scope.

## Done Criteria

1. A direct `register_repository()` call on a writable profile accepts only
   allowed remote URL schemes, persists a canonical entry, and pins a
   resolvable commit without writing outside the configured state root.
   Repeating the same canonical URL and ref returns the existing registration;
   changing only the ref returns `registration_conflict`.
   The same call on a read-only profile returns `permission_denied`; no
   model-supplied confirmation flag can enable mutation.
2. Profile-bound `discover_skills()` returns skills only from registered
   repositories and respects the canonical project scope root.
3. An unregistered repository, path, or revision cannot be returned or read;
   after unregistration, reads fail even if cache cleanup is deferred.
4. `refresh_repository()` uses a staged candidate index and atomic swap; it
   reports `fetch_failed`, `index_failed`, `drift_detected`, or
   `source_unavailable` without replacing the last trusted index.
5. `unregister_repository()` removes the repository from future discovery and
   read access, then applies the documented cache policy.
6. `read_skill()` returns only `SKILL.md` plus trusted manifest-listed support
   files at the active indexed commit, with per-file provenance and checksums;
   checksum or manifest drift is detectable.
7. No MCP operation can execute repository scripts, follow a symlink outside
   the cache root, fetch `file://` or plain `http://`, write arbitrary paths,
   install native skills, or expose credential-bearing content.
8. JSON schemas, error taxonomy, query semantics, cursor pagination, duplicate
   handling, size limits, and missing-license/compatibility behavior are
   documented and covered by tests.
9. Repository mapping is strict and deterministic: `skills/registry.json` is
   required, package paths are normalized, conflicting registry mappings fail
   closed, symlinks and unsupported binary files are rejected, and repositories
   using another manifest or manifest-free layouts are rejected.
10. Git ingestion is non-interactive, time-bounded, and fail-closed for
    unknown SSH host keys, credential prompts, missing Git, or remote failure;
    no credential-bearing output is emitted.
11. Restart and concurrency tests cover abandoned staging data, corrupt or
    missing cache/index generations, refresh-versus-unregister races, and
    lock timeout behavior.
12. The protocol smoke path passes through both Codex and Claude when those
   hosts are available. If either host cannot be exercised, the SOW remains
   `implemented but not fully verified` and cannot be closed as complete.
13. Each host smoke records startup/profile, registry info, list/status,
    registered discovery, skill read, unregistered negative, read-only mutation
    denial, host version, and raw protocol/tool evidence.
14. Default behavior never queries `skills.sh` or an unregistered public catalog.
15. Tests cover happy paths, empty registries, duplicate registration,
    concurrent mutation, refresh failure, unregistration, scope isolation,
    malformed registry/package metadata, path traversal, symlinks, submodules/hooks, private
    repo credential safety, and untrusted instructions.
16. `git diff --check`, targeted tests, protocol inspection, and one negative
    check proving an unregistered repo is invisible all pass.
17. Closeout separates implemented, simulated, and unverified provider-facing
    behavior; text inspection alone is not evidence that both hosts executed
    the MCP path.
18. The runtime uses the official `mcp>=2,<3` SDK and `MCPServer` over stdio;
    no fallback protocol implementation, HTTP daemon, or unrelated Git client
    library is introduced.
19. The registry, index generations, locks, and bare Git caches are stored under
    the external state root with user-only permissions; the Git worktree stays
    free of runtime state and credentials.
20. A fixture repository following the complete documented
    `skills/registry.json` plus `skills/<skill-id>/SKILL.md` layout is
    discoverable, while missing/invalid registries, other manifest sources,
    manifest-free repositories, and arbitrary paths are rejected.
21. `docs/mcp-skills-market-architecture.md` is consistent with this SOW and
    the plan, contains no machine-specific secrets or runtime state, and is
    reviewed twice before SOW approval.

## Out-of-Scope

- Internet-wide skill crawling or ranking.
- `skills.sh` as a mandatory provider or default source.
- A per-agent marketplace, Codex plugin package, or Claude plugin package.
- Automatic installation, synchronization, or mutation of native skill roots.
- Remote MCP write access to the user's filesystem.
- Arbitrary shell/script execution from registered repositories.
- First-party verification for MCP hosts other than Codex and Claude.
- Provider credential management, OAuth UI, hosted multi-user service, or
  telemetry.
- Changes to existing skill bodies, `skills/registry.json`, host settings, or
  unrelated repositories.
- Commit or push unless explicitly requested after implementation verification.

## Cautions / Risks

- A registered repository is user-approved as a source, not automatically
  trusted as an instruction set; content must remain policy-constrained.
- Private repository access may fail because of credential scope; the service
  must fail closed without printing credential details.
- Moving refs and force-pushed branches can invalidate provenance; commit pinning
  and drift reporting are required.
- A project-local registry can become stale; refresh status and failure state
  must remain visible.
- A repository or skill without a declared license is represented as
  `license: unknown`; it is not silently treated as permissively licensed.
- MCP provider behavior differs by host; Codex and Claude smoke evidence must
  be recorded separately rather than inferred from one another.

## Review Protocol

Before approval, perform three independent, read-only reviews of this SOW and
the companion plan:

1. `gpt-5.6-sol` at medium reasoning.
2. `custom/greennode-glm-5.2` at the requested high/max reasoning available to
   the transport.
3. `custom/greennode-glm5.3-flash-thirdparty` at the requested high/max
   reasoning available to the transport.

Each reviewer must receive a fresh, task-local context with no parent history,
must not edit files, and must report findings in the compact
`Severity | Finding | Impact | Solution` format when issues are actionable.
The coordinator owns reconciliation; reviewer agreement is not approval.

## Review Summary

All three requested reviewers completed isolated, read-only reviews of this
SOW and its companion plan. Each recommended `revise`; no reviewer requested a
change to the registered-repository source boundary or the native-installation
exclusion.

| Reviewer | Main findings | Writeback disposition |
| --- | --- | --- |
| Sol medium | Profile-bound project identity, enforceable mutation boundary, one transport, trusted-index-only reads, dependency scope, Git ingestion, and host completion gate. | Locked `stdio` v1, profile-bound scope root, writable-profile rule, atomic locking, active-index reads, dependency location, and hard host evidence gate. |
| GLM-5.2 | URL scheme allowlist, revision/path escape, registry locking/recovery, project identity, schema version, and unavailable-source status. | Restricted URLs, removed caller revision/path, added registry info, locking, integrity failure, and source-unavailable states. |
| GLM-5.3 Flash | Manifest-backed support bundle, scope identity, dependency/runtime scope, atomic refresh state, JSON schemas/error taxonomy, host smoke evidence, and mutation approval. | Added bounded bundle contract, staged index states, schema/error requirements, host smoke hard gate, and manifest/security rules. |

The writeback records coordinator reconciliation, not model consensus or user
approval. The artifact remains a DRAFT until the user approves it.

The final GLM-5.2 and GLM-5.3 reviews ran in fresh read-only contexts after the
first writeback. GLM-5.2 identified four low-severity profile/canonicalization/
migration/locking clarifications; GLM-5.3 identified query, manifest, recovery,
Git-ingestion, host-evidence, and launch-contract gaps. Those clarifications
are now incorporated above and in the companion plan; no finding changed the
registered-repository source boundary or native-installation exclusion.

The coordinator then locked the implementation stack and deployment topology:
official MCP Python SDK v2, `stdio`, typed structured tool I/O, JSON generation
storage, bare Git cache, external state root, and host-owned Codex/Claude
configuration. This is a planning decision, not implementation approval.

## Plan / Reference

- Companion plan: `plan_todo/active/PLAN_20260923_OL8CB3EC/PLAN_20260923_OL8CB3EC_mcp_skills_market_plan.md`
- Requested review skill: `skills/task-review-investigate-compare/SKILL.md`
- Delegation/context isolation: `skills/sow-delegate-flow/SKILL.md`
- Local task routing and lifecycle: `skills/task-router-flow/SKILL.md`
- MCP protocol reference: <https://modelcontextprotocol.io/specification/draft/server/index>
- Optional directory reference only: <https://www.skills.sh/docs/api>

## Approval Gate

This document is a DRAFT planning artifact. It is not approval to create the
service or change runtime/configuration surfaces. Implementation requires an
explicit approval recorded here and a subsequent execution flow.
