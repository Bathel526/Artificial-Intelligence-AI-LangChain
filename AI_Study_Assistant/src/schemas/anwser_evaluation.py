from pydantic import BaseModel, Field
from typing import Literal

class AnswerEvaluation(BaseModel):
    status: Literal[
        "correct",
        "partially_correct",
        "incorrect",
        "not_in_material"
    ] = Field(
        description=(
            "Ocena odpowiedzi ucznia. "
            "Wybierz jedną z czterech dozwolonych wartości."
        )
    )

    feedback: str = Field(
        description=(
            "Krótka informacja zwrotna dla ucznia. "
            "Maksymalnie 2 zdania."
        )
    )

    correct_answer: str = Field(
        description=(
            "Poprawna odpowiedź na pytanie, jeśli wynika z materiału. "
            "Jeśli pytania nie da się rozstrzygnąć na podstawie materiału, "
            "wyjaśnij to zamiast wymyślać odpowiedź."
        )
    )