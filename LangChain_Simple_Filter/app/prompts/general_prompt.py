from langchain_core.prompts import ChatPromptTemplate


prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
        Odpowiadaj wyłącznie po polsku.
        Używaj dokładnie 2 zdań.
        Nie używaj angielskich słów ani zwrotów.
        Jeśli nie znasz odpowiedzi lub brakuje Ci aktualnych danych,
        powiedz to wprost.
        Nie wymyślaj faktów.
        """
    ),
    ("human", "{question}"),
])