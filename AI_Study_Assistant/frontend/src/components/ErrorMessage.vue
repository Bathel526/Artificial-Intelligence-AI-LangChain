<script setup lang="ts">

defineProps<{
  message: string
}>()
</script>

<template>
  <p v-if="message" class="error-message">
    {{ message }}
  </p>
</template>

<style scoped>
  .error-message {
  margin-top: 20px;
  padding: 14px 16px;

  color: var(--color-error);
  background-color: var(--color-error-background);
  border: 1px solid var(--color-error);
  border-radius: var(--radius-md);

  font-size: 14px;
  line-height: 1.5;
}
</style>
