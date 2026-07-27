# Inline Rule Template

Use this for `docs/concept/inline_rules.md`.

```md
# Inline Rules

Short rules that are too small for mature concept files but still govern future
implementation and reviews.

| ID | Rule |
| --- | --- |
| `IR-UI-01` | UI component changes must not alter unrelated global styling unless that is the explicit task. |
| `IR-WF-01` | Run actions must not implicitly save drafts. |
```

Rules should be directly actionable and self-contained. If a rule needs a model,
lifecycle, ownership explanation, or many exceptions, promote it to a mature
concept.
