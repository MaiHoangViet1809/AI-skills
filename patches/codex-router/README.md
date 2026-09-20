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

The native Luna certification correction is recorded separately so the
provider-boundary fix can still be reviewed or retired on its own:

- Parent revision: `c8deaaa569c396b86620cc60e5ff70cb095883f4`
- Scoped source commit: `0f5f45f50857a8dc154bc0b8e5f9e2f991484aff`
- Patch: `0002-luna-routed-child-provider-domain.patch`
- Patch SHA-256: `3f95d9c46ff7282a33f9a2c245c926303a50643e7e9fdc4a787c7ac8531a1109`
- Affected paths:
  - `src/codex-agent-catalog.mjs`
  - `src/catalog.mjs`
  - `src/control.mjs`
  - `src/doctor.mjs`
  - `src/subagent-certify.mjs`
  - `test/codex-agent-catalog.test.mjs`
  - `test/subagent-certify.test.mjs`
  - `docs/SUBAGENT-CERTIFICATION.md`

## Verification

- `npm run check` passed.
- `node --test test/namespace-relay.test.mjs` passed: 118 tests.
- `node --test test/routing.test.mjs` passed: 116 tests.
- The installed router service reported healthy after the scoped runtime
  restart/readiness check.
- Native `gpt-5.6-luna` at `max` passed all five certification checks with each
  routed child: `custom/greennode-glm-5.2` and
  `custom/greennode-glm5.3-flash-thirdparty`.
- The product-path check uses `fork_turns=none`. The additional
  `fork_turns=1` check runs only in a new synthetic certification thread and
  receives no operator conversation.
- The focused catalog, control, doctor, and certification suite passed all 134
  tests; `npm run check` passed.
- The full repository suite was also attempted but is not claimed clean: it
  includes unrelated environment/pre-existing failures, including the active
  Python runtime lacking `os.waitstatus_to_exitcode`.

## Replay and retirement

Before replay, verify that the checkout is clean and still based on the
recorded upstream revision. Apply the patch in a temporary checkout, rerun the
focused tests, and review the resulting diff before activating it. If upstream
implements the same non-direct `agent_message` to user-message boundary, retire
this patch instead of layering a duplicate implementation.

This artifact contains only public source changes and synthetic test fixtures;
it must not be extended with credentials, decrypted production prompts,
rollout content, or machine-specific paths.
