# 1 Podstawowe pojęcia

### 1.1 Large Language Model

**LLM (Large Language Model)** to duży model językowy, który został wytrenowany na dużej ilości danych tekstowych, aby rozpoznawać wzorce w języku i generować tekst na podstawie otrzymanego kontekstu.

Model może między innymi:

- odpowiadać na pytania,
- streszczać i tłumaczyć teksty,
- generować kod,
- analizować przekazane informację,
- wykonywać instrukcje zapisane w prompcie,
- przekształcać dane do określonego formatu.

LLM nie działa jak tradycyjna baza danych, która wyszukuje i zwraca zapisany rekord. W typowym przypadku model generuje odpowiedź, przewidując kolejne tokeny na podstawie dotychczasowego tekstu wyuczonych zależności.

---

### 1.2 Token

**Token** to jednostka tekstu przetwarzana przez model. Tokenem może być:

- całe krótkie słowa,
- fragment dłuższego słowa,
- znak interpunkcyjny,
- liczba,
- fragment tekstu zawierający spację.

Przykładowo, słowo `programowanie` może zostać podzielone na kilka tokenów, zależnie od używanego modelu i jego tokenizatora.

Tekst wejściowy jest najpierw przekształcany na tokeny, a następnie model przetwarza ich reprezentacje i generuje tokeny odpowiedzi.

Liczba tokenów wpływa na:
- ilość tekstu, którą model może przetworzyć jednocześnie,
- zużycie pamięci i obliczeń,
- czas generowania odpowiedzi,
- koszt korzystania z modeli udostępnianych przez płatne API.

---

### 1.3 Context window 

**Okno kontekstu** (context window) to maksymalna liczba tokenów, które model może uwzględnić w ramach jednego przetwarzania konwersacji lub zadania.

W zależności od modelu i jego konfiguracji limit ten może wynosić na przykład kilka, kiladziesiąt tysięcy tokenów.

W kontekście mogą znajdować się:

- instrukcje systemowe,
- wiadomości użytkownika,
- wcześniejsze wiadomości konwersacji,
- dane do analizy,
- odpowiedź generowana przez model.

Załóżmy, że model ma skonfigurowane okno kontekstu o wielkości 8 192 tokenów.

Do wykorzystania tego limitu zaliczają się nie tylko tekst pytania, ale również instrukcje, historia rozmowy i odpowiedź. Nie można więc założyć, że całe 8 192 tokeny są dostępne wyłącznie na odpowiedź.

Po przekroczeniu limitu w zależności od konfiguracji może dojść do:

- odrzucenia zbyt długiego wejścia,
- obcięcia części tekstu,
- usunięcia najstarszych wiadomości z historii,
- podzielenia dokumentu na mniejsze fragmenty przed przetwarzaniem.

> **Ciekawostka:** W Ollama parametr `num_ctx` pozwala ustawić wielkość kontekstu, o ile obsługuje go używana wersja integracji i model.

---

### 1.4 Embeddingi

Embedding to reprezentacja danych, najczęściej tekstu w postaci wektora liczb. Wektory te są tworzone przez specjalny model embeddingowy.

Ich celem jest uchwycenie cech znaczeniowych tekstu, tak aby można było porównywać teksty na podstawie ich reprezentacji liczbowych.

Podobieństwo poniższych zdań będzie duże mimo, że zdania różnią się słowami, mają podobne znaczenie. Model embaddingowy może utworzyć na nich wektory, które będą do siebie podobne.

Zastosowanie embeddingów:

- wyszukiwania semantycznego,
- wyszukiwania fragmentów dokumentów,
- budowania baz wektorowych,
- grupowania podobnych tekstów,
- systemów RAG (Retrieval-Augmented Generation).

---

## 2 Parametry

Parametry modelu określają, w jaki sposób generowana jest odpowiedź, jak długa może być oraz jak model zachowuje się podczas przetwarzania tekstu.

### 2.1 `temperature`

```python
temperature=0.7
```

Określa poziom losowości generowania tekstu.
- Niższa wartość zazwyaczaj daje bardziej przewidywalne odpowiedzi.
- Wyższa wartość zazwyczaj zwiększa różnorodność generowanego tekstu.

Wartość ta zazwyczaj zawiera się w przedziale 0.0 - 2.0, gdzie wartość powyżej 1.5 zazwyczaj oznacza skrajną losowość.

### 2.2 `num_predict`

Określa maksymalną liczbę tokenów, które model może wygenerować w odpowiedzi.

```python
num_predict=256
```
Oznacza, że generowanie odpowiedzi może zakończyć się po osiągnięciu 256 tokenów wyjściowych. Oczywiście model może zakończyć odpowiedź wcześniej, gdy uzna ją za kompletną.

Wartość tą można dobrać eksperymentalnie w zależności od przeznaczenia modelu.

### 2.3 `reasoning`

Parametr ten jest związany z trybem rozumowania w niektórych modelach i wersjach integracji.

```python
reasoning=False
```

Nie należy jednak zakładać, że jego działanie będzie identyczne dla wszystkich modeli. Obsługa, znaczenie i sposób przekazywania tego ustawienia zależą od wersji langchain-ollama, Ollama oraz konkretnego modelu.

Ustawienie `reasoning=False` nie gwarantuje, że model całkowicie przestanie wykonywać wewnętrzne obliczenia potrzebne do wygenerowania odpowiedzi. Może wpływać na sposób korzystania z funkcji rozumowania lub prezentowania jej rezultatów, zależnie od obsługiwanej konfiguracji.

### 2.4 `num_ctx`

`num_ctx` określa wielkość okna kontekstu używanego przy generowanu odpowiedzi.

```python
num_ctx=8192
```

Większy kontekst może umożliwić przetwarzanie dłuższych instrukcji, dokumentów i historii rozmowy. Jednocześnie może zwiększać zapotrzebowanie na pamięć.

Wartość ta domyślnie wynosi 2048 w specyfikacji integracji LangChaina z Ollamą. Sama Ollama ma limit 4096, ale zależy to od wersji. Tutaj głównie limituje LangChain. Większe wartości okna kontekstowego są istotne dla systemów typu RAG.

### 2.5 `top_p`

parametr próbkowania, który ogranicza wybór kolejnego tokenu do zbioru kandydatów obejmującego określoną część łącznego prawdopodobieństwa.

```python
top_p=0.9
```

W uproszczeniu model bierze pod uwagę tokeny, których łączne prawdopodobieństwo mieści się w określonym progu, a następnie wybiera spośród nich kolejny token.

Warto pamiętać, że `top_p` i `temperature` oddziałują na siebie. Podczas strojenia modelu najlepiej zmieniać jeden parametr naraz i porównywać wyniki na tych samych pytaniach.

### 2.6 `top_k`

ogranicza wybór kolejnego tokenu do określonej liczby najbardziej prawdopodobnych kandydatów.

```python
top_p=40
```

W uproszczeniu model rozważa 40 najbardziej prawdopodobnych tokenów, a dalszy wybór zależy również od innych ustawień generowania.
- Niższe top_k ogranicza liczbę możliwych wyborów.
- Wyższe top_k pozwala uwzględnić więcej kandydatów.

To ustawienie jest przydatne przy eksperymentowaniu z różnorodnością odpowiedzi, ale nie zawsze trzeba je zmieniać. W wielu przypadkach można zacząć od ustawień domyślnych.

### 2.7 `repeat_penalty`

Wpływa na skłonność modelu do powtarzania tokenów.

```python
repeat_penalty=1.1
```

Wartości większe od `1` mogą ograniczać powtarzanie, natomiast dokładne działanie i efekty zależą od implementacji.

Zbyt mocne ograniczenie powtórzeń może pogorszyć jakość tekstu, zwłaszcza gdy powtarzanie jest naturalne, na przykład w kodzie, listach lub dłuższych wyjaśnieniach.

Warto używać tego parametru wtedy, gdy powtarzanie rzeczywiście stanowi problem.

### 2.8 `seed`

ustala ziarno generatora losowego, jeśli dany mechanizm generowania je obsługuje.

```python
seed=42
```

Stałe ziarno może pomóc w powtarzaniu eksperymentów i porównywaniu ustawień.

Nie daje jednak gwarancji identycznych odpowiedzi w każdym środowisku. Wyniki mogą zależeć również od wersji modelu, sprzętu, implementacji i pozostałych parametrów.

### 2.9 `format`

Parametr `format` może służyć do określenia oczekiwanego formatu wyjścia, na przykład JSON, jeśli obsługują go używana wersja Ollama, model i integracja.

```python
format="json"
```
Może to ułatwić otrzymywanie odpowiedzi w strukturze maszynowej, na przykład:
```json
{
  "nazwa": "Lenovo IdeaPad Slim 3",
  "cena": 2499
}
```

Samo określenie formatu nie rozwiązuje wszystkich problemów. W aplikacji produkcyjnej warto również sprawdzać, czy odpowiedź jest poprawnym JSON-em i czy spełnia wymagany schemat.

### 2.10 `keep-alive`

Określa, jak długo model pozostaje załadowany po zakończeniu żądania, zgodnie z obsługą w Ollama i danej wersji integracji.

```python
keep_alive="5m"
```

Może pozwolić na utrzymanie modelu w pamięci przez pięć minut po użyciu. Kolejne zapytanie w tym czasie może uniknąć ponownego ładowania modelu.

Dłuższy czas utrzymywania modelu może poprawić szybkość kolejnych zapytań, ale zużywa zasoby pamięci.

---

## 3 LanChain

`LangChain` to biblioteka umożliwiająca budowanie aplikacji wykorzystujących modele językowe. Pomaga łączyć modele z promptami, dokumentami, narzędziami, wyszukiwaniem i logiką aplikacji.

Zamiast samodzielnie pisać całą obsługę wywołań modelu, można korzystać z gotowych komponentów i łączyć je w większe procesy.

### 3.1 Lanchain & Ollama

Skrótowy opis jak Ollama współpracuje z Langchainem w omawianym projekcie:
- **Ollama** – uruchamia i udostępnia lokalny model.
- **Model Qwen** – generuje odpowiedzi.
- **ChatOllama** – łączy kod Pythona z modelem dostępnym przez Ollama.
- **ChatPromptTemplate** – definiuje strukturę promptu.
- **LCEL** – pozwala łączyć komponenty w łańcuchy.
- **FastAPI** – udostępnia aplikację przez HTTP.
- **LangServe** – pomaga wystawiać łańcuchy LangChain jako endpointy API i interfejsy testowe.

### 3.3 ChatOllama

`ChatOllama` jest integracją LangChain z modelem czatu udostępnianym przez Ollama.

W przypadku projektu:
```python
from langchain_ollama import ChatOllama

model = ChatOllama(
    model="qwen3:4b-instruct-2507-q4_K_M",
    temperature=0,
    reasoning=False,
    num_predict=256,
)
```

### 3.4 ChatPromptTemplate

`ChatPromptTemplate` pozwala przygotować strukturę wiadomości przekazywanych do modelu czatu.

Przykład:
```python
from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_messages([
    ("system", "Odpowiadaj wyłącznie po polsku."),
    ("human", "{question}"),
])
```

Ten prompt zawiera dwie wiadomości:
- `system` – instrukcje określające sposób działania modelu,
- `human` – treść wiadomości użytkownika.

Fragment {question} jest zmienną, którą należy uzupełnić podczas wywołania promptu.

### 3.5 `invoke()`

`invoke()` metoda używana do uruchamiania komponentu lub łańcucha na podstawie danych wejściowych.

Przykład:
```python
messages = prompt.invoke({
    "question": "Czym jest model językowy?"
})
```

Tutaj uruchamiany jest sam szablon promptu. Nie oznacza to jeszcze wysłania wiadomości do modelu językowego.

Poniższe polecenie przekazuje przygotowane wiadomości do modelu i zwraca odpowiedź.
```python
response = model.invoke(messages)
```

Można też wykonać całość jednym wywołaniem:

```python
response = chain.invoke({
    "question": "Czym jest model językowy?"
})
```
### 3.7 LCEL - LangChain ExpressionLanguage

**LCEL** to sposób łączenia komponentów LangChain w łańcuchy za pomocą operatora `|`.

Operator ten pozwala przekazywać wynik jednego komponentu do kolejnego:
```python
prompt_chain = prompt | model
```

LCEL ułatwia:
- łączenie promptów i modeli,
- tworzenie bardziej złożonych procesów,
- ponowne wykorzystywanie komponentów,
- uruchamianie całego procesu przez jedno wywołanie,
- korzystanie z obsługiwanych przez dany łańcuch mechanizmów, takich jak strumieniowanie odpowiedzi.

Nie każdy komponent automatycznie obsługuje wszystkie funkcje. Możliwości zależą od elementów wykorzystanych w łańcuchu.

### 3.8 partial()

`partial()` pozwala wstępnie ustawić wybrane zmienne szablonu.

```python
shop_chain = shop_prompt.partial(
    products=products,
) | model
```
W tym przypadku katalog products zostaje przypisany do promptu wcześniej. Podczas późniejszego wywołania trzeba więc przekazać pytanie, ale nie trzeba ponownie przekazywać całego katalogu.


### 4 Prompt engineering - tworzenie instrukcji dla modelu

Prompt engineering to proces projektowania i testowania instrukcji oraz danych wejściowych przekazywanych modelowi, aby uzyskać odpowiedzi lepiej dopasowane do określonego zadania.

Skrócona struktura dobierania promptu:
- Rola: Kim model ma być (np. „Jesteś asystentem zakupowym...”).
- Zadanie: Co dokładnie ma zrobić (np. „Wybierz laptopa...”).
- Kontekst: Sytuacja i wymagania (np. „Budżet to 3500 zł, do programowania”).
- Dane źródłowe: Baza wiedzy, na której ma się oprzeć (np. „Korzystaj tylko z tego katalogu: `{products}`”).
- Ograniczenia: Czego modelowi robić nie wolno (np. „Nie zmyślaj parametrów, nie przekraczaj budżetu”).
- Format odpowiedzi: Jak ma wyglądać wynik (np. „Podaj nazwę, cenę i uzasadnienie”).
- Obsługa błędów / braku danych: Co zrobić, gdy czegoś brakuje (np. „Jeśli nie wiesz, zadaj pytanie doprecyzowujące”).

Dobrze przygotowany prompt zmniejsza niejednoznaczność, ale nie gwarantuje poprawności każdej odpowiedzi.

## 4.1 Kontekst i dane w promptach

Kontekst to informacje, które model otrzymuje wraz z pytaniem i może wykorzystać podczas generowania odpowiedzi.

Może obejmować:
- opis problemu,
- dane z katalogu,
- fragmenty dokumentów,
- historię rozmowy,
- wyniki wyszukiwania,
- informacje przekazane przez inne komponenty aplikacji.

Przykładowo, asystent zakupowy nie musi znać wszystkich aktualnych cen laptopów. Można przekazać mu katalog produktów zawierający nazwy, ceny i parametry, a następnie polecić wybór produktu na podstawie tych danych.

```python
shop_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
        Jesteś pomocnym asystentem zakupowym
        specjalizującym się w laptopach.
        Korzystaj z poniższego katalogu produktów:
        {products}
        ...
        """
    ),
    ("human", "{question}"),
])
```

W tym przykładzie {products} zawiera dane źródłowe.

### 4.2 Filtry

Jeżeli aplikacja ma spełniać twarde wymagania, na przykład nigdy nie polecać laptopa droższego niż określony budżet, nie należy polegać wyłącznie na promptach.

Przykładowy filtr w Pythonie:
```python
budget = 3500

eligible_products = [
    product
    for product in products_list
    if product["price"] <= budget
]
```

W tym przykładzie products_list powinno być listą słowników, a każdy słownik musi zawierać pola price i pozostałe dane produktu.

To rozwiązanie jest bardziej niezawodne niż polecenie modelowi, aby samodzielnie pamiętał o każdym ograniczeniu.