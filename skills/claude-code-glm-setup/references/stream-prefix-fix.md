# Stream Prefix Fix (codex-router)

Use this when the P3 probe shows GLM answers losing their opening words.
Change the colleague's own codex-router checkout only after they confirm.

## Symptom

Answers from a routed reasoning model start mid-sentence in Codex and Claude
Code, while the final `response.output_text.done` event still holds the full
text.

## Probe

Run with `node` from the codex-router checkout root (`probe.mjs` in a scratch
directory; it reads the router's own caller secret and prints no secret).

```js
import { readFileSync } from "node:fs";
import path from "node:path";
const root = process.cwd();
const { callerBaseUrl } = await import(path.join(root, "src/caller-auth.mjs"));
const { CALLER_SECRET_PATH, PORTS } = await import(path.join(root, "src/paths.mjs"));
const secret = readFileSync(CALLER_SECRET_PATH, "utf8").trim();
const res = await fetch(`${callerBaseUrl(PORTS.router, secret)}/responses`, {
  method: "POST",
  headers: { "content-type": "application/json", authorization: `Bearer ${secret}` },
  body: JSON.stringify({ model: "greennode/glm-5.3", stream: true,
    input: "Write exactly 3 short sentences. The first sentence must start with the word ALPHA. Last word: OMEGA." }),
});
let deltas = "", done = "";
for (const frame of (await res.text()).split("\n\n")) {
  const data = frame.split("\n").filter((l) => l.startsWith("data:")).map((l) => l.slice(5).trim()).join("");
  if (!data || data === "[DONE]") continue;
  const event = JSON.parse(data);
  if (event.type === "response.output_text.delta") deltas += event.delta;
  if (event.type === "response.output_text.done") done = event.text;
}
console.log(res.status, deltas === done ? "PASS" : "TRUNCATED", JSON.stringify(deltas.slice(0, 60)));
```

`PASS` (run it three times) means no fix is needed. `TRUNCATED` with deltas
that are a suffix of the final text confirms this defect.

## Root Cause

The provider closes its thinking with one Chat Completions chunk whose delta
carries both `reasoning_content` (or `reasoning`) and the first `content`.
The chat stream itself is intact; LiteLLM's Chat-to-Responses stream bridge
emits the reasoning part of that chunk and drops its content. Verified by
comparing the forwarder stream, LiteLLM's chat stream and its Responses
stream on 2026-10-10.

## Fix Design

Split such a chunk into a reasoning-only delta followed by a content delta
inside the API forwarder, before LiteLLM sees it. Same tokens, same order.

1. Add `src/sse-data-line-transform.mjs` and `src/chat-mixed-delta.mjs` below.
2. In `src/api-forwarder.mjs`, import `chatMixedDeltaTransform` and add it to
   the response transform list for chat streams only, next to the existing
   chat-stream transforms (for example `zaiCacheUsageTransform`):

   ```js
   // Chat streams only: a native Responses stream never reaches LiteLLM's bridge.
   responsesStream ? undefined : chatMixedDeltaTransform(upstreamContentType),
   ```

3. Keep the upstream `Content-Type` on transformed chat streams. The forwarder
   drops `content-type` from copied headers whenever a transform is present,
   so replace the JSON-replay-only header line with:

   ```js
   // Chat-shaped transforms keep the upstream body type; only the Responses
   // adapters above replace it.
   if (transform.length && !responsesStream && !responsesJson && upstreamContentType) {
     response.setHeader("Content-Type", upstreamContentType);
   }
   ```

4. Add a unit test covering: a mixed chunk splits into reasoning then content;
   a chunk boundary inside the JSON and CRLF framing; the `reasoning` field
   name with terminal `usage` (usage only on the content chunk,
   `finish_reason: null` on the reasoning chunk); content-only,
   reasoning-only and non-JSON lines pass through byte for byte; the factory
   returns nothing for non event-stream content types.
5. Follow the checkout's own rules (for upstream codex-router: a
   `changelog.d/` fragment), run the full test suite and compare failures
   with the parent commit, restart the router service, and rerun the probe.

Names and line positions may differ in newer upstream versions; keep the
design (split before LiteLLM, chat streams only, keep Content-Type), not the
exact text.

## Source

From a codex-router checkout (MIT License, Copyright (c) 2026 codex-router
contributors); keep that notice when copying these files.

`src/sse-data-line-transform.mjs`:

```js
import { Transform } from "node:stream";

const LINE_FEED = 0x0a;

// Line-buffered rewriter for Chat Completions SSE streams on their way to
// LiteLLM. Subclasses implement `rewrite(payload)` and return either
// `undefined` (forward the original bytes untouched) or an array of payloads,
// each emitted as its own `data:` event in order. Non-data lines, `[DONE]`, and
// unparseable data pass through byte-for-byte.
export class SseDataLineTransform extends Transform {
  #pending = Buffer.alloc(0);

  _transform(chunk, _encoding, callback) {
    this.#pending = this.#pending.length ? Buffer.concat([this.#pending, chunk]) : chunk;
    this.#consumeLines();
    callback();
  }

  _flush(callback) {
    this.#consumeLines(true);
    callback();
  }

  rewrite(_payload) {
    return undefined;
  }

  #consumeLines(flush = false) {
    while (true) {
      const index = this.#pending.indexOf(LINE_FEED);
      if (index === -1) break;
      const line = this.#pending.subarray(0, index + 1);
      this.#pending = this.#pending.subarray(index + 1);
      this.push(this.#rewriteLine(line));
    }
    if (flush && this.#pending.length) {
      this.push(this.#rewriteLine(this.#pending));
      this.#pending = Buffer.alloc(0);
    }
  }

  #rewriteLine(line) {
    const text = line.toString("utf8");
    const terminator = text.endsWith("\r\n") ? "\r\n" : text.endsWith("\n") ? "\n" : "";
    const content = terminator ? text.slice(0, -terminator.length) : text;
    if (!content.startsWith("data:")) return line;
    const data = content.slice(5).trim();
    if (!data || data === "[DONE]") return line;
    let payload;
    try {
      payload = JSON.parse(data);
    } catch {
      return line;
    }
    const payloads = this.rewrite(payload);
    if (payloads === undefined) return line;
    const separator = terminator || "\n";
    return Buffer.from(
      payloads.map((item) => `data: ${JSON.stringify(item)}`).join(`${separator}${separator}`) + terminator,
      "utf8",
    );
  }
}
```

`src/chat-mixed-delta.mjs`:

```js
import { SseDataLineTransform } from "./sse-data-line-transform.mjs";

// Some reasoning models (GreenNode GLM-5.3, verified 2026-10-10) close their
// thinking with one Chat Completions chunk whose delta carries both the tail of
// `reasoning_content` and the head of `content`. LiteLLM's Chat -> Responses
// stream bridge emits the reasoning part of that chunk and drops its content,
// so every answer loses its opening words while `output_text.done` still has
// the full text. Splitting the chunk into a reasoning-only delta followed by a
// content delta before it reaches LiteLLM carries the same tokens in the same
// order in a shape the bridge handles.
const REASONING_KEYS = ["reasoning_content", "reasoning"];

function present(value) {
  return value !== undefined && value !== null && value !== "";
}

function mixedChoice(choice) {
  const delta = choice?.delta;
  return Boolean(delta) && typeof delta === "object" && present(delta.content) &&
    REASONING_KEYS.some((key) => present(delta[key]));
}

export class ChatMixedDeltaSplitTransform extends SseDataLineTransform {
  rewrite(payload) {
    const choices = payload?.choices;
    if (!Array.isArray(choices) || choices.length !== 1 || !mixedChoice(choices[0])) return undefined;

    const [choice] = choices;
    const reasoningDelta = {};
    const contentDelta = {};
    for (const [key, value] of Object.entries(choice.delta)) {
      if (REASONING_KEYS.includes(key) || key === "role") reasoningDelta[key] = value;
      else contentDelta[key] = value;
    }
    const reasoningChunk = { ...payload, choices: [{ ...choice, delta: reasoningDelta, finish_reason: null }] };
    delete reasoningChunk.usage;
    return [reasoningChunk, { ...payload, choices: [{ ...choice, delta: contentDelta }] }];
  }
}

export function chatMixedDeltaTransform(contentType = "") {
  if (!String(contentType).toLowerCase().includes("text/event-stream")) return undefined;
  return new ChatMixedDeltaSplitTransform();
}
```
