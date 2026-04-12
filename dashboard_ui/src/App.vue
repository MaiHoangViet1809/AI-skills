<template>
  <div class="app">
    <header class="app-header">
      <h1 class="app-title">AISkills Telemetry</h1>
      <span class="app-subtitle">local dashboard</span>
    </header>

    <FilterBar />
    <SummaryCards />

    <main class="app-body">
      <p class="placeholder">Charts and run table will appear here (SOW_0025).</p>
    </main>
  </div>
</template>

<script setup>
import FilterBar from './components/FilterBar.vue'
import SummaryCards from './components/SummaryCards.vue'
</script>

<style>
/* Global design tokens */
:root {
  --bg: #0d1117;
  --surface: #161b22;
  --surface-alt: #21262d;
  --border: #30363d;
  --text: #e6edf3;
  --text-muted: #8b949e;
  --accent: #238636;
  --accent-hover: #2ea043;
  --danger: #da3633;
}

*, *::before, *::after {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Noto Sans', Helvetica, Arial, sans-serif;
  background: var(--bg);
  color: var(--text);
  min-height: 100vh;
  font-size: 14px;
}

input, select, button {
  font-family: inherit;
}
</style>

<style scoped>
.app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.app-header {
  display: flex;
  align-items: baseline;
  gap: 0.75rem;
  padding: 0.75rem 1rem;
  border-bottom: 1px solid var(--border);
  background: var(--surface);
}

.app-title {
  font-size: 1rem;
  font-weight: 600;
  color: var(--text);
}

.app-subtitle {
  font-size: 0.75rem;
  color: var(--text-muted);
}

.app-body {
  flex: 1;
  padding: 1.5rem 1rem;
}

.placeholder {
  color: var(--text-muted);
  font-size: 0.85rem;
  border: 1px dashed var(--border);
  border-radius: 6px;
  padding: 2rem;
  text-align: center;
}
</style>
