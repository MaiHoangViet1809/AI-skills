<template>
  <div class="runs-table-wrap">
    <div class="table-header">
      <h3 class="section-title">Runs</h3>
      <span class="runs-count">{{ total }} total</span>
    </div>

    <div v-if="error" class="table-message table-message--error">{{ error }}</div>
    <div v-else-if="loading" class="table-message">Loading…</div>
    <div v-else-if="!rows.length" class="table-message">No runs in this window.</div>

    <div v-else class="table-scroll">
      <table class="table">
        <thead>
          <tr>
            <th>Started</th>
            <th>Skill</th>
            <th>Type</th>
            <th>State</th>
            <th>Duration</th>
            <th>Codex tok</th>
            <th>Claude tok</th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="row in rows"
            :key="row.run_id"
            class="table-row"
            :class="{ 'table-row--selected': row.run_id === selectedRunId }"
            @click="selectRun(row.run_id)"
          >
            <td class="cell-mono">{{ fmtTime(row.started_at) }}</td>
            <td>{{ row.skill || '—' }}</td>
            <td>{{ row.task_type || '—' }}</td>
            <td>
              <span class="badge" :class="`badge--${row.success_state}`">
                {{ row.success_state || '—' }}
              </span>
            </td>
            <td class="cell-mono">{{ fmtMs(row.run_duration_ms) }}</td>
            <td class="cell-mono">{{ fmtNum(row.codex_task_tokens) }}</td>
            <td class="cell-mono">{{ fmtNum(row.claude_total_tokens) }}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <div v-if="total > pageSize" class="pagination">
      <button class="page-btn" :disabled="offset === 0" @click="prev">← Prev</button>
      <span class="page-info">
        {{ offset + 1 }}–{{ Math.min(offset + pageSize, total) }} of {{ total }}
      </span>
      <button class="page-btn" :disabled="offset + pageSize >= total" @click="next">Next →</button>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import { fetchRuns } from '../api/index.js'
import { useFilters } from '../composables/useFilters.js'
import { useSelectedRun } from '../composables/useSelectedRun.js'

const { filters } = useFilters()
const { selectedRunId, selectRun } = useSelectedRun()

const rows = ref([])
const total = ref(0)
const loading = ref(true)
const error = ref(null)
const offset = ref(0)
const pageSize = 50

async function load() {
  loading.value = true
  error.value = null
  try {
    const res = await fetchRuns(filters, { limit: pageSize, offset: offset.value })
    rows.value = res.runs
    total.value = res.total
  } catch (e) {
    error.value = e.message
  } finally {
    loading.value = false
  }
}

watch(filters, () => { offset.value = 0; load() }, { immediate: true, deep: true })

function prev() { offset.value = Math.max(0, offset.value - pageSize); load() }
function next() { offset.value = offset.value + pageSize; load() }

function fmtTime(v) {
  if (!v) return '—'
  return v.slice(0, 16).replace('T', ' ')
}

function fmtMs(v) {
  if (v == null) return '—'
  if (v >= 60_000) return `${(v / 60_000).toFixed(1)}m`
  if (v >= 1_000) return `${(v / 1_000).toFixed(1)}s`
  return `${Math.round(v)}ms`
}

function fmtNum(v) {
  if (v == null) return '—'
  if (v >= 1_000_000) return `${(v / 1_000_000).toFixed(1)}M`
  if (v >= 1_000) return `${(v / 1_000).toFixed(1)}k`
  return String(v)
}
</script>

<style scoped>
.runs-table-wrap {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 6px;
  overflow: hidden;
}

.table-header {
  display: flex;
  align-items: baseline;
  gap: 0.75rem;
  padding: 0.75rem 1rem;
  border-bottom: 1px solid var(--border);
}

.section-title {
  font-size: 0.7rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--text-muted);
}

.runs-count {
  font-size: 0.75rem;
  color: var(--text-muted);
}

.table-message {
  padding: 1.5rem 1rem;
  font-size: 0.85rem;
  color: var(--text-muted);
  text-align: center;
}

.table-message--error {
  color: var(--danger);
}

.table-scroll {
  overflow-x: auto;
}

.table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.8rem;
}

.table th {
  padding: 0.5rem 0.75rem;
  text-align: left;
  font-size: 0.7rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.04em;
  color: var(--text-muted);
  background: var(--surface-alt);
  border-bottom: 1px solid var(--border);
  white-space: nowrap;
}

.table-row {
  cursor: pointer;
  border-bottom: 1px solid var(--border);
  transition: background 0.1s;
}

.table-row:last-child {
  border-bottom: none;
}

.table-row:hover {
  background: var(--surface-alt);
}

.table-row--selected {
  background: color-mix(in srgb, var(--accent) 15%, transparent);
}

.table-row td {
  padding: 0.45rem 0.75rem;
  color: var(--text);
  white-space: nowrap;
}

.cell-mono {
  font-family: 'SF Mono', 'Fira Code', 'Fira Mono', monospace;
  font-size: 0.75rem;
}

.badge {
  display: inline-block;
  padding: 0.15rem 0.4rem;
  border-radius: 3px;
  font-size: 0.7rem;
  font-weight: 600;
  background: var(--surface-alt);
  color: var(--text-muted);
}

.badge--accepted {
  background: color-mix(in srgb, #2ea043 20%, transparent);
  color: #3fb950;
}

.badge--failed {
  background: color-mix(in srgb, #da3633 20%, transparent);
  color: #f85149;
}

.badge--partial {
  background: color-mix(in srgb, #d29922 20%, transparent);
  color: #e3b341;
}

.pagination {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.5rem 0.75rem;
  border-top: 1px solid var(--border);
}

.page-btn {
  padding: 0.25rem 0.6rem;
  font-size: 0.75rem;
  border: 1px solid var(--border);
  border-radius: 4px;
  background: transparent;
  color: var(--text);
  cursor: pointer;
  transition: background 0.1s;
}

.page-btn:hover:not(:disabled) {
  background: var(--surface-alt);
}

.page-btn:disabled {
  opacity: 0.35;
  cursor: default;
}

.page-info {
  font-size: 0.75rem;
  color: var(--text-muted);
}
</style>
