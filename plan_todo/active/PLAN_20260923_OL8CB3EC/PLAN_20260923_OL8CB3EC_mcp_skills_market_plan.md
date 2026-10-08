# PLAN_20260923_OL8CB3EC - Plan - MCP Skills Market With Registered Repository Discovery

- Status: DRAFT
- Approval: UNKNOWN
- create_dttm: 2026-09-23T03:49:01+07:00
- create_date: 2026-09-23
- create_dttm_source: original_creation_datetime
- create_dttm_confidence: explicit
- create_dttm_evidence: `plan_todo/finished/SOW_20261008_VO3LKN0L/creation-date-evidence.json` (record: PLAN_20260923_OL8CB3EC)
- approve_dttm: null
- finish_dttm: null
- legacy_id: null
- legacy_path: plan_todo/mcp_skills_market_plan.md
- migrated_dttm: 2026-10-08T12:48:51+07:00
- legacy_title: Plan - MCP Skills Market With Registered Repository Discovery

## Preserved Contract And Historical Evidence

## Status

- **Status**: DRAFT
- **Owning SOW**: `plan_todo/active/PLAN_20260923_OL8CB3EC/SOW_20260923_GVDCDZ3B/SOW_20260923_GVDCDZ3B_mcp_skills_market_local_repository_registry.md`
- **Architecture**: `docs/mcp-skills-market-architecture.md`
- **create_dttm**: 2026-09-23T03:49:01+07:00
- **approve_dttm**: null
- **finish_dttm**: null

## Objective

Build one local MCP service that acts as a universal skills marketplace over
explicitly registered repositories. The service stores repository registration
locally, indexes only those repositories, and returns discoverable skills to
Codex and Claude without installing native skills. Other MCP-capable hosts may
consume the protocol, but are not first-party verification targets in v1.

The architecture specification is the single document for the fixed stack,
stdio wire contract, runtime storage, registered repository layout, host
wiring, security invariants, verification boundaries, and deferred scope.

## Fixed Decisions

- The market is universal at the MCP protocol layer, not a separate marketplace
  package for each host.
- Repository registration is explicit and user-authorized.
- The default source set is the local registry, not the Internet or `skills.sh`.
- Local MCP writes are limited to repository registration, refresh, and removal.
- v1 uses `stdio`; a host launches the same service contract with a configured
  profile and state root. A localhost daemon is deferred.
- Discovery and skill loading are separate from native host installation.
- Every returned skill bundle is pinned to repository/ref/commit/package and has
  visible per-file checksums and provenance.
- Global and project-local profiles are distinct; project identity is an
  explicit canonical `scope_root` fixed when the server starts, never a model
  argument.
- Launch mode (`readonly` or `writable`) is independent of scope; profile
  identity is the `(mode, scope)` tuple, not one overloaded variable.
- A project profile never inherits registrations from the global profile or
  another project profile.
- Remote skill content remains untrusted and cannot authorize code execution or
  policy bypass.
- `https://` and `ssh://` are the only accepted repository URL schemes.
- Missing license is represented as `unknown`; it is never inferred as open.
- The only supported manifest is a valid `skills/registry.json`; missing or
  invalid registries and incomplete packages are rejected. Other manifest
  sources are unsupported and there is no fallback scan.
- Initial limits are 100 MiB per repository cache, 1 MiB per complete skill
  bundle, and 256 KiB per support file.
- SSH `git@host:path` is canonicalized to `ssh://git@host/path`, host names are
  lower-cased, and default port 22 is omitted.
- `repo_id` is derived from the canonical URL. Same canonical URL plus the same
  ref is idempotent; a different ref returns `registration_conflict`. HTTPS
  and SSH forms are not implicitly equivalent unless their canonical URL is
  identical.
- Unknown registry schema versions fail closed as `registry_corrupt`; migration
  is a future SOW.
- Use the official `modelcontextprotocol/python-sdk` v2 package as
  `mcp>=2,<3`; use `MCPServer`, typed/Pydantic contracts, and `stdio` only.
  Keep `mcp[cli]` out of runtime dependencies and use it only for development
  inspection. Do not add FastAPI/Uvicorn, a daemon, GitPython, Dulwich, or
  SQLite in v1.
- Use `git` subprocesses for source ingestion, versioned JSON for registry and
  index generations, atomic replacement, and a cross-process lock adapter.
- Keep runtime state outside Git under the explicit state root; the service code
  remains in this project and host configuration remains outside the repo.

## Execution Phases

### Phase 0 - Contract and baseline

- Confirm no existing MCP service or repository registry implementation is being
  replaced.
- Lock registry schema, operation names, profile-bound scope semantics, JSON
  schemas, error taxonomy, and failure states.
- Lock query grammar, result fields, default/max page size, cursor generation
  binding to query/filter/page size, registry package-to-`skill_id` mapping,
  and binary-file handling.
- Add the official Python MCP SDK v2 as `mcp>=2,<3` to the existing `uv`
  project and record the resolved minor version in `uv.lock`. If the dependency
  cannot resolve, stop and route a scope change; do not silently implement a
  second protocol stack.
- Configure v1 as `stdio` only, with an explicit state root and optional
  canonical project `scope_root`.
- Lock the host launch contract around importable `serve_stdio()` plus fixed
  profile/state/scope configuration variables before implementation.
- Lock the wire contract: newline-delimited JSON-RPC on stdio, protocol output
  on stdout only, diagnostics on stderr, typed structured success results, and
  stable JSON error payloads for domain failures.
- Keep `docs/mcp-skills-market-architecture.md` synchronized with these locked
  decisions before implementation approval.

### Phase 1 - Registry and repository source

- Implement canonical repository URL parsing and stable repo ids.
- Accept only `https://` or `ssh://` sources; reject local paths, `file://`,
  `git://`, and plain `http://`.
- Run Git non-interactively with a fixed timeout, disabled credential prompts,
  fail-closed unknown SSH host keys, and deterministic mapping of Git-unavailable
  or remote failures to the error taxonomy.
- Use `GIT_TERMINAL_PROMPT=0`, `GIT_SSH_COMMAND` with `BatchMode=yes` and
  `StrictHostKeyChecking=yes`, non-interactive deny helpers for
  `GIT_ASKPASS`/`SSH_ASKPASS`, no automatic host-key acceptance, and a
  30-second default fetch timeout.
- Persist requested ref, pinned commit, profile identity, scope root, status,
  timestamps, and source metadata in a schema-validated local registry.
- Implement explicit registration, duplicate handling, refresh, and removal;
  same canonical URL plus ref is idempotent, while a different ref returns
  `registration_conflict`.
- Use existing Git credentials without copying secrets into application state.
- Use a single-writer lock, staged files, and atomic replacement; fail closed on
  registry corruption while preserving a verified last trusted index.
- Treat concurrent writers and refresh-versus-unregister as serialized state
  transitions; return `busy` after the lock timeout.
- Store each repository as a bare Git object cache under the profile state
  root; never serve staging data or execute checkout hooks.

### Phase 2 - Indexing and discovery

- Discover only packages declared by a valid `skills/registry.json` inside
  registered repos.
- Treat a skill package as `SKILL.md` plus only registry-listed support files;
  reject repositories without a valid registry or with incomplete packages.
- Build deterministic metadata records for name, description, path, revision,
  checksum, license, and compatibility.
- Implement query filtering by registered repo/profile, cursor, limit, stable
  sorting, duplicate handling, and explicit empty-query behavior.
- Return stable results sorted by `(repo_id, skill_id)` unless an explicit
  relevance field is later approved; deduplicate by canonical `(repo_id,
  package_path)` identity.
- Match trimmed Unicode case-folded substring tokens over skill id, name,
  description, and capability fields. Empty query returns all indexed skills;
  default `limit` is 20, maximum is 100, and cursors are opaque and bound to
  profile identity, normalized query, repo filter, page size, and generation.
  Mismatches return `invalid_cursor`; refresh or unregistration returns
  `cursor_stale`.
- Return `repo_id`, `skill_id`, `name`, `description`, capabilities, profile,
  source ref/commit, package path, checksum, license state, and index
  generation in every discovery record.
- Derive `skill_id` from normalized POSIX package path. A registered
  repository's `skills/registry.json` is required; other manifest sources and
  manifest-free scans are rejected. Missing or malformed registries fail with
  `index_failed`; conflicting registry mappings fail with `index_failed`.
  Manifest `raw_url` or other remote-content fields are ignored; reads always
  use the pinned Git checkout. Reject symlinks with `invalid_path` and
  unsupported binary support files with `binary_not_supported`; malformed
  package metadata returns `invalid_skill`.
- Fail closed on malformed registry/package metadata, path traversal, symlink escape,
  submodules, hooks/filters, unresolvable refs, or ambiguous refresh results.
- Enforce the configured repository, bundle, and support-file size limits.
- Enforce the complete repository layout: a valid `skills/registry.json` and
  registry-declared `skills/<skill-id>/SKILL.md` packages are required.
  Other manifest sources, undeclared packages, and manifest-free repositories are
  rejected; registry entries are the only v1 source of support-file allowlists.

### Phase 3 - MCP surface

- Expose the agreed write and read operations through one local `stdio` MCP
  server contract; writable mutations require a writable profile and host
  approval configuration.
- Keep generic filesystem writes, shell execution, native installers, and
  arbitrary URL fetches unavailable.
- Return compact metadata from discovery and manifest-bounded content only on
  explicit read; never accept caller-selected revision or arbitrary path.
- Add Codex and Claude connection examples targeting the same service contract.
- Publish JSON schemas and machine-readable errors for every operation.
- Successful calls return typed JSON in `structuredContent` and compact
  model-readable text; expected domain failures return stable JSON error
  payloads through the SDK tool-error path, while diagnostics stay on stderr.

The host launch contract is fixed as an importable `serve_stdio()` entrypoint
with configuration supplied by the host profile: mode, scope, state-root path,
canonical project `scope_root`, cache limits, and Git timeout. The concrete
environment names are `MCP_SKILLS_MARKET_MODE`, `MCP_SKILLS_MARKET_SCOPE`,
`MCP_SKILLS_MARKET_STATE_ROOT`, `MCP_SKILLS_MARKET_SCOPE_ROOT`,
`MCP_SKILLS_MARKET_GIT_TIMEOUT_S`, `MCP_SKILLS_MARKET_MAX_REPO_BYTES`,
`MCP_SKILLS_MARKET_MAX_BUNDLE_BYTES`, and
`MCP_SKILLS_MARKET_MAX_SUPPORT_FILE_BYTES`. The service does not accept these
values as model-controlled tool arguments.

The initial error taxonomy is: `invalid_source`, `scope_denied`,
`not_registered`, `not_indexed`, `invalid_skill`, `invalid_path`,
`fetch_failed`, `index_failed`, `drift_detected`, `source_unavailable`,
`registry_corrupt`, `permission_denied`, `size_limit_exceeded`, `busy`,
`invalid_cursor`, `cursor_stale`, `binary_not_supported`, and
`registration_conflict`.

### Runtime state and repository layout

The state root is external to Git and contains `profiles/<profile-id>/registry.json`,
immutable `indexes/gen-<n>.json`, bare Git caches under `repos/<repo-id>/repo.git/`,
staging directories, and a cross-process lock. The default macOS root is
`~/Library/Application Support/AISkills/mcp-skills-market`; Linux and Windows
follow their standard state directories. The implementation must not create a
runtime `.aiskills/` directory in this repository by default.

Registered repositories must expose a valid `skills/registry.json` and
registry-declared `skills/<skill-id>/SKILL.md` packages. Other manifest sources and
manifest-free repositories are rejected; every returned path is relative,
POSIX-normalized, and contained by its package.

The direct development launch is `uv run --project <AISkills_ROOT> python -m
mcp_skills_market.server`. Codex uses `codex mcp add <name> -- ...` and Claude
Code uses `claude mcp add <name> --scope project -- ...`; host configuration is
kept in their own config surfaces, not committed with machine-specific paths.

### Phase 4 - Verification and security

- Run fixture-repository tests for registration, profile scope, discovery, read,
  refresh, removal, checksum drift, and failed fetch/index recovery.
- Run in-memory SDK client tests for every tool's typed input/output schema and
  domain-error JSON payload before spawning a stdio subprocess.
- Run negative checks for unregistered access, arbitrary paths, script execution,
  URL/symlink escape, submodules/hooks, credential leakage, and malicious
  instruction content.
- Run protocol-level smoke plus real Codex and Claude tool calls separately.
  If either host is unavailable, record it as unverified and do not close the
  SOW as complete.
- For each host, record startup/profile, registry info, list/status, registered
  discovery, skill read, unregistered negative, read-only mutation denial, host
  version, and raw protocol/tool evidence.
- Confirm default execution performs no `skills.sh` lookup.
- Confirm the service starts from the project checkout with `uv` and that no
  runtime state or credentials are written into the Git worktree.

### Phase 5 - Closeout

- Perform the post-implementation gap-finding checklist.
- Record exact commands, scenarios, outputs, failures, and unavailable checks.
- Compare SOW deliverables and done criteria with the implementation.
- Confirm the architecture specification remains consistent with the approved
  SOW, implementation, and recorded verification evidence.
- Move both the completed SOW and this completed plan to `plan_todo/finished/`
  only after all required verification and approval gates are satisfied.

## State Model

```text
not registered
  -> registered / not indexed
  -> indexed at pinned commit
  -> refresh pending
  -> fetch_failed | index_failed | drift_detected | source_unavailable
  -> refreshed at a staged, trusted commit
  -> unregistered
```

Failed refresh, source disappearance, checksum drift, or index corruption must
preserve the last trusted index and expose the failure; it must not silently
replace trusted content with an unpinned, partial, or unverified result. After
unregistration, the cached bytes are not readable through the MCP contract.
On restart, abandoned staging data is removed only after lock acquisition;
cache/index generations must match before reads are served. Refresh and
unregister are serialized; the operation that acquires the lock first wins and
the other returns `busy` or `not_registered` according to the resulting state.
An interrupted refresh never promotes staging data; a missing or corrupt active
generation returns `registry_corrupt` and leaves no partially readable bundle.

## Verification Matrix

| Area | Evidence required |
| --- | --- |
| Registration | Local entry has canonical URL, profile, scope root, ref, pinned commit, and status |
| Discovery boundary | Registered repo appears; unregistered repo/path/revision does not |
| Scope isolation | Project-local repo is invisible outside its configured canonical scope root |
| Provenance | Bundle response includes repo, package, commit, per-file checksums, and license state |
| Refresh | Staged commit/index changes and machine-readable failure state are observable |
| Security | No arbitrary path write, script execution, URL/path escape, or credential-bearing output |
| MCP contract | JSON schemas, errors, query matching, pagination, sort, dedup, and size limits are deterministic |
| Manifest mapping | Required registry validation, package paths, skill ids, symlink/binary handling, and rejection of fallback layouts are deterministic |
| Host compatibility | Mandatory protocol smoke plus separate Codex and Claude MCP smoke evidence |
| Source policy | No default `skills.sh` or Internet-wide search |
| Recovery | Failed refresh leaves the last trusted index usable |
| Tech stack | `mcp>=2,<3`, `MCPServer`, stdio, and system Git are used without a second protocol or Git library |
| State placement | Registry/cache/lock state is outside the Git worktree and no credential-bearing artifact is committed |

## Review Contract

The SOW and this plan must be reviewed three times before approval:

- Sol medium: architecture, scope, simplicity, and verification.
- GLM-5.2: contract completeness, local write boundary, and security.
- GLM-5.3 Flash: host compatibility, failure modes, and accidental scope drift.

Reviews are read-only and isolated. The coordinator applies only justified
writebacks and keeps user decisions authoritative.

## Approval Decisions Before Implementation

- Default state root is configured explicitly for the service profile; no
  model-supplied path is trusted. A project profile must provide a canonical
  `scope_root`; a global profile has no project scope.
- The implementation source is this repository, but runtime state is external;
  Codex and Claude host configuration is generated through their own config
  surfaces and is not committed with machine-specific absolute paths.
- A project profile searches only its own registrations; there is no global
  profile fallthrough. Cross-process writers use a lock with a fixed timeout.
- Initial ingestion uses the existing Git credential helper and a pinned commit;
  the official `mcp>=2,<3` SDK and resolved lockfile version are fixed before
  code edits.
- Initial package compatibility requires a valid `skills/registry.json` plus
  registry-declared `SKILL.md` packages. Plugin manifests and missing/unknown
  registry formats are rejected; conflicts fail closed.
- Unregistration removes active registry access immediately; cache deletion is
  performed by the documented cleanup path and never restores read access.
- A project profile has no global-profile fallthrough. The launch profile is the
  sole authority for state root, writable mode, scope root, limits, and Git
  timeout.

These decisions do not reopen the fixed source boundary or native-installation
exclusion. A different transport, provider, package format, or scope authority
requires an SOW extension or replacement before implementation.

## Review Result

Sol medium, GLM-5.2, and GLM-5.3 Flash each completed an isolated read-only
review and recommended `revise`. The coordinator wrote back the agreed
contract hardening in SOW_20260923_GVDCDZ3B and this plan; the artifact remains `DRAFT` and
has not been approved for implementation. The final GLM-5.2 and GLM-5.3
reviews then checked the post-writeback contract; their remaining low/medium
ambiguities are incorporated in the query, manifest, recovery, Git, launch, and
host-evidence rules above. The coordinator also locked the official MCP SDK v2,
stdio I/O, JSON generation storage, bare Git cache, external state root, and
host-owned Codex/Claude configuration; implementation still requires approval.
