
import json
from pathlib import Path

from langchain.agents import create_agent
from langgraph.checkpoint.sqlite import SqliteSaver

from src.config import model
from src.tools import (
    count_words,
    calculate,
    create_study_note,
    evaluate_answer,
)
from src.display import display_response


BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "study_assistant.db"


def show_quiz_summary(results):
    """Wyświetla podsumowanie na podstawie ocen zebranych w Pythonie."""
    total = len(results)

    print("\n===== PODSUMOWANIE QUIZU =====")

    if total == 0:
        print("Quiz nie zawiera ocenionych odpowiedzi.")
        return

    correct = sum(
        item["status"] == "correct"
        for item in results
    )
    percentage = round(correct / total * 100)

    print(f"Liczba ocenionych pytań: {total}")
    print(f"W pełni poprawne odpowiedzi: {correct}")
    print(f"Wynik: {percentage}%")

    needs_review = [
        item for item in results
        if item["status"] != "correct"
    ]

    if needs_review:
        print("\nDo powtórki:")
        for item in needs_review:
            print(f"- {item['question']}")
            print(f"  Ocena: {item['status']}")
    else:
        print("\nŚwietnie! Wszystkie odpowiedzi były poprawne.")


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


def main():
    print("\n=== AI Study Assistant ===")
    print("Zadaj pytanie lub poproś o wykonanie zadania.")
    print("Wpisz 'exit', aby zakończyć.\n")

    last_material = ""
    last_questions = []

    with SqliteSaver.from_conn_string(str(DB_PATH)) as checkpointer:
        agent = create_agent(
            model=model,
            tools=[
                count_words,
                calculate,
                create_study_note,
                evaluate_answer,
            ],
            system_prompt=(
                "Jesteś pomocnym asystentem do nauki. "
                "Odpowiadaj w języku użytkownika. "
                "Używaj count_words do liczenia słów, calculate "
                "do obliczeń, a create_study_note do tworzenia notatek. "
                "Nie twórz notatki, jeśli użytkownik o nią nie prosi."
            ),
            checkpointer=checkpointer,
        )

        config = {
            "configurable": {
                "thread_id": "study_session_1"
            }
        }

        while True:
            user_text = input("\nTy: ").strip()

            if user_text.lower() in ("exit", "quit", "koniec"):
                print("Do zobaczenia!")
                break

            if not user_text:
                continue

            previous_message_count = len(
                agent.get_state(config).values.get("messages", [])
            )

            response = agent.invoke(
                {"messages": [{"role": "user", "content": user_text}]},
                config=config,
            )

            new_messages = response["messages"][previous_message_count:]
            display_response({"messages": new_messages})

            # Odczytujemy materiał i pytania z wywołania narzędzia notatki.
            for message in new_messages:
                if message.type == "ai":
                    for call in message.tool_calls:
                        if call["name"] == "create_study_note":
                            last_material = call["args"].get("material", "")

                elif (
                    message.type == "tool"
                    and message.name == "create_study_note"
                ):
                    try:
                        note = json.loads(message.content)
                        last_questions = note.get("questions", [])
                    except (json.JSONDecodeError, TypeError):
                        last_questions = []

            note_created = any(
                message.type == "tool"
                and message.name == "create_study_note"
                for message in new_messages
            )

            if note_created and last_material and last_questions:
                choice = input(
                    "\nCzy chcesz teraz rozwiązać quiz z tej notatki? "
                    "(tak/nie): "
                ).strip().lower()

                if choice in ("tak", "t", "yes", "y"):
                    run_quiz(last_material, last_questions)
                else:
                    print("Jasne! Możemy zrobić quiz później.")


if __name__ == "__main__":
    main()
