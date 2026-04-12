<template>
  <div class="chart-wrap">
    <h3 class="chart-title">Activity</h3>
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
import { fetchActivityChart } from '../api/index.js'
import { useFilters } from '../composables/useFilters.js'

Chart.register(...registerables)

const { filters } = useFilters()

const canvasRef = ref(null)
const loading = ref(true)
const error = ref(null)
const empty = ref(false)

let chart = null

function fmtBucket(iso) {
  try {
    const d = new Date(iso)
    const mo = String(d.getUTCMonth() + 1).padStart(2, '0')
    const da = String(d.getUTCDate()).padStart(2, '0')
    const hr = String(d.getUTCHours()).padStart(2, '0')
    const mi = String(d.getUTCMinutes()).padStart(2, '0')
    return `${mo}-${da} ${hr}:${mi}`
  } catch {
    return iso
  }
}

function destroyChart() {
  if (chart) { chart.destroy(); chart = null }
}

function buildChart(buckets) {
  destroyChart()
  if (!canvasRef.value || !buckets.length) return

  chart = new Chart(canvasRef.value, {
    type: 'bar',
    data: {
      labels: buckets.map(b => fmtBucket(b.bucket)),
      datasets: [
        {
          label: 'Accepted',
          data: buckets.map(b => b.accepted),
          backgroundColor: '#2ea043',
          stack: 's',
        },
        {
          label: 'Failed',
          data: buckets.map(b => b.failed),
          backgroundColor: '#da3633',
          stack: 's',
        },
        {
          label: 'Other',
          data: buckets.map(b => b.total - b.accepted - b.failed),
          backgroundColor: '#8b949e',
          stack: 's',
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { labels: { color: '#e6edf3', boxWidth: 12, font: { size: 11 } } },
      },
      scales: {
        x: {
          stacked: true,
          ticks: { color: '#8b949e', maxRotation: 45, font: { size: 10 } },
          grid: { color: '#21262d' },
        },
        y: {
          stacked: true,
          beginAtZero: true,
          ticks: { color: '#8b949e', precision: 0 },
          grid: { color: '#21262d' },
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
    const res = await fetchActivityChart(filters)
    empty.value = res.buckets.length === 0
    await nextTick()
    buildChart(res.buckets)
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
