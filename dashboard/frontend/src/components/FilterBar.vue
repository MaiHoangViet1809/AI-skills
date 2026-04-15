<template>
  <div class="filter-bar">
    <div class="filter-group">
      <label class="filter-label">Window</label>
      <div class="window-buttons">
        <button
          v-for="w in windows"
          :key="w"
          :class="['window-btn', { active: filters.window === w }]"
          @click="setWindow(w)"
        >
          {{ w }}
        </button>
      </div>
    </div>

    <div class="filter-group">
      <label class="filter-label" for="filter-skill">Skill</label>
      <input
        id="filter-skill"
        class="filter-input"
        type="text"
        placeholder="any"
        :value="filters.skill ?? ''"
        @change="e => setSkill(e.target.value)"
      />
    </div>

    <div class="filter-group">
      <label class="filter-label" for="filter-state">State</label>
      <select
        id="filter-state"
        class="filter-input"
        :value="filters.success_state ?? ''"
        @change="e => setSuccessState(e.target.value)"
      >
        <option value="">any</option>
        <option value="accepted">accepted</option>
        <option value="repaired">repaired</option>
        <option value="fallback_local">fallback_local</option>
        <option value="stopped">stopped</option>
      </select>
    </div>

    <div class="filter-group">
      <label class="filter-label" for="filter-type">Task type</label>
      <input
        id="filter-type"
        class="filter-input"
        type="text"
        placeholder="any"
        :value="filters.task_type ?? ''"
        @change="e => setTaskType(e.target.value)"
      />
    </div>

    <button class="reset-btn" @click="reset">Reset</button>
  </div>
</template>

<script setup>
import { useFilters } from '../composables/useFilters.js'

const { filters, windows, setWindow, setSkill, setSuccessState, setTaskType, reset } = useFilters()
</script>

<style scoped>
.filter-bar {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  align-items: flex-end;
  padding: 0.75rem 1rem;
  background: var(--surface);
  border-bottom: 1px solid var(--border);
}

.filter-group {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.filter-label {
  font-size: 0.7rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--text-muted);
}

.window-buttons {
  display: flex;
  gap: 0.25rem;
}

.window-btn {
  padding: 0.25rem 0.5rem;
  font-size: 0.8rem;
  border: 1px solid var(--border);
  border-radius: 4px;
  background: transparent;
  color: var(--text);
  cursor: pointer;
  transition: background 0.15s, color 0.15s;
}

.window-btn:hover {
  background: var(--accent-hover);
}

.window-btn.active {
  background: var(--accent);
  color: #fff;
  border-color: var(--accent);
}

.filter-input {
  padding: 0.25rem 0.5rem;
  font-size: 0.85rem;
  border: 1px solid var(--border);
  border-radius: 4px;
  background: var(--surface-alt);
  color: var(--text);
  min-width: 7rem;
}

.reset-btn {
  padding: 0.3rem 0.75rem;
  font-size: 0.8rem;
  border: 1px solid var(--border);
  border-radius: 4px;
  background: transparent;
  color: var(--text-muted);
  cursor: pointer;
  align-self: flex-end;
  transition: color 0.15s;
}

.reset-btn:hover {
  color: var(--text);
}
</style>
