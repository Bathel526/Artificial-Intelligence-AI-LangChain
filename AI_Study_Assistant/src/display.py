import json


def display_response(response):
    messages = response["messages"]

    # Sprawdzamy, czy w tej turze utworzono notatkę.
    note_was_created = any(
        message.type == "tool" and message.name == "create_study_note"
        for message in messages
    )

    for message in messages:
        if message.type == "ai" and message.tool_calls:
            print("\n[AI wywołuje narzędzie]")
            print(message.tool_calls)

        elif message.type == "tool":
            print(f"\n[Narzędzie: {message.name}]")

            if message.name == "create_study_note":
                note = json.loads(message.content)

                print("\n===== TWOJA NOTATKA =====")
                print(f"Tytuł: {note['title']}")
                print(f"\nPodsumowanie:\n{note['summary']}")

                print("\nKluczowe pojęcia:")
                for concept in note["key_concepts"]:
                    print(f"- {concept}")

                print("\nPytania sprawdzające:")
                for question in note["questions"]:
                    print(f"- {question}")
            else:
                print(message.content)

        elif message.type == "ai" and message.content:
            if note_was_created:
                continue

            print(f"\nAI: {message.content}")

