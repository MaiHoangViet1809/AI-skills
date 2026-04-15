const BASE = '/api'

async function fetchJSON(path) {
  const res = await fetch(`${BASE}${path}`)
  if (!res.ok) {
    throw new Error(`API ${path} returned ${res.status}`)
  }
  return res.json()
}

function buildParams({ window, skill, success_state, task_type }) {
  const params = new URLSearchParams({ window })
  if (skill) params.set('skill', skill)
  if (success_state) params.set('success_state', success_state)
  if (task_type) params.set('task_type', task_type)
  return params
}

export function fetchSummary(filters) {
  return fetchJSON(`/summary?${buildParams(filters)}`)
}

export function fetchRuns(filters, { limit = 50, offset = 0 } = {}) {
  const params = buildParams(filters)
  params.set('limit', String(limit))
  params.set('offset', String(offset))
  return fetchJSON(`/runs?${params}`)
}

export function fetchRunDetail(runId) {
  return fetchJSON(`/runs/${encodeURIComponent(runId)}`)
}

export function fetchActivityChart(filters) {
  return fetchJSON(`/charts/activity?${buildParams(filters)}`)
}

export function fetchDurationChart(filters) {
  return fetchJSON(`/charts/duration?${buildParams(filters)}`)
}
