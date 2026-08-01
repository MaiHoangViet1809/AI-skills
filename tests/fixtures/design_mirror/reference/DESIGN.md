---
version: alpha
name: Design Mirror Source Fixture
colors:
  primary: "#2563eb"
  background: "#f7f9fc"
  surface: "#ffffff"
  text: "#172033"
  muted: "#64748b"
  border: "#dbe3ef"
typography:
  headline-lg:
    fontFamily: Inter
    fontSize: 32px
    fontWeight: 700
    lineHeight: 1.15
  body-md:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: 400
    lineHeight: 1.6
  label-sm:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: 700
    lineHeight: 1
    letterSpacing: 0.08em
spacing:
  sm: 8px
  md: 12px
  lg: 16px
  xl: 24px
rounded:
  card: 8px
  control: 6px
---

# Design Mirror Source Fixture

## Design Philosophy

Observed style is a quiet operational dashboard: neutral background, white cards, compact controls, blue primary action, restrained border, and low elevation.

## Evidence Summary

Claims are grounded in `design-mirror-evidence.json` and the source fixture CSS. Responsive behavior is observed from the source CSS media query. Motion is unsupported.

## Typography

Use Inter or a system sans fallback. Page titles are 32px desktop, 26px mobile, bold, and tight line height. Small labels are uppercase, 12px, bold, muted, and spaced.

## Spacing And Geometry

Use 8px, 12px, 16px, and 24px spacing roles. Cards use 8px radius; controls use 6px radius.

## Components And States

Primary buttons use white text on `#2563eb` with `#1d4ed8` hover. Disabled buttons use reduced opacity. Selected cards use the primary border. Error metrics use `#dc2626`.

## AI Agent Constraints

Reuse target-owned tokens and components. Do not create a parallel theme or wrapper component family. Treat motion as unsupported unless new evidence is supplied.
