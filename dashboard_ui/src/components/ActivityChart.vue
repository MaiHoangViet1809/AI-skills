<template>
  <div class="chart-wrap">
    <div class="chart-head">
      <h3 class="chart-title">Token Activity</h3>
      <div class="mode-toggle">
        <button
          v-for="option in metricModes"
          :key="option"
          :class="['mode-btn', { active: mode === option }]"
          @click="mode = option"
        >
          {{ option }}
        </button>
      </div>
    </div>
    <div v-if="error" class="chart-error">{{ error }}</div>
    <div v-else class="heatmap-wrap">
      <span v-if="loading" class="chart-loading">Loading…</span>
      <span v-else-if="empty" class="chart-loading">No data in this window.</span>
      <div v-else class="heatmap-shell">
        <div class="month-row" :style="monthGridStyle">
          <span class="weekday-spacer"></span>
          <span
            v-for="label in monthLabels"
            :key="`${label.col}-${label.label}`"
            class="month-label"
            :style="{ gridColumn: `${label.col} / span ${label.span}` }"
          >
            {{ label.label }}
          </span>
        </div>

        <div class="heatmap-grid">
          <div class="weekday-col">
            <span v-for="label in weekdayLabels" :key="label.text" :style="{ gridRow: label.row }">
              {{ label.text }}
            </span>
          </div>

          <div class="weeks-grid" :style="weeksGridStyle">
            <template v-for="(week, weekIndex) in weeks" :key="weekIndex">
              <div
                v-for="cell in week"
                :key="cell.date"
                class="day-cell"
                :class="{ outside: cell.outside, empty: isEmptyCell(cell) }"
                :style="{ gridColumn: weekIndex + 1, gridRow: cell.weekday + 1, backgroundColor: cellColor(cell) }"
                :title="cellTooltip(cell)"
              ></div>
            </template>
          </div>
        </div>

        <div class="legend-row">
          <span>{{ legendLabel }}</span>
          <div class="legend-scale">
            <span
              v-for="level in [0, 1, 2, 3, 4]"
              :key="level"
              class="legend-cell"
              :style="{ backgroundColor: heatColor(level / 4) }"
            ></span>
          </div>
          <span>More</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, ref, onMounted, watch } from 'vue'
import { fetchActivityChart } from '../api/index.js'
import { useFilters } from '../composables/useFilters.js'

const { filters } = useFilters()

const loading = ref(true)
const error = ref(null)
const empty = ref(false)
const mode = ref('total')
const metricModes = ['total', 'codex', 'claude']
const response = ref({ days: [], max_total_tokens: 0, max_codex_tokens: 0, max_claude_tokens: 0 })
const weekdayLabels = [
  { text: 'Mon', row: 2 },
  { text: 'Wed', row: 4 },
  { text: 'Fri', row: 6 },
]

function startOfWeek(date) {
  const copy = new Date(Date.UTC(date.getUTCFullYear(), date.getUTCMonth(), date.getUTCDate()))
  const weekday = (copy.getUTCDay() + 6) % 7
  copy.setUTCDate(copy.getUTCDate() - weekday)
  return copy
}

function isoDate(date) {
  return date.toISOString().slice(0, 10)
}

function formatShortDate(value) {
  return new Date(`${value}T00:00:00Z`).toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric',
    timeZone: 'UTC',
  })
}

const weeks = computed(() => {
  const days = response.value.days ?? []
  if (!days.length) return []

  const byDate = new Map(days.map(day => [day.date, day]))
  const first = new Date(`${days[0].date}T00:00:00Z`)
  const last = new Date(`${days[days.length - 1].date}T00:00:00Z`)
  const gridStart = startOfWeek(first)
  const gridEnd = new Date(Date.UTC(last.getUTCFullYear(), last.getUTCMonth(), last.getUTCDate()))
  gridEnd.setUTCDate(gridEnd.getUTCDate() + (6 - ((gridEnd.getUTCDay() + 6) % 7)))

  const columns = []
  for (let cursor = new Date(gridStart); cursor <= gridEnd; cursor.setUTCDate(cursor.getUTCDate() + 7)) {
    const week = []
    for (let offset = 0; offset < 7; offset += 1) {
      const day = new Date(Date.UTC(cursor.getUTCFullYear(), cursor.getUTCMonth(), cursor.getUTCDate()))
      day.setUTCDate(day.getUTCDate() + offset)
      const key = isoDate(day)
      const source = byDate.get(key)
      week.push({
        date: key,
        weekday: offset,
        outside: !source,
        run_count: source?.run_count ?? 0,
        accepted_runs: source?.accepted_runs ?? 0,
        codex_tokens: source?.codex_tokens ?? 0,
        claude_tokens: source?.claude_tokens ?? 0,
        total_tokens: source?.total_tokens ?? 0,
      })
    }
    columns.push(week)
  }
  return columns
})

const monthLabels = computed(() => {
  const labels = []
  let previousMonth = null
  weeks.value.forEach((week, index) => {
    const firstInside = week.find(cell => !cell.outside)
    if (!firstInside) return
    const month = firstInside.date.slice(0, 7)
    if (month === previousMonth) return
    previousMonth = month
    labels.push({
      label: new Date(`${firstInside.date}T00:00:00Z`).toLocaleDateString('en-US', { month: 'short', timeZone: 'UTC' }),
      col: index + 2,
      span: 1,
    })
  })
  return labels
})

const monthGridStyle = computed(() => ({ gridTemplateColumns: `auto repeat(${weeks.value.length}, 12px)` }))
const weeksGridStyle = computed(() => ({ gridTemplateColumns: `repeat(${weeks.value.length}, 12px)` }))
const legendLabel = computed(() => `${mode.value} token burn`)

function metricValue(cell) {
  if (mode.value === 'codex') return cell.codex_tokens
  if (mode.value === 'claude') return cell.claude_tokens
  return cell.total_tokens
}

function maxMetricValue() {
  if (mode.value === 'codex') return response.value.max_codex_tokens || 0
  if (mode.value === 'claude') return response.value.max_claude_tokens || 0
  return response.value.max_total_tokens || 0
}

function heatColor(ratio) {
  if (ratio <= 0) return '#21262d'
  if (ratio < 0.25) return '#0e4429'
  if (ratio < 0.5) return '#006d32'
  if (ratio < 0.75) return '#26a641'
  return '#39d353'
}

function cellColor(cell) {
  if (cell.outside) return 'transparent'
  if (isEmptyCell(cell)) return 'transparent'
  const max = maxMetricValue()
  const value = metricValue(cell)
  return heatColor(max > 0 ? value / max : 0)
}

function cellTooltip(cell) {
  if (cell.outside) return ''
  if (isEmptyCell(cell)) {
    return `${formatShortDate(cell.date)}\nno runs`
  }
  return [
    formatShortDate(cell.date),
    `total: ${cell.total_tokens.toLocaleString()} tokens`,
    `codex: ${cell.codex_tokens.toLocaleString()} tokens`,
    `claude: ${cell.claude_tokens.toLocaleString()} tokens`,
    `runs: ${cell.run_count}`,
    `accepted: ${cell.accepted_runs}`,
  ].join('\n')
}

function isEmptyCell(cell) {
  return !cell.outside && cell.run_count === 0
}

async function load() {
  loading.value = true
  error.value = null
  empty.value = false
  try {
    const res = await fetchActivityChart(filters)
    response.value = res
    empty.value = res.days.length === 0
  } catch (e) {
    error.value = e.message
  } finally {
    loading.value = false
  }
}

onMounted(load)
watch(filters, load, { deep: true })
</script>

<style scoped>
.chart-wrap {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 6px;
  padding: 1rem;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.chart-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 0.75rem;
}

.chart-title {
  font-size: 0.7rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--text-muted);
}

.mode-toggle {
  display: flex;
  gap: 0.35rem;
}

.mode-btn {
  border: 1px solid var(--border);
  background: var(--surface-alt);
  color: var(--text-muted);
  border-radius: 999px;
  padding: 0.25rem 0.55rem;
  font-size: 0.72rem;
  cursor: pointer;
  text-transform: uppercase;
}

.mode-btn.active {
  background: var(--accent);
  border-color: var(--accent);
  color: #fff;
}

.heatmap-wrap {
  position: relative;
  min-height: 200px;
}

.chart-loading {
  position: absolute;
  inset: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--text-muted);
  font-size: 0.8rem;
}

.heatmap-shell {
  display: flex;
  flex-direction: column;
  gap: 0.7rem;
}

.month-row {
  display: grid;
  column-gap: 4px;
  align-items: end;
}

.weekday-spacer {
  width: 28px;
}

.month-label {
  font-size: 0.72rem;
  color: var(--text-muted);
}

.heatmap-grid {
  display: flex;
  gap: 6px;
}

.weekday-col {
  width: 28px;
  display: grid;
  grid-template-rows: repeat(7, 12px);
  row-gap: 4px;
  font-size: 0.68rem;
  color: var(--text-muted);
}

.weeks-grid {
  display: grid;
  grid-auto-flow: column;
  grid-template-rows: repeat(7, 12px);
  gap: 4px;
}

.day-cell {
  width: 12px;
  height: 12px;
  border-radius: 2px;
  background: #21262d;
  border: 1px solid rgba(255, 255, 255, 0.04);
}

.day-cell.outside {
  border-color: transparent;
}

.day-cell.empty {
  border-color: rgba(255, 255, 255, 0.02);
}

.legend-row {
  display: flex;
  justify-content: flex-end;
  align-items: center;
  gap: 0.45rem;
  color: var(--text-muted);
  font-size: 0.72rem;
}

.legend-scale {
  display: flex;
  gap: 0.2rem;
}

.legend-cell {
  width: 12px;
  height: 12px;
  border-radius: 2px;
}

.chart-error {
  color: var(--danger);
  font-size: 0.8rem;
  padding: 0.5rem 0;
}
</style>
