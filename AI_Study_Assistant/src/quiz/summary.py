

def show_quiz_summary(results):
    """Wyświetla podsumowanie ocenionych odpowiedzi."""

    print("\n===== PODSUMOWANIE QUIZU =====")

    if not results:
        print("Quiz nie zawiera ocenionych odpowiedzi.")
        return

    excluded = [
        item for item in results
        if item["status"] == "not_in_material"
    ]

    scored_results = [
        item for item in results
        if item["status"] != "not_in_material"
    ]

    correct = sum(
        item["status"] == "correct"
        for item in scored_results
    )

    total = len(scored_results)

    print(f"Liczba wszystkich odpowiedzi: {len(results)}")
    print(f"Pytania wyłączone z oceny: {len(excluded)}")

    if total > 0:
        percentage = round(correct / total * 100)

        print(f"Liczba ocenionych pytań: {total}")
        print(f"W pełni poprawne odpowiedzi: {correct}")
        print(f"Wynik: {percentage}%")
    else:
        print("Brak pytań, które można było ocenić.")

    needs_review = [
        item for item in scored_results
        if item["status"] != "correct"
    ]

    if needs_review:
        print("\nDo powtórki:")
        for item in needs_review:
            print(f"- {item['question']}")
            print(f"  Ocena: {item['status']}")
    else:
        print("\nŚwietnie! Wszystkie ocenione odpowiedzi były poprawne.")

    if excluded:
        print("\nPytania wyłączone z wyniku:")
        for item in excluded:
            print(f"- {item['question']}")

