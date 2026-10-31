export interface StudyNote {
  title: string
  summary: string
  key_concepts: string[]
  questions: string[]
}

const API_URL = 'http://127.0.0.1:8000/api'

export async function generateNote(material: string): Promise<StudyNote> {
  const response = await fetch(`${API_URL}/notes/generate/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ material }),
  })

  if (!response.ok) {
    throw new Error('Failed to generate study notes.')
  }

  return await response.json()
}

export async function generateNoteFromFile(file: File): Promise<StudyNote> {
  const formData = new FormData()
  formData.append('file', file)

  const response = await fetch(`${API_URL}/notes/generate-from-file/`, {
    method: 'POST',
    body: formData,
  })

  if (!response.ok) {
    throw new Error('Failed to generate notes from file.')
  }

  return await response.json()
}
