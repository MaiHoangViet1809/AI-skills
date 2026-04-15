<template>
  <div class="summary-cards">
    <div v-if="error" class="card card--error">
      <span class="card-label">Error</span>
      <span class="card-value">{{ error }}</span>
    </div>

    <template v-else>
      <div class="card">
        <span class="card-label">Total runs</span>
        <span class="card-value">{{ loading ? '…' : fmt(data.total_runs) }}</span>
      </div>

      <div class="card">
        <span class="card-label">Accepted</span>
        <span class="card-value">{{ loading ? '…' : fmt(data.accepted_runs) }}</span>
        <span class="card-sub">{{ loading ? '' : fmtPct(data.acceptance_rate) }}</span>
      </div>

      <div class="card">
        <span class="card-label">Codex tokens</span>
        <span class="card-value">{{ loading ? '…' : fmtNum(data.total_codex_task_tokens) }}</span>
      </div>

      <div class="card">
        <span class="card-label">Claude tokens</span>
        <span class="card-value">{{ loading ? '…' : fmtNum(data.total_claude_tokens) }}</span>
      </div>

      <div class="card">
        <span class="card-label">Avg duration</span>
        <span class="card-value">{{ loading ? '…' : fmtMs(data.avg_run_duration_ms) }}</span>
      </div>

      <div class="card">
        <span class="card-label">Tool calls</span>
        <span class="card-value">{{ loading ? '…' : fmt(data.total_tool_calls) }}</span>
        <span class="card-sub">{{ loading ? '' : `${fmt(data.fallback_count)} fallbacks` }}</span>
      </div>
    </template>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import { fetchSummary } from '../api/index.js'
import { useFilters } from '../composables/useFilters.js'

const { filters } = useFilters()

const data = ref({})
const loading = ref(true)
const error = ref(null)

async function load() {
  loading.value = true
  error.value = null
  try {
    data.value = await fetchSummary(filters)
  } catch (e) {
    error.value = e.message
  } finally {
    loading.value = false
  }
}

watch(filters, load, { immediate: true, deep: true })

function fmt(v) {
  return v == null ? '—' : String(v)
}

function fmtNum(v) {
  if (v == null) return '—'
  if (v >= 1_000_000) return `${(v / 1_000_000).toFixed(1)}M`
  if (v >= 1_000) return `${(v / 1_000).toFixed(1)}k`
  return String(v)
}

function fmtPct(v) {
  if (v == null) return ''
  return `${(v * 100).toFixed(0)}%`
}

function fmtMs(v) {
  if (v == null) return '—'
  if (v >= 60_000) return `${(v / 60_000).toFixed(1)}m`
  if (v >= 1_000) return `${(v / 1_000).toFixed(1)}s`
  return `${Math.round(v)}ms`
}
</script>

<style scoped>
.summary-cards {
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem;
  padding: 1rem;
}

.card {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
  padding: 0.75rem 1rem;
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 6px;
  min-width: 9rem;
  flex: 1 1 9rem;
}

.card--error {
  border-color: var(--danger);
  color: var(--danger);
}

.card-label {
  font-size: 0.7rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--text-muted);
}

.card-value {
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--text);
  line-height: 1.1;
}

.card-sub {
  font-size: 0.75rem;
  color: var(--text-muted);
}
</style>
