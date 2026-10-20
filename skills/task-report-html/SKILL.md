---
name: task-report-html
description: Create or update durable analytical, benchmark, technical or business reports and report-style dashboards with evidence-backed conclusions and visual-first HTML. Not for quick chat answers, task progress, mechanism-only diagrams or frontend application development.
---

# Visual-First HTML Reports

Make the answer visible before explaining it. Own report presentation and evidence
communication, not a new analysis engine or application framework.

## Set The Report Boundary

- Identify the question, audience and decision from existing context. Read the
  supplied sources and any existing report before choosing the presentation.
- Default a durable report to HTML. An explicit format or project contract wins;
  preserve PDF, slides or Markdown when requested, using appropriate tooling.
- Reuse the project's report location, design and available rendering tools.
  A portable HTML file is often enough. Do not mandate a library, server,
  dependency or framework, or rewrite existing report architecture.
- Quick answers and progress updates stay in chat. Mechanism-only explanations
  and frontend applications retain their own workflows. Preserve applicable
  specialist analysis/tool contracts; this skill does not override them or
  authorize publishing, deployment or unrelated edits.

## Choose The Visual From The Question

- Comparisons: aligned bars or dots; trends and load curves: lines; distributions:
  percentiles, histogram or box plot when observations support them. Mechanisms,
  ownership and handoffs: diagrams with meaningful labeled connections.
- Give each figure a clear question and takeaway. Use consistent units, readable
  labels and comparable scales. Show relevant sample counts and missing/failed
  observations; color alone must not carry meaning.
- Prefer diagrams/charts/graphs over tables and narrative. Use compact tables
  for exact lookup or relationships a visual would obscure, and prose for short
  interpretation. Do not add decorative figures or arbitrary chart quotas.
- Keep key evidence visible without making readers open every detail panel.
  Put long methods and supporting detail after the main result or in optional
  details when useful. Do not hide limitations that change the conclusion.

## Ground The Conclusion

- Lead with the answer, supported magnitude and operational meaning; recommend
  a next decision only when justified. Keep explanations short and plain.
  Do not force a change-over-time story when the question is different.
- Trace every headline result and chart to sources, calculations and relevant
  run/date identities. Compact links or notes suffice; do not build a separate
  provenance subsystem. Never invent missing values or recover percentiles
  from averages.
- Distinguish observations from interpretation and recommendations. Partial
  runs, resource differences, workload/scale, cache policies and measurement
  definitions can invalidate a ranking: make those differences visible rather
  than presenting false parity or inventing normalization.
- When evidence cannot answer the question, state precisely what is supported,
  what remains unknown and the minimum missing evidence. A sharp conclusion is
  not a stronger claim than the data permits; correlation is not causality.

## Verify And Deliver

- Cross-check headline values, chart inputs, units and derived comparisons
  against the source, including failed/empty data where relevant. Distinguish
  unavailable from zero and measured from estimated values.
- Inspect the rendered artifact at its intended viewing size when possible:
  readable axes/labels, no clipping or overlap, meaningful contrast/text
  alternatives, keyboard-operable controls and working source links. Keep
  offline delivery usable without remote dependencies when required.
- Without reading the long notes, can the reader identify the answer, supporting
  comparison and material limitation? Remove repetition or redraw if not.
- Deliver the artifact link and a concise takeaway. State unavailable rendering
  or evidence checks honestly; source/structural validation is not rendered
  verification, and a polished report is not runtime acceptance.
