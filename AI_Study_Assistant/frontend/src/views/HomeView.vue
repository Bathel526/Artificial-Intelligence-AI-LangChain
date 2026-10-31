

<script setup lang="ts">
import { ref } from 'vue'
import { generateNote, generateNoteFromFile } from '../services/api'
import type { StudyNote } from '../services/api'
import { jsPDF } from 'jspdf'
import dejavusansUrl from '../assets/fonts/DejaVuSans.ttf?url'
import StudyNoteDisplay from '../components/StudyNoteDisplay.vue'
import FileUpload from '../components/FileUpload.vue'
import GenerateButton from '../components/GenerateButton.vue'
import ErrorMessage from '../components/ErrorMessage.vue'
import ResetButton from '../components/ResetButton.vue'

const material = ref('')
const selectedFile = ref<File | null>(null)
const generatedNote = ref<StudyNote | null>(null)

const isLoading = ref(false)
const errorMessage = ref('')

async function loadFontAsBase64(): Promise<string> {
  const response = await fetch(dejavusansUrl)

  if (!response.ok) {
    throw new Error('Could not load PDF font.')
  }

  const fontBuffer = await response.arrayBuffer()
  const bytes = new Uint8Array(fontBuffer)

  let binary = ''

  for (let i = 0; i < bytes.length; i++) {
    binary += String.fromCharCode(bytes[i]!)
  }

  return btoa(binary)
}

async function handleGenerateNote() {
  errorMessage.value = ''
  generatedNote.value = null

  const hasText = material.value.trim().length > 0
  const hasFile = selectedFile.value !== null

  if (!hasText && !hasFile) {
    errorMessage.value = 'Please enter study material or select a file.'
    return
  }

  if (hasText && hasFile) {
    errorMessage.value = 'Please use either text or a file, not both.'
    return
  }

  isLoading.value = true

  try {
    if (hasFile) {
      generatedNote.value = await generateNoteFromFile(selectedFile.value!)
    } else {
      generatedNote.value = await generateNote(material.value.trim())
    }
  } catch (error) {
    errorMessage.value = 'Something went wrong while generating your study notes.'
    console.error(error)
  } finally {
    isLoading.value = false
  }
}

function resetForm() {
  material.value = ''
  selectedFile.value = null
  generatedNote.value = null
  errorMessage.value = ''
}

function handleDownloadNote() {
  if (!generatedNote.value) return

  const note = generatedNote.value

  const noteContent = `
${note.title}

SUMMARY
${note.summary}

KEY CONCEPTS
${note.key_concepts.map((concept, index) => `${index + 1}. ${concept}`).join('\n')}

QUESTIONS
${note.questions.map((question, index) => `${index + 1}. ${question}`).join('\n')}
  `.trim()

  const blob = new Blob(
    ['\uFEFF', noteContent],
    { type: 'text/plain;charset=utf-8' }
  )

  const url = URL.createObjectURL(blob)
  const link = document.createElement('a')

  const filename = note.title
    .replace(/[<>:"/\\|?*]/g, '-')
    .trim() || 'study-note'

  link.href = url
  link.download = `${filename}.txt`

  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)

  URL.revokeObjectURL(url)
}

async function handleDownloadPDF() {
  if (!generatedNote.value) return

  try {
    const note = generatedNote.value

    const fontBase64 = await loadFontAsBase64()

    const pdf = new jsPDF({
      orientation: 'portrait',
      unit: 'mm',
      format: 'a4',
    })

    // Register custom font
    pdf.addFileToVFS('DejaVuSans.ttf', fontBase64)
    pdf.addFont('DejaVuSans.ttf', 'DejaVuSans', 'normal')
    pdf.setFont('DejaVuSans', 'normal')

    const pageWidth = pdf.internal.pageSize.getWidth()
    const pageHeight = pdf.internal.pageSize.getHeight()

    const margin = 20
    const contentWidth = pageWidth - margin * 2

    let y = 25

    function checkPageSpace(requiredSpace: number) {
      if (y + requiredSpace > pageHeight - margin) {
        pdf.addPage()
        y = 25
      }
    }

    function addSection(title: string, content: string[]) {
      checkPageSpace(18)

      pdf.setFontSize(15)
      pdf.setTextColor(37, 99, 235)
      pdf.text(title, margin, y)

      y += 9

      pdf.setFontSize(10)
      pdf.setTextColor(71, 85, 105)

      for (const item of content) {
        const lines = pdf.splitTextToSize(item, contentWidth)

        for (const line of lines) {
          checkPageSpace(6)

          pdf.text(line, margin, y)
          y += 6
        }

        y += 3
      }

      y += 8
    }

    // Document title
    pdf.setFontSize(22)
    pdf.setTextColor(23, 37, 84)

    const titleLines = pdf.splitTextToSize(
      note.title,
      contentWidth,
    )

    for (const line of titleLines) {
      checkPageSpace(12)
      pdf.text(line, margin, y)
      y += 11
    }

    y += 8

    // Summary
    addSection('Summary', [note.summary])

    // Key concepts
    addSection(
      'Key concepts',
      note.key_concepts.map(
        (concept, index) => `${index + 1}. ${concept}`,
      ),
    )

    // Questions
    addSection(
      'Questions',
      note.questions.map(
        (question, index) => `${index + 1}. ${question}`,
      ),
    )

    const filename =
      note.title.replace(/[<>:"/\\|?*]/g, '-').trim() ||
      'study-note'

    pdf.save(`${filename}.pdf`)
  } catch (error) {
    console.error('PDF generation failed:', error)
    errorMessage.value = 'Could not generate PDF. Please try again.'
  }
}

</script>


<template>
  <main class="home">
    <h1>AI Study Assistant</h1>

    <p class="subtitle">
      Your personal AI-powered learning companion.
    </p>

    <section class="note-form">
      <h2>Create your study notes</h2>

      <textarea
        v-model="material"
        placeholder="Paste your study material here..."
      ></textarea>

      <FileUpload
        :selected-file="selectedFile"
        @file-selected="selectedFile = $event"
      />

      <GenerateButton
        :is-loading="isLoading"
        :disabled="isLoading"
        @click="handleGenerateNote"
      />

    </section>


    <ErrorMessage :message="errorMessage" />

    <StudyNoteDisplay
       v-if="generatedNote"
      :note="generatedNote"
    />
    <div v-if="generatedNote" class="note-actions">
      <button class="download-button" @click="handleDownloadNote">
        <font-awesome-icon icon="download" />
        Download as TXT
      </button>
      <button class="pdf-button" @click="handleDownloadPDF">
        <font-awesome-icon icon="file-pdf" />
        <span>Download as PDF</span>
      </button>

      <ResetButton @click="resetForm" />
    </div>
  </main>
</template>

<style scoped>
.home {
  width: 100%;
  max-width: 1000px;
  margin: 0 auto;
  padding: 60px 24px;
}

h1 {
  font-size: 36px;
  color: var(--color-text);
}

.subtitle {
  color: var(--color-text-muted);
  margin-bottom: 40px;
  font-size: 16px;
}

.note-form {
  padding: 32px;
  background-color: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-xl);
  box-shadow: var(--shadow-md);
  max-width: 850px;
  margin: 0 auto;
}

.note-form h2 {
  margin-top: 0;
  color: var(--color-text);
}

textarea {
  width: 100%;
  min-height: 200px;
  padding: 16px;
  resize: vertical;
  font: inherit;
  color: var(--color-text);
  background-color: var(--color-surface-secondary);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
}

textarea:focus {
  outline: 2px solid var(--color-primary-light);
  border-color: var(--color-primary);
}

@media (max-width: 768px) {
  .home {
    padding: 40px 20px;
  }

  h1 {
    font-size: 30px;
  }

  .subtitle {
    margin-bottom: 30px;
  }

  .note-form {
    padding: 24px;
  }
}

@media (max-width: 480px) {
  .home {
    padding: 28px 16px;
  }

  h1 {
    font-size: 26px;
  }

  .subtitle {
    font-size: 14px;
    margin-bottom: 24px;
  }

  .note-form {
    padding: 18px;
  }

  textarea {
    min-height: 160px;
    padding: 12px;
  }
}

.note-actions {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 14px;
  margin-top: 20px;
  flex-wrap: wrap;
}

.download-button {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 9px;

  padding: 12px 22px;

  color: white;
  background-color: var(--color-primary);
  border: 1px solid var(--color-primary);
  border-radius: var(--radius-md);

  font-size: 14px;
  font-weight: 600;

  transition: all 0.2s ease;
}

.download-button:hover {
  background-color: var(--color-primary-dark);
  transform: translateY(-1px);
  box-shadow: var(--shadow-sm);
}

.pdf-button {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 9px;

  padding: 12px 22px;

  color: white;
  background-color: #dc2626;
  border: 1px solid #dc2626;
  border-radius: var(--radius-md);

  font-size: 14px;
  font-weight: 600;

  transition: all 0.2s ease;
}

.pdf-button:hover {
  background-color: #b91c1c;
  border-color: #b91c1c;
  transform: translateY(-1px);
  box-shadow: var(--shadow-sm);
}

</style>
