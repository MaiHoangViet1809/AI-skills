import { ref } from 'vue'

// Module-level singleton — shared across all component instances
const selectedRunId = ref(null)

export function useSelectedRun() {
  return {
    selectedRunId,
    selectRun: (id) => { selectedRunId.value = id },
    clearRun: () => { selectedRunId.value = null },
  }
}
