<template>
  <div class="chart-wrap">
    <h3 class="chart-title">Run Duration</h3>
    <div v-if="error" class="chart-error">{{ error }}</div>
    <div v-else class="chart-canvas-wrap">
      <span v-if="loading" class="chart-loading">Loading…</span>
      <span v-else-if="empty" class="chart-loading">No data in this window.</span>
      <canvas ref="canvasRef"></canvas>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch, nextTick } from 'vue'
import { Chart, registerables } from 'chart.js'
import { fetchDurationChart } from '../api/index.js'
import { useFilters } from '../composables/useFilters.js'

Chart.register(...registerables)

const STATE_COLORS = { accepted: '#2ea043', failed: '#da3633' }

function stateColor(state) {
  return STATE_COLORS[state] || '#8b949e'
}

const { filters } = useFilters()

const canvasRef = ref(null)
const loading = ref(true)
const error = ref(null)
const empty = ref(false)

let chart = null
// Store points for tooltip access (immutable reference replaced on each load)
let lastPoints = []

function destroyChart() {
  if (chart) { chart.destroy(); chart = null }
}

function buildChart(points) {
  destroyChart()
  lastPoints = points
  if (!canvasRef.value || !points.length) return

  const durations = points.map(p =>
    p.run_duration_ms != null ? Math.round(p.run_duration_ms / 1000) : null
  )

  chart = new Chart(canvasRef.value, {
    type: 'line',
    data: {
      labels: points.map((_, i) => i + 1),
      datasets: [{
        label: 'Duration (s)',
        data: durations,
        borderColor: '#388bfd',
        borderWidth: 1.5,
        pointBackgroundColor: points.map(p => stateColor(p.success_state)),
        pointRadius: 4,
        pointHoverRadius: 6,
        tension: 0.1,
        spanGaps: true,
      }],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false },
        tooltip: {
          callbacks: {
            title: (items) => {
              const p = lastPoints[items[0].dataIndex]
              if (!p) return ''
              const t = (p.started_at || '').slice(0, 16).replace('T', ' ')
              return `${p.skill || '—'}  @  ${t}`
            },
            label: (item) => {
              const p = lastPoints[item.dataIndex]
              const dur = item.raw != null ? `${item.raw}s` : '—'
              return `${dur}  ·  ${p?.success_state || '—'}`
            },
          },
        },
      },
      scales: {
        x: {
          ticks: { display: false },
          grid: { color: '#21262d' },
        },
        y: {
          beginAtZero: true,
          ticks: { color: '#8b949e' },
          grid: { color: '#21262d' },
          title: {
            display: true,
            text: 'seconds',
            color: '#8b949e',
            font: { size: 10 },
          },
        },
      },
    },
  })
}

async function load() {
  loading.value = true
  error.value = null
  empty.value = false
  try {
    const res = await fetchDurationChart(filters)
    empty.value = res.points.length === 0
    await nextTick()
    buildChart(res.points)
  } catch (e) {
    error.value = e.message
  } finally {
    loading.value = false
  }
}

onMounted(load)
watch(filters, load, { deep: true })
onUnmounted(destroyChart)
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

.chart-title {
  font-size: 0.7rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--text-muted);
}

.chart-canvas-wrap {
  position: relative;
  height: 200px;
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

.chart-error {
  color: var(--danger);
  font-size: 0.8rem;
  padding: 0.5rem 0;
}
</style>
