
<script setup lang="ts">
import type { StudyNote } from '../services/api'

defineProps<{
  note: StudyNote
}>()

</script>

<template>
  <section class="generated-note">
    <h2>{{ note.title }}</h2>

    <div class="note-section">
      <h3>Summary</h3>
      <p>{{ note.summary }}</p>
    </div>

    <div class="note-section">
      <h3>Key concepts</h3>
      <ul>
        <li v-for="(concept, index) in note.key_concepts" :key="index">
          {{ concept }}
        </li>
      </ul>
    </div>

    <div class="note-section">
      <h3>Questions</h3>
      <ul>
        <li v-for="(question, index) in note.questions" :key="index">
          {{ question }}
        </li>
      </ul>
    </div>
  </section>
</template>

<style scoped>
.generated-note {
  margin-top: 32px;
  padding: 32px;
  background-color: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-xl);
  box-shadow: var(--shadow-md);
}

.generated-note h2 {
  margin: 0;
  padding-bottom: 20px;
  color: var(--color-text);
  font-size: 26px;
  line-height: 1.3;
  border-bottom: 1px solid var(--color-border);
}

.note-section {
  margin-top: 28px;
}

.note-section h3 {
  margin: 0 0 12px;
  color: var(--color-primary);
  font-size: 18px;
}

.note-section p {
  margin: 0;
  color: var(--color-text-secondary);
  line-height: 1.8;
}

.note-section ul {
  margin: 0;
  padding-left: 22px;
}

.note-section li {
  margin-bottom: 10px;
  padding-left: 4px;
  color: var(--color-text-secondary);
  line-height: 1.6;
}

.note-section li:last-child {
  margin-bottom: 0;
}

</style>
