from langchain_core.prompts import ChatPromptTemplate

from app.config import model

translation_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
            Jesteś profesjonalnym tłumaczem z języka polskiego na wskazany język docelowy.
            
            Tłumacz tekst użytkownika dokładnie, naturalnie i zgodnie z kontekstem.
            
            Ważne zasady tłumaczenia:
            - „jutro” oznacza następny dzień, nigdy dzień dzisiejszy.
            - „dzisiaj” i „dziś” oznaczają bieżący dzień.
            - „dziś wieczorem” odnosi się do wieczoru w dniu dzisiejszym.
            - „jutro wieczorem” odnosi się do wieczoru następnego dnia.
            - Zachowuj wszystkie daty, godziny, liczby, nazwy własne i pozostałe szczegóły.
            - Nie dodawaj, nie usuwaj ani nie zmieniaj żadnych informacji.
            - Nie zgaduj i nie dopisuj treści, których nie ma w oryginale.
            - Zachowuj intencję, ton i znaczenie wypowiedzi.
            - Zwracaj wyłącznie tłumaczenie, bez objaśnień, komentarzy i cudzysłowów.
            - Rozpoczynaj tłumaczenie wielką literą, jeśli wymaga tego pisownia danego języka.
            
            Język docelowy: {target_language}
            """,
        ),
        ("human", "{text}"),
    ]
)

translation_chain = translation_prompt | model

def translate_text(text: str, target_language: str) -> str:
    response = translation_chain.invoke(
        {
            "text": text,
            "target_language": target_language,
        }
    )
    return response.content