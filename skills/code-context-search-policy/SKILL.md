---
name: code-context-search-policy
description: Use when you need to search or navigate a codebase and must choose between semantic codegraph queries and text-first ripgrep. Prefer this skill before codebase exploration so the search method matches the question type.
---

# Code Context Search Policy

Use this skill before searching a codebase.

Goal:
- pick the right search method first
- reduce false positives
- avoid wasting turns on broad grep when semantic lookup is available

## Default rule

- Use `codegraph` first for symbol lookup, callers/callees, impact, and code-structure questions.
- Use `rg` first for literal text, config keys, error strings, logs, comments, and fuzzy wording.
- If the first method smells wrong, switch immediately instead of forcing it.

## Decision table

| Question type | Default tool | Why |
|---|---|---|
| Find a class/function/method/type by name | `codegraph_search` | Symbol-aware, cleaner than text grep |
| Understand a known symbol or code area | `codegraph_context` / `codegraph_node` | Better semantic context |
| Find callers / callees / impact radius | `codegraph_callers` / `codegraph_callees` / `codegraph_impact` | `rg` cannot infer graph relations |
| Explore indexed project structure | `codegraph_files` | Better than filesystem-glob for indexed repos |
| Find literal strings / env vars / config keys / error text | `rg` | Exact text match is the real task |
| Search with vague natural-language wording | `rg` first, then `codegraph` | Semantic query can drift if symbol names are unknown |
| Verify a suspected symbol after text discovery | `codegraph` | Good second step after `rg` |

## Recommended workflow

1. If the question names a symbol, start with `codegraph`.
2. If the question names text, syntax, or strings, start with `rg`.
3. If using `codegraph_context`, prefer short symbol-heavy queries over long natural language.
4. If `codegraph` returns irrelevant frontend/backend noise, fall back to `rg` to ground the search.
5. After `rg` reveals the likely symbol/file, switch back to `codegraph` for callers/callees/impact.

## Query shaping for codegraph

Good:
- `SubagentManager _announce_result publish_inbound session_key_override`
- `build_messages build_system_prompt get_history AgentLoop _process_message`
- `AuthService login session`

Bad:
- `how does the agent basically do prompts and tool stuff`
- `where is the code that maybe handles reinjection somehow`

## Benchmark summary

Benchmark run:
- project: `nanobot`
- focus: accuracy, not latency

| Task type | Better tool | Result |
|---|---|---|
| Exact symbol lookup like `SubagentManager`, `build_messages` | `codegraph` | More precise |
| Callers / callees / impact | `codegraph` | Clearly better |
| Vague task like `pending follow-up injection mid-turn queue` | `rg` | `codegraph_context` drifted |
| Prompt assembly question phrased in natural language | `rg` | Better grounding |
| Subagent tool access inventory | `rg` | Better for literal registration lines |

Practical conclusion:
- `codegraph` is better for semantic navigation
- `rg` is better for fuzzy text hunting
- best working style is `codegraph-first`, not `codegraph-only`

## Guardrails

- Do not use `rg` first for caller/callee/impact questions when `codegraph` is available.
- Do not trust `codegraph_context` blindly on long natural-language prompts.
- Do not keep pushing one tool after it already showed drift.
- If the repo is not indexed, either initialize `codegraph` or fall back cleanly to `rg`.
