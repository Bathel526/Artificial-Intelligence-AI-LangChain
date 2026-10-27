from pydantic import BaseModel
from typing import Literal


class StudyNote(BaseModel):
    title: str
    summary: str
    key_concepts: list[str]
    questions: list[str]


class AnswerEvaluation(BaseModel):
    status: Literal["correct", "partially_correct", "incorrect"]
    feedback: str
    correct_answer: str