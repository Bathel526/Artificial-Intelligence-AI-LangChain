import json
from src.tools.evaluate_answer import evaluate_answer
from src.quiz.summary import show_quiz_summary

def run_quiz(material, questions):
    """Prowadzi quiz i zbiera oceny bezpośrednio w Pythonie."""
    results = []

    if not material or not questions:
        print("Brakuje materiału lub pytań do quizu.")
        return results

    print("\n===== ROZPOCZYNAMY QUIZ =====")
    print(f"Liczba pytań: {len(questions)}")

    for index, question in enumerate(questions, start=1):
        print(f"\nPytanie {index}/{len(questions)}:")
        print(question)

        user_answer = input("Twoja odpowiedź (lub 'koniec'): ").strip()

        if user_answer.lower() in ("koniec", "exit", "quit"):
            print("Kończymy quiz.")
            break

        if not user_answer:
            print("Pusta odpowiedź — pomijam pytanie.")
            continue

        try:
            evaluation = evaluate_answer.invoke({
                "material": material,
                "question": question,
                "user_answer": user_answer,
            })

            if isinstance(evaluation, str):
                evaluation = json.loads(evaluation)

            status = evaluation.get("status", "incorrect")
            feedback = evaluation.get("feedback", "")
            correct_answer = evaluation.get("correct_answer", "")

            if status not in (
                "correct",
                "partially_correct",
                "incorrect",
                "not_in_material",
            ):
                status = "incorrect"

            results.append({
                "question": question,
                "status": status,
                "feedback": feedback,
            })

            print("\nOcena:", {
                "correct": "Poprawna",
                "partially_correct": "Częściowo poprawna",
                "incorrect": "Niepoprawna",
                "not_in_material": "Brak informacji w materiale",
            }[status])

            if feedback:
                print("Informacja zwrotna:", feedback)

            if status != "correct" and correct_answer:
                print("Poprawna odpowiedź:", correct_answer)

        except Exception as error:
            print(f"Nie udało się ocenić odpowiedzi: {error}")
            print("To pytanie nie zostanie uwzględnione w wyniku.")

    show_quiz_summary(results)
    return results