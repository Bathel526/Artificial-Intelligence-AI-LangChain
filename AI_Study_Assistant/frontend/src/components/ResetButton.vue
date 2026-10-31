
<script setup lang="ts">
</script>

<template>
  <button class="reset-button">
    <font-awesome-icon icon="rotate-right" />
    <span>Create another note</span>
  </button>
</template>

<style scoped>
.reset-button {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 9px;

  margin: 0;
  padding: 12px 22px;

  color: var(--color-text-secondary);
  background-color: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);

  font-size: 14px;
  font-weight: 600;

  transition: all 0.2s ease;
}

.reset-button:hover {
  color: var(--color-primary);
  background-color: var(--color-primary-light);
  border-color: var(--color-primary);
  transform: translateY(-1px);
  box-shadow: var(--shadow-sm);
}

.reset-button:active {
  transform: translateY(0);
}
</style>
