const BASE = '/api'

async function fetchJSON(path) {
  const res = await fetch(`${BASE}${path}`)
  if (!res.ok) {
    throw new Error(`API ${path} returned ${res.status}`)
  }
  return res.json()
}

export function fetchSummary({ window, skill, success_state, task_type }) {
  const params = new URLSearchParams({ window })
  if (skill) params.set('skill', skill)
  if (success_state) params.set('success_state', success_state)
  if (task_type) params.set('task_type', task_type)
  return fetchJSON(`/summary?${params}`)
}
