<template>
  <transition name="drawer">
    <div v-if="selectedRunId" class="drawer-backdrop" @click.self="clearRun">
      <aside class="drawer">
        <div class="drawer-header">
          <h2 class="drawer-title">Run Detail</h2>
          <button class="drawer-close" @click="clearRun" aria-label="Close">✕</button>
        </div>

        <div v-if="loading" class="drawer-status">Loading…</div>
        <div v-else-if="error" class="drawer-status drawer-status--error">{{ error }}</div>
        <div v-else-if="run" class="drawer-body">
          <section v-for="section in SECTIONS" :key="section.title" class="detail-section">
            <h3 class="detail-section-title">{{ section.title }}</h3>
            <dl class="detail-list">
              <template v-for="field in section.fields" :key="field.key">
                <dt>{{ field.label }}</dt>
                <dd :class="{ 'dd--mono': field.mono }">{{ fmt(run[field.key], field.type) }}</dd>
              </template>
            </dl>
          </section>
        </div>
      </aside>
    </div>
  </transition>
</template>

<script setup>
import { ref, watch } from 'vue'
import { fetchRunDetail } from '../api/index.js'
import { useSelectedRun } from '../composables/useSelectedRun.js'

const { selectedRunId, clearRun } = useSelectedRun()

const run = ref(null)
const loading = ref(false)
const error = ref(null)

const SECTIONS = [
  {
    title: 'Identity',
    fields: [
      { key: 'run_id',     label: 'Run ID',    type: 'str', mono: true },
      { key: 'skill',      label: 'Skill',     type: 'str' },
      { key: 'plan',       label: 'Plan',      type: 'str', mono: true },
      { key: 'sow',        label: 'SOW',       type: 'str', mono: true },
      { key: 'task_type',  label: 'Task type', type: 'str' },
      { key: 'intent',     label: 'Intent',    type: 'str' },
    ],
  },
  {
    title: 'Timing',
    fields: [
      { key: 'started_at',                    label: 'Started',          type: 'time' },
      { key: 'finished_at',                   label: 'Finished',         type: 'time' },
      { key: 'run_duration_ms',               label: 'Duration',         type: 'ms' },
      { key: 'time_to_first_usable_result_ms', label: 'Time to first',  type: 'ms' },
    ],
  },
  {
    title: 'Codex Metrics',
    fields: [
      { key: 'codex_task_tokens',             label: 'Task tokens',      type: 'num', mono: true },
      { key: 'codex_cached_input_tokens',     label: 'Cached input',     type: 'num', mono: true },
      { key: 'codex_fresh_input_tokens',      label: 'Fresh input',      type: 'num', mono: true },
      { key: 'codex_output_tokens',           label: 'Output tokens',    type: 'num', mono: true },
      { key: 'codex_reasoning_output_tokens', label: 'Reasoning tokens', type: 'num', mono: true },
      { key: 'codex_turn_count',              label: 'Turns',            type: 'num', mono: true },
      { key: 'codex_tool_call_count',         label: 'Tool calls',       type: 'num', mono: true },
      { key: 'codex_tool_error_count',        label: 'Tool errors',      type: 'num', mono: true },
      { key: 'codex_mcp_call_count',          label: 'MCP calls',        type: 'num', mono: true },
    ],
  },
  {
    title: 'Claude Metrics',
    fields: [
      { key: 'claude_total_tokens',          label: 'Total tokens',    type: 'num', mono: true },
      { key: 'claude_input_tokens',          label: 'Input tokens',    type: 'num', mono: true },
      { key: 'claude_output_tokens',         label: 'Output tokens',   type: 'num', mono: true },
      { key: 'claude_cache_creation_tokens', label: 'Cache creation',  type: 'num', mono: true },
      { key: 'claude_cache_read_tokens',     label: 'Cache read',      type: 'num', mono: true },
      { key: 'claude_duration_ms',           label: 'Claude duration', type: 'ms' },
      { key: 'claude_tool_call_count',       label: 'Tool calls',      type: 'num', mono: true },
      { key: 'claude_tool_error_count',      label: 'Tool errors',     type: 'num', mono: true },
      { key: 'claude_mcp_call_count',        label: 'MCP calls',       type: 'num', mono: true },
    ],
  },
  {
    title: 'Outcome',
    fields: [
      { key: 'success_state',        label: 'State',            type: 'str' },
      { key: 'outcome',              label: 'Outcome',          type: 'str' },
      { key: 'files_changed_count',  label: 'Files changed',    type: 'num', mono: true },
      { key: 'repair_rounds',        label: 'Repair rounds',    type: 'num', mono: true },
      { key: 'fallback_flag',        label: 'Fallback',         type: 'bool' },
      { key: 'validation_pass',      label: 'Validation pass',  type: 'bool' },
      { key: 'scope_respected',      label: 'Scope respected',  type: 'bool' },
      { key: 'delegate_ratio',       label: 'Delegate ratio',   type: 'pct' },
      { key: 'codex_to_claude_ratio', label: 'Codex/Claude',   type: 'float', mono: true },
    ],
  },
]

function fmt(v, type) {
  if (v == null) return '—'
  if (type === 'ms') {
    if (v >= 60_000) return `${(v / 60_000).toFixed(1)}m`
    if (v >= 1_000) return `${(v / 1_000).toFixed(1)}s`
    return `${Math.round(v)}ms`
  }
  if (type === 'num') {
    if (v >= 1_000_000) return `${(v / 1_000_000).toFixed(2)}M`
    if (v >= 1_000) return `${(v / 1_000).toFixed(1)}k`
    return String(v)
  }
  if (type === 'pct') return `${(v * 100).toFixed(1)}%`
  if (type === 'float') return Number(v).toFixed(3)
  if (type === 'bool') return v ? 'yes' : 'no'
  if (type === 'time') return String(v).slice(0, 19).replace('T', ' ')
  return String(v)
}

watch(selectedRunId, async (id) => {
  if (!id) { run.value = null; return }
  loading.value = true
  error.value = null
  run.value = null
  try {
    run.value = await fetchRunDetail(id)
  } catch (e) {
    error.value = e.message
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.drawer-backdrop {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.45);
  z-index: 200;
  display: flex;
  justify-content: flex-end;
}

.drawer {
  width: min(480px, 100vw);
  height: 100vh;
  background: var(--surface);
  border-left: 1px solid var(--border);
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.drawer-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0.75rem 1rem;
  border-bottom: 1px solid var(--border);
  background: var(--surface-alt);
  flex-shrink: 0;
}

.drawer-title {
  font-size: 0.85rem;
  font-weight: 600;
  color: var(--text);
}

.drawer-close {
  background: none;
  border: none;
  color: var(--text-muted);
  font-size: 1rem;
  cursor: pointer;
  padding: 0.25rem 0.4rem;
  border-radius: 4px;
  line-height: 1;
  transition: color 0.1s, background 0.1s;
}

.drawer-close:hover {
  color: var(--text);
  background: var(--border);
}

.drawer-status {
  padding: 1.5rem 1rem;
  font-size: 0.85rem;
  color: var(--text-muted);
  text-align: center;
}

.drawer-status--error {
  color: var(--danger);
}

.drawer-body {
  flex: 1;
  overflow-y: auto;
  padding: 0.75rem 0;
}

.detail-section {
  padding: 0 1rem 0.75rem;
  border-bottom: 1px solid var(--border);
  margin-bottom: 0;
}

.detail-section:last-child {
  border-bottom: none;
}

.detail-section-title {
  font-size: 0.65rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  color: var(--text-muted);
  margin-bottom: 0.5rem;
  padding-top: 0.75rem;
}

.detail-list {
  display: grid;
  grid-template-columns: 10rem 1fr;
  gap: 0.2rem 0.5rem;
}

.detail-list dt {
  font-size: 0.75rem;
  color: var(--text-muted);
  padding: 0.15rem 0;
  align-self: baseline;
}

.detail-list dd {
  font-size: 0.78rem;
  color: var(--text);
  padding: 0.15rem 0;
  word-break: break-all;
  align-self: baseline;
}

.dd--mono {
  font-family: 'SF Mono', 'Fira Code', monospace;
  font-size: 0.72rem;
}

/* Slide transition */
.drawer-enter-active,
.drawer-leave-active {
  transition: opacity 0.2s ease;
}

.drawer-enter-active .drawer,
.drawer-leave-active .drawer {
  transition: transform 0.2s ease;
}

.drawer-enter-from,
.drawer-leave-to {
  opacity: 0;
}

.drawer-enter-from .drawer,
.drawer-leave-to .drawer {
  transform: translateX(100%);
}
</style>
