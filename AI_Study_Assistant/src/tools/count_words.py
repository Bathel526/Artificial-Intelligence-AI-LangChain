from langchain.tools import tool

@tool
def count_words(text: str) -> int:
    """Policz liczbę słów w podanym tekście."""
    print("TOOL count_words został wywołany")
    return len(text.split())