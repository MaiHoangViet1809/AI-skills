# Codex Router external subagent message compatibility

This directory contains a reinstall/recovery patch for SOW_0092. It is a
derived artifact, not a replacement runtime checkout.

## Provenance

- Source repository: `https://github.com/duolahypercho/codex-router.git`
- Upstream/base revision: `3f1ca211a62b5ebbb855673e6f115810b72c5aba`
- Scoped source commit: `c8deaaa569c396b86620cc60e5ff70cb095883f4`
- Patch: `0001-external-subagent-message-compat.patch`
- Patch SHA-256: `14d5ea06f337d7cfead4b3c4241a7f080ed580a3671fa9c44d6ce1cf1d07b6fd`
- Affected paths:
  - `src/router.mjs`
  - `src/namespace-relay.mjs`
  - `test/routing.test.mjs`
  - `test/namespace-relay.test.mjs`
  - `docs/HOW-IT-WORKS.md`

## Verification

- `npm run check` passed.
- `node --test test/namespace-relay.test.mjs` passed: 118 tests.
- `node --test test/routing.test.mjs` passed: 116 tests.
- The installed router service reported healthy after the scoped runtime
  restart/readiness check.
- Live GreenNode marker checks remain deferred: the active ChatGPT account
  rejects custom-model subagent creation before a child turn starts. No live
  success is claimed here.

## Replay and retirement

Before replay, verify that the checkout is clean and still based on the
recorded upstream revision. Apply the patch in a temporary checkout, rerun the
focused tests, and review the resulting diff before activating it. If upstream
implements the same non-direct `agent_message` to user-message boundary, retire
this patch instead of layering a duplicate implementation.

This artifact contains only public source changes and synthetic test fixtures;
it must not be extended with credentials, decrypted production prompts,
rollout content, or machine-specific paths.
