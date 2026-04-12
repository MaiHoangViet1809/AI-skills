# Output Filtering

Output filtering is mandatory by default for captured delegate output.

The goal is to reduce coordinator read context, not to change Claude's runtime environment.

## Default Rule

- Drop `system`-typed messages from captured output by default.
- Keep only the smallest useful subset for the current flow.
- Only keep `system` output when the flow or the user explicitly requires it.

## Json Mode

In `json` mode, keep the useful final result and any required top-level fields such as:

- `session_id`
- `result`
- `error`
- `is_error`
- `structured_output`

If the returned payload contains `message` entries with `type: "system"`, drop them from the captured version by default.

## Stream-Json Mode

In `stream-json` mode, keep only the events needed for the current debugging task.

Default keep-set:

- `assistant`
- `result`
- `rate_limit_event`

Default drop-set:

- `system`
- hook start events
- hook response events
- init noise such as tools, mcp server lists, slash commands, skills, and plugins

## Examples

Prefer filtered capture like:

```text
json mode:
- session_id
- is_error
- error
- result
- structured_output

stream-json mode:
- rate_limit_event
- assistant
- result
```

Avoid passing through raw capture like:

```text
- system init payloads
- hook_started lines
- hook_response lines
- full tool and plugin inventories

## Shell Examples

Filter `json` output down to the useful final fields:

```bash
claude -p --output-format json --json-schema '<schema-json>' "<prompt>" \
  | jq '{session_id, is_error, error, result, structured_output}'
```

Filter `stream-json` output down to the default keep-set:

```bash
claude -p --output-format stream-json --json-schema '<schema-json>' "<prompt>" \
  | jq -c 'select(.type == "assistant" or .type == "result" or .type == "rate_limit_event")'
```

If you only need the terminal result from `stream-json`:

```bash
claude -p --output-format stream-json --json-schema '<schema-json>' "<prompt>" \
  | jq -c 'select(.type == "result")'
```
```

## Exception Rule

Keep normally dropped output only when:

- the current debug flow explicitly needs it
- the user explicitly asks to see it
