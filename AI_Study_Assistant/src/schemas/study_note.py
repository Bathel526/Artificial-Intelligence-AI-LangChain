from pydantic import BaseModel, Field


class StudyNote(BaseModel):
    title: str = Field(description="Krótki tytuł notatki.")
    summary: str = Field(description="Podsumowanie materiału źródłowego.")
    key_concepts: list[str] = Field(
        description="Lista najważniejszych pojęć z materiału."
    )
    questions: list[str] = Field(
        description="Pytania sprawdzające wiedzę z materiału."
    )