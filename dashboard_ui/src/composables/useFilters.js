import { reactive, readonly } from 'vue'

const WINDOWS = ['1h', '6h', '12h', '24h', '2d', '7d', '30d', '90d', '365d', 'all']

const state = reactive({
  window: '12h',
  skill: null,
  success_state: null,
  task_type: null,
})

function setWindow(value) {
  if (WINDOWS.includes(value)) {
    state.window = value
  }
}

function setSkill(value) {
  state.skill = value || null
}

function setSuccessState(value) {
  state.success_state = value || null
}

function setTaskType(value) {
  state.task_type = value || null
}

function reset() {
  state.window = '12h'
  state.skill = null
  state.success_state = null
  state.task_type = null
}

export function useFilters() {
  return {
    filters: readonly(state),
    windows: WINDOWS,
    setWindow,
    setSkill,
    setSuccessState,
    setTaskType,
    reset,
  }
}
