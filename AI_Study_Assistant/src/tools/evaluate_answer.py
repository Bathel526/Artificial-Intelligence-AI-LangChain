from src.config import model
from langchain.tools import tool
from src.schemas.anwser_evaluation import AnswerEvaluation

@tool
def evaluate_answer(
        material: str,
        question: str,
        user_answer: str,
) -> dict:
    """Oceń odpowiedź ucznia na podstawie materiału źródłowego."""

    print("TOOL evaluate_answer został wywołany")

    evaluation_model = model.with_structured_output(AnswerEvaluation)

    prompt = f"""
        Jesteś nauczycielem oceniającym odpowiedzi ucznia.

        MATERIAŁ ŹRÓDŁOWY JEST JEDYNYM ŹRÓDŁEM WIEDZY.
        Nie wykorzystuj wiedzy ogólnej ani własnych przypuszczeń.

        NAJPIERW USTAL:
        1. Czy na pytanie można odpowiedzieć na podstawie materiału?
        2. Jakie informacje powinna zawierać poprawna odpowiedź?
        3. Czy odpowiedź ucznia jest zgodna z tymi informacjami?

        ZASADY OCENIANIA:

        1. "not_in_material":
           Wybierz, jeśli materiał nie zawiera informacji pozwalających
           odpowiedzieć na zadane pytanie.
           Nie próbuj uzupełniać braków wiedzą ogólną.

        2. "correct":
           Wybierz, jeśli odpowiedź ucznia jest zgodna z materiałem
           i zawiera wszystkie najważniejsze informacje wymagane
           przez pytanie. Uznawaj poprawne odpowiedzi sformułowane
           własnymi słowami.

        3. "partially_correct":
           Wybierz tylko wtedy, gdy odpowiedź zawiera przynajmniej
           jedną poprawną informację wynikającą z materiału,
           ale pomija inną istotną informację wymaganą przez pytanie.
           Odpowiedź nie może jednocześnie zawierać zasadniczej
           sprzeczności z materiałem.

        4. "incorrect":
           Wybierz, jeśli odpowiedź:
           - jest sprzeczna z materiałem,
           - podaje nieprawdziwe informacje,
           - zawiera wyłącznie informacje niepotwierdzone w materiale,
           - nie odpowiada na zadane pytanie.

        WAŻNA ZASADA:
        Informacja sprzeczna z materiałem nie może zostać uznana
        za częściowo poprawną tylko dlatego, że dotyczy tematu pytania.

        PRZYKŁADY:

        Materiał: Delfiny utrzymują więzi społeczne nawet w mętnej wodzie.

        Pytanie: Czy delfiny mogą utrzymywać więzi społeczne w mętnej wodzie?

        Odpowiedź: Tak.
        Ocena: correct.

        Odpowiedź: Nie, potrzebują przezroczystej wody.
        Ocena: incorrect.

        Odpowiedź: Tak, również na duże odległości.
        Ocena: correct.

        Odpowiedź: Tak, ale nie wiem, jak to robią.
        Ocena: correct, jeśli pytanie dotyczy wyłącznie możliwości utrzymywania więzi.

        DODATKOWE ZASADY:

        - Nie uznawaj odpowiedzi za poprawną tylko dlatego,
          że zawiera słowa związane z pytaniem.
        - Nie dopisuj uczniowi informacji, których nie podał.
        - Nie wymagaj informacji, których nie ma w materiale.
        - Nie karz za błędy ortograficzne, literówki ani brak polskich znaków,
          jeśli znaczenie odpowiedzi jest jasne.
        - Jeśli odpowiedź zawiera zarówno poprawne, jak i sprzeczne
          informacje, wybierz incorrect, jeśli sprzeczność dotyczy
          głównej odpowiedzi na pytanie.
        - Feedback powinien zawierać maksymalnie 2 krótkie zdania.
        - Correct_answer musi zawierać poprawną odpowiedź wynikającą
          z materiału.
        - Jeśli wybierzesz not_in_material, wyjaśnij, że materiał
          nie pozwala rozstrzygnąć pytania.

        MATERIAŁ:
        {material}

        PYTANIE:
        {question}

        ODPOWIEDŹ UCZNIA:
        {user_answer}
    """

    result = evaluation_model.invoke(prompt)

    return result.model_dump()
