# SOW_0092 - Codex Router External Subagent Message Compatibility

- **Status**: DONE
- **Approval**: approved by user
- **create_dttm**: unknown
- **approve_dttm**: `2026-09-20T05:19:34+07:00`
- **finish_dttm**: `2026-09-20T21:10:57+07:00`
- **Task**: Convert decrypted Codex collaboration `agent_message` items into
  standard user messages at every non-direct routed provider boundary so
  external subagents reliably receive their delegated task.
- **Location**:
  - local target checkout for this SOW:
    `/Users/maihoangviet/Projects/tools/codex-router`
  - `$CODEX_ROUTER_CHECKOUT/src/router.mjs`
  - `$CODEX_ROUTER_CHECKOUT/src/namespace-relay.mjs`
  - `$CODEX_ROUTER_CHECKOUT/test/routing.test.mjs`
  - `$CODEX_ROUTER_CHECKOUT/test/namespace-relay.test.mjs`
  - `$CODEX_ROUTER_CHECKOUT/src/subagent-certify.mjs`
  - `$CODEX_ROUTER_CHECKOUT/src/codex-agent-catalog.mjs`
  - `$CODEX_ROUTER_CHECKOUT/src/catalog.mjs`
  - `$CODEX_ROUTER_CHECKOUT/src/doctor.mjs`
  - `$CODEX_ROUTER_CHECKOUT/src/control.mjs`
  - `$CODEX_ROUTER_CHECKOUT/test/codex-agent-catalog.test.mjs`
  - `$CODEX_ROUTER_CHECKOUT/test/subagent-certify.test.mjs`
  - `$CODEX_ROUTER_CHECKOUT/docs/HOW-IT-WORKS.md`
  - `$CODEX_ROUTER_CHECKOUT/docs/SUBAGENT-CERTIFICATION.md`
  - `patches/codex-router/0001-external-subagent-message-compat.patch`
  - `patches/codex-router/0002-luna-routed-child-provider-domain.patch`
  - `patches/codex-router/README.md`
  - this SOW
- **Why**: Codex Multi-Agent V2 delivers delegated instructions as a private
  `agent_message`. Codex Router recovers the plaintext from
  `encrypted_content`, but generic external routes still receive the private
  item type. GreenNode GLM-5.2 and GLM-5.3 Flash consequently answer inherited
  ordinary chat or report that no task was supplied.
- **Proposed-By**: Codex
- **Plan / Reference**:
  - `plan_todo/SOW_0056_codex_router_claude_cli_native_subagent.md`
  - `https://github.com/openai/codex/issues/33551`
  - `$CODEX_ROUTER_CHECKOUT/docs/SUBAGENT-CERTIFICATION.md`

## Root-Cause Evidence

- Both affected GreenNode models resolve to the same provider boundary:
  `custom`, `openai-responses`, `directResponses=false`.
- The inspected Codex Router checkout was at `3f1ca21`; implementation must
  revalidate HEAD and the named call sites before editing if that revision has
  changed.
- Parent rollout records store the delegated `spawn_agent.message` as
  `gAAAA...` ciphertext.
- Child rollout records receive that value as
  `agent_message.content[].encrypted_content`.
- `normalizeRoutedAgentInput()` recovers readable `input_text` but preserves
  `type: agent_message`.
- `agentMessagesAsUserMessages()` already implements the required standard
  conversion, but the ordinary non-direct routed path does not call it.
- Before the scoped change, relay tests asserted plaintext recovery but did not
  assert that the provider receives a public Responses `message` item.
- With `fork_turns=none`, the routed model sees no ordinary task and asks for
  one. With `fork_turns=1`, it sees the inherited parent user message and
  answers that instead. This is deterministic transport behavior, not random
  context leakage or a model-comprehension failure.

## Latest Verification

- Router restarted successfully and reports healthy.
- Focused tests and `npm run check` pass.
- Scoped router commit `c8deaaa569c396b86620cc60e5ff70cb095883f` contains only
  the five SOW-owned router, test, and documentation paths.
- The recovery patch applies cleanly to base
  `3f1ca211a62b5ebbb855673e6f115810b72c5aba`; replayed focused tests pass with
  118 relay tests and 116 routing tests. The sanitized patch/provenance
  artifact is recorded in AISkills commit `f976676`.
- Earlier live-certification attempts used either native `gpt-5.6-sol` or a
  routed GLM parent. Neither reproduces the original Luna-to-GLM path, so those
  outcomes are retained only as superseded experiment evidence.
- Extension 1 fixes the certification topology to native `gpt-5.6-luna` at
  `max` delegating to the selected routed GLM child through the authenticated
  encrypted relay. The child remains in the built-in `openai` provider domain;
  `openai_base_url` routes that transport through Codex Router.
- Both `custom/greennode-glm-5.2` and
  `custom/greennode-glm5.3-flash-thirdparty` passed all five live checks:
  streaming, tool call, encrypted relay, delegated marker return, and
  same-child follow-up.
- The product path uses `fork_turns=none`. The `fork_turns=1` case is only an
  isolated synthetic negative regression and receives no operator conversation.
- Focused catalog, control, doctor, and certification tests pass: 134/134.
  `npm run check` and `git diff --check` pass.
- The full repository suite was attempted but is not claimed clean because of
  unrelated environment/pre-existing failures, including the active Python
  runtime lacking `os.waitstatus_to_exitcode`.
- Router commit `0f5f45f50857a8dc154bc0b8e5f9e2f991484aff` contains only
  the eight Extension 1 paths. Recovery patch `0002` records that commit with
  SHA-256 `3f95d9c46ff7282a33f9a2c245c926303a50643e7e9fdc4a787c7ac8531a1109`.
- Catalog refresh generated both managed child definitions with
  `model_provider = "openai"`; doctor reports 2/2 current definitions, router
  configuration active, and router version 0.5.1 healthy. A full Codex Desktop
  quit/reopen is only the operator activation step for the already-running UI
  process, not missing implementation or live-proof evidence.

## As-Is Diagram (ASCII)

```text
Codex parent
    |
    | NEW_TASK as encrypted agent_message
    v
Codex Router
    |
    | decrypt encrypted_content -> input_text
    | retain type = agent_message
    v
Non-direct routed provider
    |
    | private item unsupported / ignored
    v
Child misses task
    +-- fork_turns=none -> "ready / send task"
    `-- fork_turns=1    -> answers inherited parent chat
```

## To-Be Diagram (ASCII)

```text
Codex parent
    |
    | encrypted agent_message
    v
Codex Router collaboration boundary
    |
    +-- direct/native Responses route -> existing native representation
    `-- every non-direct routed provider
            |
            +-- recover plaintext or fail closed
            +-- convert once to message(role=user)
            v
       Routed child receives exact task
            |
            +-- NEW_TASK
            +-- MESSAGE / FOLLOWUP_TASK
            `-- existing reverse return path remains unchanged
```

## Implementation Decision

- Apply `agentMessagesAsUserMessages()` immediately after
  `normalizeRoutedAgentInput()` has recovered collaboration plaintext, before
  aging, compaction preparation, image bridging, tool-history rewriting, or
  provider request construction.
- Apply the same normalized representation to ordinary turns and routed
  compaction so replay cannot reintroduce the private item.
- The direct Responses branch bypasses this compatibility boundary and remains
  byte-compatible with its existing native contract.
- Do not add provider IDs, model-name conditions, prompt injection, duplicate
  task messages, fallback delivery, or another converter.
- Extend the existing helper only to retain a stable item `id` for router-side
  compaction correlation while omitting private sender fields; do not preserve
  `author` or `recipient` as provider-facing fields.
- The reverse routed-child-to-native normalization is verification-only in this
  SOW; its implementation is not changed unless review finds a separate proven
  defect and the SOW is explicitly extended.

## Deliverables

1. Normalize decrypted collaboration input once at the non-direct routed
   provider boundary. Those providers receive:

   ```json
   {
     "type": "message",
     "role": "user",
     "content": [{"type": "input_text", "text": "..."}]
   }
   ```

2. Reuse the existing `agentMessagesAsUserMessages()` helper rather than
   introducing a second converter, model-specific branch, facade, fallback, or
   duplicated payload parser.
3. Preserve direct/native provider behavior and fail-closed encrypted-payload
   handling.
4. Cover initial task and follow-up/message delivery through the same inbound
   compatibility path; verify that the existing reverse return path is not
   regressed.
5. Extend router tests to assert the exact gateway request shape, not merely
   plaintext presence.
6. Add synthetic regression fixtures representing isolated and
   inherited-context child inputs. `fork_turns` itself remains a Codex lifecycle
   option and is verified through live collaboration, not simulated as router
   business logic.
7. Update router documentation with the standard-message compatibility
   boundary.
8. Restart only the installed Codex Router service after the scoped code and
   tests pass and the restart precondition below is satisfied, then run the
   bounded live checks. Do not reinstall the router or modify provider
   credentials/catalog selection.
9. After verification, save the scoped commit as
   `patches/codex-router/0001-external-subagent-message-compat.patch` and write
   its sanitized provenance in `patches/codex-router/README.md`. Record the
   source repository, upstream/base revision, resulting scoped commit, affected
   relative paths, patch SHA-256, verification evidence, and retirement rule.
   These files are the reinstall recovery artifact; they contain no
   credentials, decrypted prompts, rollout content, username, or machine-local
   absolute paths.

## Done Criteria

- Unit/regression tests prove the outbound non-direct routed request contains
  `type: message`, `role: user`, the exact recovered synthetic task text, and no
  `agent_message` or `encrypted_content` for that delegated item.
- Tests exercise both a Responses-shaped external route and a translated
  Chat-Completions route, establishing that the boundary is transport-generic
  rather than GreenNode-specific.
- A negative test proves direct/native Responses routing bypasses the
  conversion, while an unreadable encrypted payload still fails closed.
- Routed compaction receives the same public message representation and cannot
  replay `agent_message` to the external provider.
- Initial and follow-up delivery use the same compatibility boundary; no
  second message path or duplicated task is introduced.
- Live GreenNode verification succeeds independently for GLM-5.2 and GLM-5.3
  Flash with `fork_turns=none`: each child returns a unique synthetic marker
  supplied only in the delegated task rather than a readiness response.
- Live verification with `fork_turns=1` uses distinct markers in inherited chat
  and delegated task inside a newly created synthetic certification thread; the
  child must return the delegated-task marker. This is a negative regression
  test only: the final product path remains `fork_turns=none` and never supplies
  the operator conversation to the child.
- A same-child follow-up returns a third unique marker, establishing continued
  collaboration rather than spawn-only success.
- Existing routed-subagent and focused routing tests pass.
- Before restarting the installed service, compare its running revision with
  the checkout and inventory every dirty runtime-loaded source/config file. If
  restart would activate an unrelated uncommitted change, stop for an explicit
  ownership decision or use a proven isolated test instance; do not produce
  mixed-change live evidence.
- After a scope-clean restart, the installed router reports healthy. When the
  managed agent definitions change, catalog refresh must request a full Codex
  Desktop quit/reopen so an already-running UI process reloads them.
- The durable patch applies cleanly to the recorded base revision in a clean
  temporary checkout, and the focused regression suite passes there.
- The generated patch contains exactly the scoped Codex Router commit and no
  AISkills planning files or pre-existing dirty work.
- The implementation commit in `codex-router` contains only SOW-owned files;
  existing unrelated changes to `src/model-registry.mjs`,
  `test/per-model-endpoint-protocol.test.mjs`, and the existing GreenNode patch
  are preserved and excluded. The scoped helper and its focused test are
  explicitly included.
- Negative completion check: if a child succeeds only because the task was
  copied into inherited chat, or a test checks plaintext without checking the
  outbound item type, this SOW is not complete.

## Concept Compliance

- **Applicable Concepts**: No AgentHangar product concept changes. This is a
  provider-transport interoperability correction in Codex Router.
- **Concept Change**: No.
- **Required Concept Updates**: None. The fix preserves Codex ownership of the
  collaboration lifecycle and adapts only the external provider wire boundary.

## Public / Local Artifact Boundary

- This SOW remains local-only unless its local operational references are
  sanitized and the user separately approves tracking it in the public
  AISkills repository.
- The durable code patch and provenance note may be tracked only after a
  privacy review confirms they contain public source diffs and sanitized
  metadata exclusively.
- Runtime rollouts, decrypted task text, credentials, local service state, and
  machine-specific paths never enter AISkills history.

## Out-of-Scope

- Changing AgentHangar runtime, prompts, skills, or product concepts.
- Downgrading the whole root/child tree to Multi-Agent V1.
- Model-specific GreenNode prompt injection or special-case task duplication.
- Changing model catalog eligibility, reasoning effort, provider credentials,
  or certification policy beyond the isolated harness correction authorized by
  Extension 1.
- Modifying Codex Desktop or Codex CLI source.
- Persisting plaintext delegated prompts in patch artifacts, logs, or tests.
- Reinstalling Codex Router or restarting Codex Desktop.
- Changing the existing reverse collaboration implementation without a proven
  defect and explicit SOW extension.

## Cautions / Risks

- Converting outside the non-direct routed boundary could change native OpenAI
  collaboration semantics; routing identity, not model name, selects the path.
- The visible collaboration header and recovered payload must remain ordered so
  the child retains task identity and sender metadata.
- A provider returning HTTP 200 does not prove it consumed the delegated task;
  marker-based behavioral verification is required.
- Live tests consume provider quota and must be bounded to the listed cases.
- The Codex Router checkout currently contains unrelated local changes. They
  must not be staged, rewritten, included in the scoped commit, or captured in
  the reinstall patch.
- The current dirty `src/model-registry.mjs` is runtime-loaded. Restarting from
  that checkout may activate behavior outside this SOW even if it is not
  committed. This is a hard live-verification gate, not permission to clean,
  commit, stash, or include that file.
- Patch replay is recovery evidence, not an alternate runtime or permanent
  fork. Before replay, compare against current upstream behavior and require a
  clean applicability check. If upstream implements the same boundary, retire
  the local patch rather than layering both implementations.

## Extension 1: Luna-Max Native Collaboration Certification

- **Status**: DONE
- **Approval**: approved by user
- **create_dttm**: `2026-09-20T19:22:51+07:00`
- **approve_dttm**: `2026-09-20T19:22:51+07:00`
- **finish_dttm**: `2026-09-20T21:10:57+07:00`
- **Finding**: The original runtime defect is specifically native
  `gpt-5.6-luna` at `max` delegating to a routed GLM child. Replacing Luna with
  the candidate route as parent changed the topology and conflated GLM parent
  tool-following with the child-content boundary under test.
- **Decision**:
  - keep the implemented `agent_message -> message(role=user)` compatibility
    boundary unchanged;
  - use native `gpt-5.6-luna` with reasoning effort `max` as the fixed parent;
  - use the real authenticated Codex home because Luna must produce the native
    encrypted collaboration payload and the router must relay it with the
    existing ChatGPT bearer;
  - keep the candidate `custom/...` route exclusively as the child under test;
  - keep the child in the built-in `openai` provider domain and point that
    transport to Codex Router through `openai_base_url`; this preserves native
    relay auth without triggering Codex's cross-provider account rejection;
  - treat any account-policy rejection as a harness/runtime finding to resolve,
    not as permission to replace Luna or weaken the child acceptance checks.
- **Location**:
  - `$CODEX_ROUTER_CHECKOUT/src/subagent-certify.mjs`
  - `$CODEX_ROUTER_CHECKOUT/src/control.mjs`
  - `$CODEX_ROUTER_CHECKOUT/test/subagent-certify.test.mjs`
  - `$CODEX_ROUTER_CHECKOUT/docs/SUBAGENT-CERTIFICATION.md`
  - this SOW
- **Done Criteria**:
  - certification uses native `gpt-5.6-luna` at `max` from the real authenticated
    Codex home while restoring any temporary candidate agent definition;
  - the child remains in the native `openai` provider domain while its exact
    custom model slug resolves through Codex Router, which receives the native
    encrypted collaboration payload;
  - `fork_turns=none` returns a unique delegated marker from the child;
  - an isolated synthetic `fork_turns=1` negative regression returns the
    delegated marker rather than its synthetic parent marker; it is not the
    product configuration and receives no operator conversation;
  - a same-child follow-up returns a third unique marker;
  - focused certification tests and the existing router checks pass;
  - each live run remains quota-bounded and records no prompt, token, caller
    key, or machine-local credential path in durable proof artifacts.
- **Out-of-Scope**:
  - modifying Codex Desktop or Codex CLI;
  - adding a model alias, facade, hidden provider mapping, or router-owned agent
    orchestrator;
  - reading, copying, persisting, or logging ChatGPT credentials outside
    Codex's existing authenticated request path;
  - weakening promotion from all five checks or treating unit tests as live
    collaboration proof.
- **Cautions / Risks**:
  - running the parent through another routed model would no longer reproduce
    the approved Luna-to-GLM behavior and cannot close this SOW;
  - Codex account/model eligibility may differ between the Desktop-native tool
    path and the CLI harness, so the exact rejection owner must be identified
    before changing authentication or provider configuration.

### Extension 1 Superseded Experiment

- The isolated router-authenticated harness removes the ChatGPT-account gate;
  focused tests and the combined 254-test router/relay suite pass.
- GLM-5.2 has successfully spawned and returned the initial
  `fork_turns=none` marker in one run, but its later parent turns did not
  reliably call `spawn_agent` or return the child marker.
- GLM-5.3 Flash emitted only reasoning and an agent message after being told to
  call `spawn_agent`; no structured spawn tool-call event was produced.
- These runs used the wrong parent topology and are retained only as negative
  experiment evidence. They cannot certify or reject Luna-to-GLM delegation.

### Decision D001

- **Status**: approved
- **approve_dttm**: `2026-09-20T20:32:21+07:00`
- **Decision**: The parent/coordinator is always native `gpt-5.6-luna` at
  reasoning effort `max`; the target child is the selected GLM route through
  Codex Router.
- **Reason**: This is the original failed user path. A routed GLM parent tests a
  different behavior and cannot prove the Luna `fork_turns=none` defect fixed.
- **Impact**: Revert the candidate-as-parent harness experiment; preserve the
  real ChatGPT-authenticated relay path; no Codex source fork, model alias, or
  router-owned orchestration is introduced.

### Decision D002

- **Status**: approved by original SOW intent and the user's instruction to
  resolve the Luna-to-GLM path
- **Decision**: Managed routed-agent definitions use the provider identity that
  owns the active router transport: built-in `openai` in authenticated router
  mode, and `codex-router` only in login-free mode.
- **Reason**: The exact Luna `max` run proves `spawn_agent` creates the child,
  but Codex rejects it before any child request reaches the router because the
  definition hardcodes a custom `codex-router` provider under a ChatGPT account.
  The installed authenticated router deliberately intercepts built-in `openai`;
  forcing a separate provider contradicts that runtime contract.
- **Objective**: Keep Luna and the child in one Codex provider domain while the
  custom model slug still selects the external route inside Codex Router, so the
  encrypted delegated message reaches the existing compatibility boundary.
- **Plan**: Parameterize the existing agent-definition generator, pass the
  provider from catalog runtime mode, make certification temporarily install
  and exactly restore the expected authenticated definition, then rerun both
  live routes.
- **Impact**: Changes managed agent TOML generation and focused tests only; no
  Codex fork, provider alias, fallback delivery, or router-owned orchestrator.
  Login-free behavior remains on its existing `codex-router` provider.
