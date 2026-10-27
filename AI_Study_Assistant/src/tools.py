from src.config import model
from langchain.tools import tool
import ast
import operator


from src.schemas import StudyNote, AnswerEvaluation


@tool
def count_words(text: str) -> int:
    """Policz liczbę słów w podanym tekście."""
    print("TOOL count_words został wywołany")
    return len(text.split())


@tool
def calculate(expression: str) -> float:
    """Oblicz proste działanie matematyczne, np. 12 * (4 + 3)."""
    print("TOOL calculate został wywołany")

    allowed_operators = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Pow: operator.pow,
        ast.USub: operator.neg,
        ast.UAdd: operator.pos,
    }

    def evaluate(node):
        if isinstance(node, ast.Constant) and type(node.value) in (int, float):
            return node.value

        if isinstance(node, ast.BinOp) and type(node.op) in allowed_operators:
            left = evaluate(node.left)
            right = evaluate(node.right)

            if isinstance(node.op, ast.Pow) and abs(right) > 100:
                raise ValueError("Wykładnik jest za duży.")

            return allowed_operators[type(node.op)](left, right)

        if isinstance(node, ast.UnaryOp) and type(node.op) in allowed_operators:
            return allowed_operators[type(node.op)](evaluate(node.operand))

        raise ValueError("Niedozwolone działanie matematyczne.")

    tree = ast.parse(expression, mode="eval")
    result = evaluate(tree.body)

    if isinstance(result, (int, float)) and abs(result) > 1e100:
        raise ValueError("Wynik jest za duży.")

    return result

@tool
def create_study_note(material: str) -> dict:
    """Utwórz notatkę do nauki na podstawie materiału.
    Zwróć tytuł, podsumowanie, kluczowe pojęcia i pytania sprawdzające."""
    print("TOOL create_study_note został wywołany")

    structured_model = model.with_structured_output(StudyNote)

    note = structured_model.invoke(
        "Utwórz krótką notatkę do nauki na podstawie podanego materiału. "
        "Cała notatka musi być napisana w tym samym języku co materiał źródłowy. "
        "Jeśli materiał jest po polsku, tytuł, podsumowanie, wszystkie kluczowe "
        "pojęcia i wszystkie pytania muszą być po polsku. "
        "Nie tłumacz terminów technicznych, jeśli naturalnie używa się ich "
        "w języku źródłowym. Nie dodawaj informacji, których nie ma w materiale. "
        "Zwróć wszystkie wymagane pola zgodnie ze schematem.\n\n"
        f"MATERIAŁ:\n{material}"
    )

    return note.model_dump()


@tool
def evaluate_answer(
    material: str,
    question: str,
    user_answer: str,
) -> dict:
    """Oceń odpowiedź ucznia na pytanie na podstawie materiału źródłowego.
    Zwróć ocenę, informację zwrotną i poprawną odpowiedź."""

    print("TOOL evaluate_answer został wywołany")

    evaluation_model = model.with_structured_output(AnswerEvaluation)

    result = evaluation_model.invoke(
        "Oceń odpowiedź ucznia WYŁĄCZNIE na podstawie materiału źródłowego. "
        "Zwróć wszystkie pola wymagane przez schemat AnswerEvaluation. "
        "Nie dodawaj żadnych innych pól. "
        "Pole status musi mieć dokładnie jedną wartość: "
        "'correct', 'partially_correct' albo 'incorrect'. "
        "Pole feedback ma zawierać maksymalnie 2 krótkie zdania. "
        "Pole correct_answer ma zawierać krótką poprawną odpowiedź "
        "na zadane pytanie, a nie ocenę odpowiedzi ucznia. "
        "Nie powtarzaj uzasadnienia. "
        "Jeśli odpowiedź jest poprawna merytorycznie, ale sformułowana "
        "innymi słowami, zaakceptuj ją. "
        "Jeśli odpowiedź zawiera tylko część wymaganych informacji, "
        "wybierz 'partially_correct'. "
        "Jeśli odpowiedź nie odpowiada na pytanie lub zawiera "
        "nieuzasadnione informacje, wybierz 'incorrect'.\n\n"
        f"MATERIAŁ:\n{material}\n\n"
        f"PYTANIE:\n{question}\n\n"
        f"ODPOWIEDŹ UCZNIA:\n{user_answer}"
    )
    return result.model_dump()

