from langchain.agents import create_agent

from src.config import model

from src.tools.count_words import count_words
from src.tools.calculate import calculate
from src.tools.create_study_note import create_study_note
from src.tools.evaluate_answer import evaluate_answer

def create_study_agent(checkpointer):
    return create_agent(
        model=model,
        tools=[
            count_words,
            calculate,
            create_study_note,
            evaluate_answer,
        ],
        system_prompt=(
            "Jesteś asystentem do nauki. Odpowiadaj w języku użytkownika. "
    
            "ZASADY KORZYSTANIA Z NARZĘDZI: "
    
            "1. Jeśli użytkownik prosi o utworzenie, przygotowanie "
            "lub napisanie notatki na podstawie materiału, "
            "ZAWSZE wywołaj narzędzie create_study_note. "
            "Nie twórz notatki samodzielnie w odpowiedzi tekstowej. "
    
            "2. Jeśli użytkownik prosi o obliczenia, użyj calculate. "
    
            "3. Jeśli użytkownik prosi o policzenie słów, "
            "użyj count_words. "
    
            "4. Jeśli użytkownik odpowiada na pytanie quizowe, "
            "oceniaj odpowiedź za pomocą evaluate_answer. "
    
            "5. Nie pomijaj narzędzi, gdy ich użycie jest wymagane. "
    
            "6. Nie twórz notatki, jeśli użytkownik o nią nie prosi."
        ),
        checkpointer=checkpointer,
    )