<script setup lang="ts">

defineProps<{
  selectedFile: File | null
}>()

const emit = defineEmits<{
  fileSelected: [file: File | null]
}>()

function handleFileUpload(event: Event) {
  const target = event.target as HTMLInputElement
  const file = target.files?.[0] ?? null

  emit('fileSelected', file)
}

</script>


<template>
  <div class="file-upload">
    <label for="file" class="upload-area">
      <span class="upload-icon">↑</span>

      <span class="upload-title">
        Choose a file to upload
      </span>

      <span class="upload-description">
        PDF, DOCX or TXT
      </span>

      <input
        id="file"
        type="file"
        accept=".pdf,.docx,.txt"
        @change="handleFileUpload"
      />
    </label>

    <p v-if="selectedFile" class="selected-file">
      Selected file: <strong>{{ selectedFile.name }}</strong>
    </p>
  </div>
</template>


<style scoped>

.file-upload {
  margin: 24px 0;
}

.upload-area {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;

  padding: 30px 20px;

  background-color: var(--color-surface-secondary);
  border: 2px dashed var(--color-border);
  border-radius: var(--radius-lg);

  cursor: pointer;

  transition:
    border-color 0.2s ease,
    background-color 0.2s ease;
}

.upload-area:hover {
  border-color: var(--color-primary);
  background-color: var(--color-primary-light);
}

.upload-icon {
  display: flex;
  align-items: center;
  justify-content: center;

  width: 44px;
  height: 44px;

  background-color: var(--color-primary-light);
  color: var(--color-primary);

  border-radius: 50%;
  font-size: 28px;
}

.upload-title {
  color: var(--color-text);
  font-weight: 600;
}

.upload-description {
  color: var(--color-text-muted);
  font-size: 13px;
}

.upload-area input {
  display: none;
}

.selected-file {
  margin-top: 14px;
  padding: 12px;
  background-color: var(--color-primary-light);
  border-radius: var(--radius-md);
  color: var(--color-text);
  font-size: 14px;
  overflow-wrap: anywhere;
}

</style>
