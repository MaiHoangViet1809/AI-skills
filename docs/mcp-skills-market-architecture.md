# MCP Skills Market Architecture

## Document Control

- **Status**: DRAFT
- **Owning SOW**: `plan_todo/active/PLAN_20260923_OL8CB3EC/SOW_20260923_GVDCDZ3B/SOW_20260923_GVDCDZ3B_mcp_skills_market_local_repository_registry.md`
- **Plan**: `plan_todo/active/PLAN_20260923_OL8CB3EC/PLAN_20260923_OL8CB3EC_mcp_skills_market_plan.md`
- **Created**: `2026-09-23T14:56:32+07:00`
- **Scope**: v1 local registered-repository catalog for Codex and Claude
- **Implementation state**: Architecture only. No MCP service is implemented by this document.

This document is the architecture authority for the MCP service described by
[SOW_20260923_GVDCDZ3B](../plan_todo/active/PLAN_20260923_OL8CB3EC/SOW_20260923_GVDCDZ3B/SOW_20260923_GVDCDZ3B_mcp_skills_market_local_repository_registry.md). The SOW remains the approval and execution authority. If this
document and the approved SOW diverge, implementation must stop until the SOW
is extended or corrected.

## 1. Purpose And Boundaries

The service is a local MCP catalog that lets an agent discover and read skills
from repositories the user explicitly registered. Codex and Claude consume the
same protocol and repository contract; neither host receives a separate
marketplace implementation.

The service **does**:

- persist an explicit allowlist of registered Git repositories;
- fetch and pin a requested repository ref to a resolved commit;
- index registry-declared skill packages and their `SKILL.md` files;
- search and return bounded skill metadata or a manifest-backed skill bundle;
- expose explicit local registration, refresh, and removal operations from a
  separately configured writable profile.

Only the local service process has filesystem write authority. A remote or
hosted MCP endpoint cannot write this machine's registry, and a host connection
must not grant remote callers a path or credential to bypass that boundary.

The service **does not**:

- crawl the Internet or query `skills.sh` by default;
- discover repositories that were not registered in the active profile;
- install files into `~/.codex`, `~/.claude`, or another native skill root;
- execute repository scripts, hooks, prompts, or arbitrary tool payloads;
- expose a generic filesystem writer, arbitrary URL fetcher, HTTP daemon, or
  hosted MCP endpoint in v1.

## 2. Context And Topology

```text
                         host-owned configuration
                  +-------------------------------+
                  | Codex CLI       Claude Code   |
                  +---------------+---------------+
                                  |
                    one child process per profile
                                  |
                         stdio JSON-RPC
                                  |
                  +---------------v---------------+
                  | mcp_skills_market.server     |
                  | official MCP Python SDK v2   |
                  +---------------+---------------+
                                  |
       +--------------------------+--------------------------+
       |                          |                          |
  typed contracts          profile-bound registry       Git source adapter
  and tool errors          + index generations          non-interactive Git
       |                          |                          |
       +--------------------------+--------------------------+
                                  |
                    external per-profile state root
             registry.json, immutable indexes, bare Git caches
                                  |
                    explicitly registered remote repositories
```

The host starts the service as a child process. There is no shared background
daemon in v1. A host restart creates a new process with the same explicit
profile configuration.

## 3. Fixed Technology Stack

| Concern | Decision | Explicitly excluded in v1 |
| --- | --- | --- |
| Runtime | Python 3.10+ managed by `uv` | A second runtime or global install |
| MCP protocol | Official `modelcontextprotocol/python-sdk`, PyPI `mcp>=2,<3`, SDK v2 `MCPServer` | Hand-written JSON-RPC, host-specific SDKs |
| Input/output | Typed Python/Pydantic models generated into MCP schemas | Untyped `dict` contracts |
| Transport | `stdio` only | FastAPI, Uvicorn, localhost daemon, hosted HTTP/SSE |
| Git ingestion | System `git` in a controlled subprocess | GitPython, Dulwich, embedded Git implementation |
| Registry/index | Versioned JSON, immutable index generations, atomic replacement, cross-process lock | SQLite or an unversioned mutable blob |
| Protocol tests | Repository `unittest` plus SDK in-memory `Client(server)` | Inspector-only or syntax-only proof |
| Development inspection | `mcp[cli]` as a development/Inspector extra only | Making the CLI extra a runtime requirement |

The package constraint is intentionally major-version bounded. The exact
resolved minor version is recorded in `uv.lock` when the implementation SOW is
approved. The implementation must use the SDK's server and error APIs rather
than maintaining a parallel protocol implementation.

## 4. Process And Wire Contract

### 4.1 Lifecycle

1. The host resolves a profile and starts one service child process.
2. The service reads process configuration and opens only that profile's state.
3. The SDK performs the MCP handshake over the child's standard streams.
4. The host sends typed tool calls until the process exits or is restarted.
5. The service writes protocol frames to stdout and diagnostics to stderr.

Stdout is reserved for MCP protocol frames. Git stderr, diagnostics, audit-safe
events, and tracebacks never enter stdout. Secrets and raw credential-bearing
Git output must not be written to either MCP responses or logs.

### 4.2 Input and output rules

- The transport is newline-delimited JSON-RPC over stdin/stdout as managed by
  the official SDK.
- Every tool has a typed input model and a published JSON Schema.
- Invalid arguments are rejected by SDK/schema validation before handler logic.
- Successful calls return typed JSON in `structuredContent` and the same
  compact JSON as model-readable text content.
- Expected domain failures use the SDK tool-error path with a stable payload:

  ```json
  {
    "error_code": "not_registered",
    "message": "repository is not registered in the active profile"
  }
  ```

- Protocol-invalid input remains an SDK validation error. Unexpected exceptions
  are sanitized in the tool result and recorded with detail only on stderr.
- The service does not expose resources, prompts, arbitrary file reads, or a
  generic write tool in v1.

### 4.3 Public tools

| Tool | Profile | Purpose |
| --- | --- | --- |
| `register_repository(url, ref?)` | Writable only | Canonicalize, fetch, pin, index, and register one repository |
| `refresh_repository(repo_id)` | Writable only | Stage and promote a new trusted commit/index |
| `unregister_repository(repo_id)` | Writable only | Remove active registry access and apply cache policy |
| `list_registered_repositories()` | Read | List only registrations in the active profile |
| `get_registry_info()` | Read | Return schema, profile, state, and active-generation metadata |
| `get_repository_status(repo_id)` | Read | Return registration, fetch, index, and last-error state |
| `discover_skills(query, repo_id?, cursor?, limit?)` | Read | Search the active profile's trusted index |
| `get_skill_manifest(repo_id, skill_id)` | Read | Return normalized manifest metadata and provenance |
| `read_skill(repo_id, skill_id)` | Read | Return a bounded, pinned skill bundle |

`get_install_hint()` is not a v1 core operation. A future install hint or host
adapter requires an SOW extension and must not mutate native skill directories.

### 4.4 Discovery and bundle results

`discover_skills` uses trimmed Unicode case-folded substring tokens over skill
id, name, description, and declared capability fields. An empty query returns
all indexed skills. The default page size is 20 and the maximum is 100. Results
are stable in `(repo_id, skill_id)` order and are deduplicated by canonical
`(repo_id, package_path)` identity.

An opaque cursor is bound to profile identity, normalized query, optional
repository filter, page size, and index generation. A mismatch returns
`invalid_cursor`; refresh or unregistration invalidates the generation and
returns `cursor_stale` for an old cursor.

Every discovery result includes:

- `repo_id`, `skill_id`, name, description, and capabilities;
- source ref and resolved commit;
- package path, content checksum, license state, and index generation;
- active profile identity.

`read_skill` returns the `SKILL.md` file and only manifest-allowlisted support
files from the active trusted commit. Each file record contains a repository-
relative POSIX path, UTF-8 text, byte size, and checksum. The bundle also
contains source URL, requested ref, resolved commit, package path, license
state, and provenance. `raw_url` or similar manifest URLs are metadata only and
are never fetched.

## 5. Source Repository Contract

### 5.1 Accepted sources and identity

Only `https://` and `ssh://` repository URLs are accepted. Local paths,
`file://`, `git://`, and plain `http://` are rejected. The scp-like form
`git@host:path` is normalized to `ssh://git@host/path`; host names are
lower-cased and default SSH port 22 is omitted.

`repo_id` is derived from the canonical URL. The same canonical URL and ref are
idempotent. A different ref returns `registration_conflict`. HTTPS and SSH are
not assumed equivalent unless their canonical URL is identical.

Git credentials remain owned by the user's configured credential helper. The
service never copies tokens into the registry, logs, staging files, or MCP
responses.

### 5.2 Repository layout and strict discovery

The recommended registered repository layout is:

```text
repository-root/
  skills/
    <skill-id>/
      SKILL.md
      references/...
      scripts/...
  skills/registry.json                 # required manifest
  LICENSE                               # optional; absent means unknown
```

The repository format is strict and has no discovery precedence or fallback:
`skills/registry.json` must exist, parse against the supported schema, and
declare every package. Each declared package is a normalized
repository-relative directory containing one `SKILL.md`; support files must be
explicitly allowlisted by that registry. A repository without the required
registry, with an invalid registry, with an undeclared package, or with an
invalid package is rejected and never indexed. A missing or malformed registry
returns `index_failed`; malformed package metadata returns `invalid_skill`.
Other manifest sources are not supported and cannot make an otherwise invalid
repository usable.

Paths cannot contain `..`, escape the package, or resolve through an outside
symlink. Symlinks, unsupported binary support files, conflicting registry
entries, and malformed packages fail closed. There is no `SKILL.md`-only scan.

The indexer reads bytes only from the pinned Git cache. It never follows a
manifest URL, checks out executable content for execution, runs a package
script, installs dependencies, or treats skill text as policy authority.

## 6. Profiles And Runtime Configuration

The process receives configuration from the host, not from MCP tool arguments:

| Variable | Values / meaning |
| --- | --- |
| `MCP_SKILLS_MARKET_MODE` | `readonly` or `writable` |
| `MCP_SKILLS_MARKET_SCOPE` | `global` or `project` |
| `MCP_SKILLS_MARKET_STATE_ROOT` | Explicit parent for runtime state |
| `MCP_SKILLS_MARKET_SCOPE_ROOT` | Required canonical project root when scope is `project` |
| `MCP_SKILLS_MARKET_GIT_TIMEOUT_S` | Git operation timeout; default 30 seconds |
| `MCP_SKILLS_MARKET_MAX_REPO_BYTES` | Repository cache limit; default 100 MiB |
| `MCP_SKILLS_MARKET_MAX_BUNDLE_BYTES` | Complete bundle limit; default 1 MiB |
| `MCP_SKILLS_MARKET_MAX_SUPPORT_FILE_BYTES` | Individual support-file limit; default 256 KiB |

The project scope root is canonicalized at process startup. Missing,
non-canonical, or symlink-ambiguous roots fail closed with `scope_denied`.
The model cannot select or override a root per call. A project profile searches
only its own registry and never inherits global or other project registrations.

The profile identity is a stable hash of `(mode, scope, canonical scope_root)`;
the canonical root is empty for global scope. Read-only and writable profiles
are therefore separate state identities. A read-only process cannot mutate
state even if a caller supplies a `user_confirmed` field.

## 7. Runtime State And Atomicity

Runtime state is external to Git and is not committed to the AISkills project.
`MCP_SKILLS_MARKET_STATE_ROOT` is the explicit parent. Defaults are:

- macOS: `~/Library/Application Support/AISkills/mcp-skills-market`
- Linux: `$XDG_STATE_HOME/aiskills/mcp-skills-market`, falling back to
  `~/.local/state/aiskills/mcp-skills-market`
- Windows: `%LOCALAPPDATA%/AISkills/mcp-skills-market`

The state layout is:

```text
<state-root>/
  profiles/<profile-id>/
    registry.json                 # registrations and trusted generation pointer
    indexes/gen-<n>.json          # immutable, validated index generations
    repos/<repo-id>/repo.git/     # bare Git object cache
    staging/<operation-id>/       # candidate data, never served directly
    locks/registry.lock           # cross-process single-writer lock
```

The service creates state directories with user-only permissions. Registry and
index files contain no credentials. A `.aiskills/` directory is not created in
the source repository by default.

Each registry entry contains, at minimum:

- canonical repository URL, stable `repo_id`, requested ref, and resolved
  commit SHA;
- active profile id, scope type, canonical scope root, and state-root identity;
- index status, last refresh time, last trusted generation, and last safe error;
- discovered skill ids and manifest-allowlisted package files;
- source license/provenance, content checksums, and registry schema version.

The registry pointer identifies the active trusted index generation. It never
serves a candidate generation from staging and never stores credential values.

Mutation sequence:

1. Acquire the profile lock; return `busy` after the fixed lock timeout.
2. Fetch or update the bare cache with non-interactive Git.
3. Resolve and pin the requested commit.
4. Build and validate a candidate index in `staging/<operation-id>`.
5. Validate limits, path containment, manifests, checksums, and generation
   metadata.
6. Atomically promote the candidate index and registry pointer.
7. Release the lock and expose the new generation.

Any fetch, index, validation, or process failure leaves the last trusted
generation active. Staging data is never served. On restart, abandoned staging
data is removed only after acquiring the lock. A missing or corrupt active
generation fails closed with `registry_corrupt`; it cannot expose partial or
unpinned data.

## 8. Git And Security Controls

Git operations run with:

- `GIT_TERMINAL_PROMPT=0`;
- `GIT_SSH_COMMAND` containing `BatchMode=yes` and
  `StrictHostKeyChecking=yes`;
- non-interactive deny helpers for `GIT_ASKPASS` and `SSH_ASKPASS`;
- no automatic unknown-host-key acceptance;
- a fixed timeout and bounded repository cache.

The initial error taxonomy is:

```text
invalid_source, scope_denied, not_registered, not_indexed, invalid_skill,
invalid_path, fetch_failed, index_failed, drift_detected, source_unavailable,
registry_corrupt, permission_denied, size_limit_exceeded, busy,
invalid_cursor, cursor_stale, binary_not_supported, registration_conflict
```

Security invariants:

- no arbitrary path reads or writes;
- no local-path, plain-HTTP, or unregistered-repository fetches;
- no checkout hooks, submodule execution, package scripts, or dependency
  installation;
- no symlink escape, `..` traversal, unsupported binary exposure, or manifest
  conflict promotion;
- no credential-bearing output or persisted raw Git prompt;
- no model-controlled profile, state-root, limit, or confirmation override;
- skill text is untrusted data and cannot override system, user, `AGENTS.md`,
  SOW, or host policy;
- writable tools are isolated in a separate profile and protected by host
  approval/HITL.

## 9. Host Wiring And Startup

The service is started from the AISkills checkout during v1 and is not copied
into native skill directories. The direct development command is:

```text
uv run --project <AISkills_ROOT> python -m mcp_skills_market.server
```

Codex registers the same stdio command through its own configuration surface:

```text
codex mcp add aiskills-market --env MCP_SKILLS_MARKET_MODE=readonly \
  --env MCP_SKILLS_MARKET_SCOPE=project --env MCP_SKILLS_MARKET_SCOPE_ROOT=<PROJECT_ROOT> \
  -- uv run --project <AISkills_ROOT> python -m mcp_skills_market.server
codex mcp list
codex mcp get aiskills-market
```

Claude Code uses its own project or user scope:

```text
claude mcp add aiskills-market --scope project \
  --env MCP_SKILLS_MARKET_MODE=readonly \
  --env MCP_SKILLS_MARKET_SCOPE=project \
  --env MCP_SKILLS_MARKET_SCOPE_ROOT=${CLAUDE_PROJECT_DIR} \
  -- uv run --project <AISkills_ROOT> python -m mcp_skills_market.server
claude mcp list
claude mcp get aiskills-market
```

The command examples are host wiring instructions, not executable artifacts in
the repository. Replace placeholders outside the checked-in documentation.
Host configuration must not commit machine-specific absolute paths, tokens, or
project-local credentials. Use a separate explicitly approved writable profile
for registration, refresh, and removal; keep the default profile read-only.

## 10. Planned Repository Implementation Layout

The implementation SOW may add the following modules without creating an
`__init__.py` solely for this service:

```text
mcp_skills_market/
  server.py        # MCPServer construction and serve_stdio entrypoint
  config.py        # process configuration and profile identity
  contracts.py     # typed inputs, outputs, manifests, and registry schemas
  errors.py        # stable error taxonomy and SDK tool-error mapping
  storage.py       # JSON generations, lock, atomic promotion, recovery
  git_source.py    # controlled system-Git subprocess adapter
  indexer.py       # required registry validation, package checksums
  registry.py      # profile-bound registration and lifecycle operations
  discovery.py     # query, pagination, and bundle reads
tests/mcp_skills_market/
  test_contract.py
  test_storage.py
  test_git_source.py
  test_indexer.py
  test_registry.py
  test_stdio_smoke.py
docs/mcp-skills-market.md
docs/mcp-skills-market-architecture.md
```

The actual module boundaries may be simplified if the approved SOW preserves
the same ownership, contracts, and security invariants. Product/runtime code
must not contain task-specific demo or smoke behavior.

## 11. Verification And Acceptance

Verification is evidence-based and is required before SOW closeout:

| Layer | Required evidence |
| --- | --- |
| Contract | SDK in-memory `Client(server)` calls prove schemas, structured results, and domain-error payloads |
| Storage | Fixture tests prove generation swaps, lock timeout, recovery, corruption fail-closed behavior, and profile isolation |
| Source | Tests prove URL policy, pinned commits, Git timeout, credential-prompt denial, and no hook/script execution |
| Index | Tests prove required-registry validation, rejection of fallback layouts, path containment, symlink/binary rejection, checksums, limits, and deterministic sort |
| Discovery | Tests prove registered-only search, cursor binding, refresh invalidation, duplicate handling, and empty query |
| Protocol | A real stdio subprocess smoke proves startup, handshake, calls, stderr/stdout separation, and shutdown |
| Host | Separate Codex and Claude runs prove list/status, registered discovery, skill read, unregistered negative, and read-only mutation denial |
| Boundary | A negative check proves no `skills.sh` lookup, native installation, arbitrary write, or credential-bearing response |

If a host is unavailable, provider-facing behavior is **not verified** and the
SOW cannot be represented as fully complete. Closeout must separate definitely
implemented, simulated, and unverified behavior, and include exact commands,
scenarios, observed results, and residual gaps.

## 12. Decisions, Tradeoffs, And Deferred Work

| Decision | Reason | Tradeoff |
| --- | --- | --- |
| Official SDK v2 | Keeps protocol framing, schemas, and error behavior aligned with MCP | Adds a dependency and requires a locked major version |
| `stdio` child process | No network listener, simple host ownership, narrow attack surface | Each host/profile has a process and cannot share live memory |
| JSON generations | Inspectable, diffable, easy to validate and atomically replace for a small registry | Requires explicit locking and generation recovery as scale grows |
| Bare Git cache | Uses the user's existing Git credentials and preserves pinned commits | Requires careful subprocess and host-key hardening |
| External state root | Keeps runtime/cache/locks out of the public Git worktree | State backup and cleanup are operator responsibilities |
| Registered repositories only | Makes source authority explicit and prevents accidental Internet ingestion | Discovery is limited until the user registers a source |
| No native installation | Separates catalog trust from host filesystem mutation | A later install workflow needs a new explicit contract |

Deferred until an approved SOW extension: HTTP/SSE transport, hosted service,
SQLite or another database, Internet-wide catalog search, `skills.sh` as a
source, arbitrary resources/prompts, automatic native installation, shared
cross-profile registry, and generic write operations.

## 13. Review Record

The architecture document was reviewed twice on `2026-09-23` before any
implementation work:

1. **Scope and contract review** at `2026-09-23T14:56:32+07:00`: checked that
   the document covered the SOW boundary, fixed stack, MCP I/O, operations,
   source layout, profiles, state lifecycle, host wiring, security, and
   verification. The review fixed the creation timestamp, made local write
   authority explicit, and added the minimum registry-entry fields.
2. **Security and consistency review** at `2026-09-23T15:02:25+07:00`:
   cross-checked this document against SOW_0093 and the plan, checked URL/Git
   restrictions, profile isolation, error taxonomy, host placeholders, secret
   patterns, and closeout evidence. No residual findings were found.

Evidence for both passes was read-only `uv run python` assertion coverage plus
`git diff --check` on this document, the SOW, and the plan. These checks prove
document consistency only; they do not prove the MCP runtime, Codex, or Claude
integration, which remain implementation-phase evidence.

Post-review amendment at `2026-09-23T15:10:48+07:00` tightened repository
acceptance: a valid `skills/registry.json` and its declared packages are now
mandatory; plugin or manifest-free layouts are rejected, with no fallback scan.
The same rule was written back to SOW_0093 and the plan.

## 14. References

- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [MCP Python SDK getting started](https://py.sdk.modelcontextprotocol.io/get-started/)
- [MCP Python SDK error handling](https://py.sdk.modelcontextprotocol.io/servers/handling-errors/)
- [OpenAI Codex MCP configuration](https://developers.openai.com/learn/docs-mcp)
- [Claude Code MCP configuration](https://code.claude.com/docs/en/mcp)
