from langchain.tools import tool
from src.config import model
from src.schemas.study_note import StudyNote

@tool
def create_study_note(material: str) -> dict:
    """Utwórz notatkę do nauki na podstawie materiału.
    Zwróć tytuł, podsumowanie, kluczowe pojęcia i pytania sprawdzające."""
    print("TOOL create_study_note został wywołany")

    structured_model = model.with_structured_output(StudyNote)

    prompt = f"""
        Utwórz notatkę do nauki wyłącznie na podstawie materiału źródłowego.

        JĘZYK:
        - Używaj wyłącznie języka materiału źródłowego.

        WIERNOŚĆ MATERIAŁOWI:
        - Materiał źródłowy jest jedynym źródłem informacji.
        - Nie dodawaj informacji spoza materiału.
        - Nie wykorzystuj wiedzy ogólnej ani własnej wiedzy o omawianym temacie.
        - Nie uzupełniaj brakujących informacji własnymi przypuszczeniami.
        - Nie zmieniaj znaczenia terminów ani faktów.
        - Zachowuj dokładne nazwy i pojęcia użyte w materiale.

        KLUCZOWE POJĘCIA:
        - Wybierz tylko najważniejsze pojęcia.
        - Nie powtarzaj tych samych informacji pod innymi nazwami.
        - Każde pojęcie musi mieć uzasadnienie w materiale.

        PYTANIA SPRAWDZAJĄCE:
        1. Każde pytanie musi dotyczyć informacji zawartej w materiale.
        2. Odpowiedź na każde pytanie musi być możliwa do udzielenia
           wyłącznie na podstawie materiału źródłowego.
        3. Nie pytaj o informacje, których materiał nie podaje.
        4. Nie wykorzystuj wiedzy ogólnej, nawet jeśli znasz
           prawidłową odpowiedź na dane pytanie.
        5. Nie rozszerzaj tematyki materiału o powiązane zagadnienia.
        6. Nie twórz pytań wymagających znajomości faktów,
           które nie zostały opisane w materiale.
        7. Pytania mogą wymagać prostego wnioskowania,
           ale wszystkie potrzebne przesłanki muszą znajdować się
           w materiale.
        8. Dopasuj liczbę pytań do długości i zawartości materiału.
        9. Dla krótkiego materiału zazwyczaj wystarczą 2-4 pytania.
        10. Każde pytanie musi sprawdzać inną informację.
        11. Nie twórz kilku pytań o ten sam fakt, nawet jeśli są
            sformułowane innymi słowami.
        12. Unikaj pytań typu tak/nie, jeśli można zadać pytanie
            otwarte sprawdzające tę samą wiedzę.
        13. Pytania muszą być poprawne gramatycznie.
        14. Jeśli materiał nie zawiera wystarczającej liczby różnych
            informacji, wygeneruj mniej pytań.

        KONTROLA KAŻDEGO PYTANIA:
        Przed dodaniem pytania do wyniku:
        - Ustal, jaka dokładnie informacja jest sprawdzana.
        - Znajdź odpowiedni fragment materiału, który ją potwierdza.
        - Sprawdź, czy na pytanie można odpowiedzieć bez korzystania
          z wiedzy spoza materiału.
        - Jeśli nie możesz znaleźć uzasadnienia w materiale,
          usuń pytanie.
        - Nie zastępuj usuniętego pytania pytaniem wymagającym
          wiedzy ogólnej.

        KONTROLA JAKOŚCI:
        - Sprawdź, czy pytania nie powtarzają się znaczeniowo.
        - Sprawdź ich poprawność językową.
        - Sprawdź, czy każde pytanie ma odpowiedź w materiale.
        - Nie zwiększaj liczby pytań kosztem ich zgodności z materiałem.

        FORMAT ODPOWIEDZI:
        Zwróć obowiązkowo wszystkie cztery pola:
        title, summary, key_concepts oraz questions.
        Żadne pole nie może zostać pominięte.
        Jeśli masz mało informacji, nadal zwróć wszystkie pola,
        a listy wypełnij odpowiednią liczbą elementów.

        MATERIAŁ ŹRÓDŁOWY:
        {material}
    """

    note = structured_model.invoke(prompt)

    return note.model_dump()