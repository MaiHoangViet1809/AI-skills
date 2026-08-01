---
name: verify-design-mirror
description: Independently verify source-to-target UI design fidelity using a DESIGN.md package, design-mirror-evidence.json, design-mirror-mapping.md, rendered target output, and target behavior checks. Use when the user asks to audit, compare, validate, QA, or regression-test whether a mirrored design style was applied correctly.
---

# Verify Design Mirror

Verify design fidelity independently from the implementation step. A full verification claim requires the source design package and `design-mirror-mapping.md`; missing artifacts downgrade affected checks to `not_verified`.

The verifier reports findings. It must not silently edit implementation code or refresh baselines to make a mismatch pass.

## Workflow

1. Gather verification inputs.
   - Source package: `DESIGN.md`, `design-mirror-evidence.json`, and optional `screenshots/`.
   - Target handoff: `design-mirror-mapping.md`.
   - Target runtime: built UI, source files, tests, screenshots, or browser-accessible routes.
   - If any required input is missing, mark affected items `not_verified`.

2. Control the comparison environment.
   - Record browser, OS, viewport, device pixel ratio, fonts, theme, animation handling, data state, and build command when applicable.
   - Use deterministic browser conditions when feasible.
   - Never bootstrap a passing baseline from the target currently under test.

3. Run the fidelity matrix.
   - Read `references/fidelity-matrix.md` before scoring.
   - Combine structural checks, token coverage, rendered visual inspection, interaction states, responsive behavior, accessibility, and target behavior preservation.
   - Pixel or screenshot comparison alone cannot decide the result.

4. Score each item.
   - Use `pass`, `approximate`, `fail`, or `not_verified`.
   - Include evidence, source claim id when available, target mapping id when available, and explanation.
   - Keep inferred source claims lower confidence than observed source claims.

5. Write `design-mirror-verification.md`.
   - Place it only in a user-approved project or artifact root.
   - Include environment, result matrix, evidence, limitations, follow-up required, and whether a bounded apply-to-verify repair loop is authorized.
   - Return repair findings to `apply-design-mirror` or the target execution workflow; do not apply repairs inside this skill unless the user explicitly changes scope and target authority allows it.

## Stop Conditions

- The user asks to update baselines before explaining mismatches.
- The reference package or target runtime is unavailable and the requested conclusion requires it.
- The comparison would expose sensitive screenshots or data without approval or masking.
- The requested repair would require target code changes without target authority.

## Output

`design-mirror-verification.md` must separate:

- verified pass/fail evidence;
- approximate matches and accepted deviations;
- not verified areas;
- implementation findings that require a repair loop;
- environment limitations that could change visual results.

## Resource

Read `references/fidelity-matrix.md` before producing or reviewing a verification report.
