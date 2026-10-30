import json
from pathlib import Path

from langgraph.checkpoint.sqlite import SqliteSaver

from src.quiz.runner import run_quiz
from src.display import display_response
from src.agent import create_study_agent


BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "study_assistant.db"


def main():
    print("\n=== AI Study Assistant ===")
    print("Zadaj pytanie lub poproś o wykonanie zadania.")
    print("Wpisz 'exit', aby zakończyć.\n")

    last_material = ""
    last_questions = []

    with SqliteSaver.from_conn_string(str(DB_PATH)) as checkpointer:
        agent = create_study_agent(checkpointer)

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
