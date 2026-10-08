# SOW_20260920_9851QRQ4_EXT_7MPLVEOK - Extension 1: Luna-Max Native Collaboration Certification

- Status: DONE
- Approval: approved by user
- create_dttm: 2026-09-20T19:22:51+07:00
- approve_dttm: 2026-09-20T19:22:51+07:00
- finish_dttm: 2026-09-20T21:10:57+07:00
- legacy_id: SOW_0092_EXT_1
- legacy_path: plan_todo/SOW_0092_codex_router_external_subagent_message_compat.md
- migrated_dttm: 2026-10-08T12:48:51+07:00
- Parent: [SOW_20260920_9851QRQ4](SOW_20260920_9851QRQ4_codex_router_external_subagent_message_compat.md)

## Preserved Contract And Historical Evidence

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
