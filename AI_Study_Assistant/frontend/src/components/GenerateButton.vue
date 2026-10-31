<script setup lang="ts">

defineProps<{
  isLoading: boolean
  disabled: boolean
}>()

</script>

<template>
  <button
    class = "generate-button"
    :disabled = "disabled || isLoading"
    >
    {{ isLoading ? 'Generating...' : 'Generate study notes' }}
  </button>
</template>

<style scoped>

.generate-button {
  width: 100%;
  margin-top: 20px;
  padding: 15px 24px;

  background-color: var(--color-primary);
  color: white;

  border: none;
  border-radius: var(--radius-md);

  font-size: 16px;
  font-weight: 600;

  box-shadow: var(--shadow-sm);

  transition:
    background-color 0.2s ease,
    transform 0.2s ease,
    box-shadow 0.2s ease;
}

.generate-button:hover:not(:disabled) {
  background-color: var(--color-primary-dark);
  box-shadow: var(--shadow-md);
  transform: translateY(-1px);
}

.generate-button:active:not(:disabled) {
  transform: translateY(0);
}

.generate-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  box-shadow: none;
}


</style>

