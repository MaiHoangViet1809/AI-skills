---
name: task-diagram-explaination
description: Explain a system, workflow or decision through concise, evidence-grounded diagrams for meetings, documentation or HTML presentations. Use when the visual must make ownership, handoffs, branches or state changes understandable, not merely decorate prose. Not a general frontend redesign or charting skill.
---

# Task Diagram Explaination

Make the mechanism visible, not just the page attractive. A row of boxes filled
with paragraphs is still a document if readers must reconstruct the relationships.

## Start From The Question And Evidence

- Identify the audience and what they should understand or decide. Reuse context;
  ask only when missing information materially changes the explanation.
- Read the actual implementation, accepted design or supplied source before
  explaining behavior. Distinguish current behavior, proposed behavior and
  illustrative examples. Do not invent automation, approvals or guarantees.
- Inspect an existing successful visual when one is supplied. Reuse its visual
  language and useful patterns, not its application-specific labels or assumptions.
- Respect the requested format and project conventions. A quick ASCII diagram
  may be enough; an HTML presentation may need a carefully laid-out SVG.
  Do not force a renderer, palette, font, dependency or separate deliverable.

## Choose The Visual Grammar Before Styling

Give each figure one central question. Use only the relationships that answer it:

| Question | Useful visual |
| --- | --- |
| Where does data or a request go? | Flow with labeled handoffs |
| Who declares, executes or owns what? | Lanes, boundaries or grouped responsibilities |
| Why is an item accepted or excluded? | Selector with explicit outcomes |
| What happens after success or failure? | Branch and relevant return/retry path |
| What changed after each step? | State progression aligned with those steps |
| How does one identifier resolve in different contexts? | One reference branching into context-owned configurations |

These are options, not mandatory panels. Use a table for a small exact mapping;
split a diagram only when combining questions obscures the explanation.

### Keep Semantics Precise

- Decide what nodes and edges mean. Distinguish an artifact, a task, a data
  transfer, a dependency and a consumer read; not every arrow is an execution task.
- Label important boundaries with the real owner or API when that improves
  comprehension. Do not turn an implementation detail into the headline.
- Show a failure/return branch when it explains the mechanism; do not invent
  retries or draw every possible failure for completeness.
- Separate permission/configuration from execution and observable result.
  A local edit, deployment and active runtime state are distinct events.
- Align state indicators with the step that actually changes state. Explain
  marker meaning and initial assumptions; color alone must not carry the meaning.
- When useful, include a short “is / is not” boundary to prevent a likely
  misunderstanding. Do not add a wall of disclaimers.

## Build For A Meeting, Not A Manual

- Lay out topology and reading order first; apply styling afterward.
- Use a clear title, short node names and one supporting line where practical.
  Move credentials/config fields, code and secondary detail outside the figure.
- Use spacing, alignment and typography to distinguish stages from responsibilities.
  Equal-size boxes are fine for equivalent peers, not a default for every idea.
- Make focal decisions visibly stronger than supporting structure. Use restrained
  color for meaningful states or categories, consistent across the page.
- Route connectors without ambiguous endpoints or labels crossing text. Prefer
  direct or orthogonal paths; make return paths distinguishable from forward flow.
- Retain accessibility: readable labels, sufficient contrast, text alternatives
  and keyboard access for any controls. Adapt to the intended display; do not
  sacrifice presentation-scale readability to fit everything into one figure.
- Keep static explanations static. Add interaction or animation only when the
  request or explanation benefits from it. Avoid decorative dashboard controls.

## Verify Understanding As Well As Rendering

Review the visual against its source, including a relevant excluded/failure case.
Check that a simplified diagram has not changed ownership, prerequisites or outcomes.

When rendering is available, inspect the actual output at the intended viewing
size. Look for clipping, unreadable labels, overlaps, excessive scrolling and
broken resources. For an offline deliverable, avoid or package external resources.
If rendering is unavailable, label visual verification incomplete; source inspection
is not a substitute. Reuse a valid rendering tool rather than installing one just
to satisfy this skill.

Then apply a quick-reader check:

```text
Without reading the paragraphs, can the viewer identify:
  the starting point -> owner/action -> decision or handoff -> resulting state?
```

Remove, shorten or redraw anything that requires the presenter to reconstruct
the missing relationship verbally. This is a design heuristic, not a claim of
measured comprehension or a reason to add unnecessary branches/state strips.

## Delivery

Deliver the requested artifact or explanation, summarize its main takeaway and
state verification limits briefly. Do not claim the drawing is live telemetry or
that a good-looking illustration proves runtime correctness. Do not modify runtime
behavior, publish, install skills or alter unrelated files without authorization.
