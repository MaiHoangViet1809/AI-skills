# SOW_0092 - Codex Router External Subagent Message Compatibility

- **Status**: BLOCKED (implementation complete; live child verification awaits an eligible Codex account)
- **Approval**: Approved by user in the current task (`approve, nhớ poc cẩn thận nếu cần`) at `2026-09-20T05:19:34+07:00`
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
  - `$CODEX_ROUTER_CHECKOUT/docs/HOW-IT-WORKS.md`
  - `patches/codex-router/0001-external-subagent-message-compat.patch`
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
- Current relay tests assert plaintext recovery but do not assert that the
  provider receives a public Responses `message` item.
- With `fork_turns=none`, the routed model sees no ordinary task and asks for
  one. With `fork_turns=1`, it sees the inherited parent user message and
  answers that instead. This is deterministic transport behavior, not random
  context leakage or a model-comprehension failure.

## Latest Verification

- Router restarted successfully and reports healthy.
- Focused tests and `npm run check` pass.
- GLM-5.2 reached the child relay, but the child was rejected with HTTP 400 because the ChatGPT account does not support custom models.
- GLM-5.3 Flash was deferred for the same account restriction.
- Live marker and follow-up checks remain open; rerun them after switching to an account that permits custom subagents.

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
  and delegated task; the child must return the delegated-task marker.
- A same-child follow-up returns a third unique marker, establishing continued
  collaboration rather than spawn-only success.
- Existing routed-subagent and focused routing tests pass.
- Before restarting the installed service, compare its running revision with
  the checkout and inventory every dirty runtime-loaded source/config file. If
  restart would activate an unrelated uncommitted change, stop for an explicit
  ownership decision or use a proven isolated test instance; do not produce
  mixed-change live evidence.
- After a scope-clean restart, the installed router reports healthy; no Codex
  restart is claimed necessary because catalog/configuration is unchanged.
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
- Changing model catalog eligibility, certification policy, reasoning effort,
  or provider credentials.
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
