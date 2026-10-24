# Czym jest Ollama?

Ollama jest narzędziem umożliwiającym pobieranie i uruchamianie modeli językowych lokalnie, bez konieczności korzystania z zewnętrznych usług. Umożliwia testowanie modeli AI, prowadzenie rozmów oraz integrowanie ich z własnymi aplikacjami. Dzięki temu można eksperymentować z różnymi modelami, kontrolować ich konfigurację i ograniczyć przesyłanie danych do zewnętrznych usług.

---

## 1. Biblioteka modeli Ollama

Modele można znaleźć w oficjalnej bibliotece Ollama:

<https://ollama.com/library>

Jest to katalog modeli, które można uruchamiać lokalnie na komputerze. Przy każdym modelu można sprawdzić dostępne warianty, ich rozmiary oraz instrukcje uruchomienia.

### Oznaczenia w nazwach modeli

- **1.5B, 4B, 7B itd.** — liczba parametrów modelu, wyrażana w miliardach (*B* = *billion*, czyli miliard). Większa liczba parametrów może sprzyjać lepszym odpowiedziom, ale sama w sobie nie gwarantuje wyższej jakości. Większe modele zwykle wymagają więcej pamięci i mogą działać wolniej.
- **Instruct** — model dostrojony do wykonywania poleceń i odpowiadania na pytania.
- **Q4_K_M** — wariant kwantyzacji, czyli sposób zapisu wag modelu z mniejszą precyzją, co pozwala ograniczyć zużycie pamięci. Zwykle wiąże się to z pewnym kompromisem jakości względem wariantu o wyższej precyzji.
- **Latest** — domyślny wariant przypisany do danej nazwy w bibliotece. Nie oznacza automatycznie, że jest to najnowsza generacja modelu.

> **Ważne:** jakość odpowiedzi zależy nie tylko od liczby parametrów, lecz także od rodziny modelu, sposobu jego dostrojenia, kwantyzacji, użytego szablonu rozmowy oraz treści polecenia.

---

## 2. Podstawowe komendy

### Pobranie i uruchomienie modelu

Przykładowo:

```powershell
ollama run qwen2.5:1.5b
```

Jeżeli model nie jest jeszcze pobrany, Ollama pobierze go, a następnie uruchomi. Nazwa modelu jest przykładowa i może zostać zastąpiona inną pozycją z biblioteki.

### Wyświetlenie pobranych modeli

```powershell
ollama list
```

### Usunięcie pobranego modelu

```powershell
ollama rm qwen2.5:1.5b
```

### Zakończenie rozmowy z modelem

W interaktywnym trybie Ollama:

```text
/bye
```

### Przydatne dodatkowe komendy

#### Samo pobranie modelu

```powershell
ollama pull qwen2.5:1.5b
```

Pobiera model bez rozpoczynania rozmowy. Przydatne, gdy wcześniej chce się przygotować kilka modeli do testów.

#### Informacje o lokalnym modelu

```powershell
ollama show qwen2.5:1.5b
```

Wyświetla informacje o modelu, takie jak jego szczegóły i konfiguracja.

#### Sprawdzenie działających modeli

```powershell
ollama ps
```

Pokazuje modele aktualnie załadowane i działające w Ollama.

#### Uruchomienie pojedynczego testu bez interaktywnej sesji

```powershell
ollama run qwen2.5:1.5b "Odpowiedz po polsku: ile to 2 + 2?"
```

Pozwala szybko sprawdzić odpowiedź na konkretne polecenie. Po otrzymaniu odpowiedzi nie trzeba prowadzić dalszej rozmowy w interaktywnym trybie.

#### Sprawdzenie wersji Ollama

```powershell
ollama --version
```

Przydatne podczas diagnozowania różnic w zachowaniu modeli lub obsłudze parametrów.

---

## 3. Problem: bardzo małe modele i niska jakość odpowiedzi

Modele o niewielkiej liczbie parametrów, na przykład **1.5B**, mają mniejsze wymagania sprzętowe, ale mogą mieć wyraźne ograniczenia jakościowe. W zależności od konkretnego modelu mogą pojawiać się:

- błędy gramatyczne, ortograficzne i składniowe;
- zdania, które brzmią nienaturalnie albo nie mają logicznego sensu;
- niepoprawne odmiany wyrazów;
- przypadkowe wtrącenia słów z innych języków;
- wyrazy, które wyglądają na zmyślone lub są użyte w niewłaściwym kontekście;
- powtarzanie treści, urywanie zdań lub nieprzestrzeganie instrukcji.

### Przykład wadliwej odpowiedzi

**Polecenie:**

```text
Cześć, co tutaj robisz?
```

**Przykładowa odpowiedź modelu:**

```text
Jestem Qwen, to jest robota AI specjalizujący się w odpowiedzi na pytania,
dostosowywanych do oficjalnych potrzeb.
Nie mogę roboczo, bo nie jestem człowiekiem. Mój główny związek polega
na pomocy użytkownikom, odpowiedziawszy na thunty i zasady dotyczące ich potrzeb.
```

Odpowiedź zawiera nienaturalne sformułowania, błędy gramatyczne oraz słowo „thunty”, które nie pasuje do kontekstu.

### Możliwe przyczyny i sposoby postępowania

1. **Ograniczone możliwości modelu** — najmniejsze modele mogą gorzej radzić sobie z danym językiem, dłuższymi poleceniami i generowaniem spójnego tekstu.
2. **Niedopasowanie modelu do zadania** — warto sprawdzić inną rodzinę modeli lub wariant przeznaczony do wykonywania instrukcji (*Instruct*).
3. **Kwantyzacja** — mocno skwantyzowany wariant może mieć niższą jakość niż wariant o wyższej precyzji, choć wpływ zależy od modelu i zadania.
4. **Ustawienia generowania i szablon rozmowy** — niewłaściwe parametry lub szablon mogą pogarszać wynik.
5. **Oczekiwania wobec małego modelu** — większa liczba parametrów nie gwarantuje poprawności, ale przy zadaniach wymagających dobrej polszczyzny większy, odpowiednio dostrojony model może być lepszym wyborem.

**Wniosek:** jeśli model regularnie tworzy niezrozumiałe zdania, miesza języki lub wymyśla wyrazy, samo dopracowywanie polecenia może nie wystarczyć. Warto porównać kilka modeli na tym samym zestawie pytań.

---

## 4. Problem: nadmierne „myślenie” modelu (`think`)

Niektóre modele, w tym wybrane warianty rodziny Qwen3, obsługują tryb rozumowania określany jako **thinking**. W tym trybie model może generować dodatkowy tekst poświęcony analizie zadania przed podaniem odpowiedzi końcowej.

Może to prowadzić do:

- bardzo długich odpowiedzi na proste pytania;
- dużego zużycia tokenów i wydłużenia czasu generowania;
- pojawiania się w wyniku szczegółowego toku rozumowania zamiast krótkiej odpowiedzi;
- urywania tekstu przed odpowiedzią końcową, jeżeli generowanie zostanie przerwane lub osiągnie limit tokenów.

Token to jednostka tekstu przetwarzana przez model. Nie odpowiada zawsze jednemu słowu — może reprezentować całe krótkie słowo, fragment wyrazu, znak lub część tekstu.

### Przykład problemu

Próba uruchomienia modelu z wyłączonym trybem myślenia:

```powershell
ollama run qwen3:4b --think=false "Ile to 2 + 2? Odpowiedz po polsku jednym krótkim zdaniem."
```

Oczekiwany wynik:

```text
2 + 2 = 4.
```

Zamiast tego model może zacząć generować długi tekst po angielsku:

```text
Okay, the user is asking "Ile to 2 + 2?" which translates to
"How much is 2 + 2?" in Polish. They want the answer in Polish,
one short sentence.

First, I need to calculate 2 + 2. That's straightforward: 4.

Now, the answer should be in Polish. The phrase for "2 + 2 equals"
in Polish would be...
```

Przykład ilustruje sytuację, w której zamiast krótkiej odpowiedzi pojawia się rozbudowany tekst pomocniczy, a generowanie może nie dojść do odpowiedzi końcowej.

### Jak ograniczyć problem?

W przypadku obsługiwanych modeli Qwen3 tryb myślenia można zwykle kontrolować za pomocą opcji Ollama, na przykład:

```powershell
ollama run qwen3:4b --think=false
```

Następnie polecenie można wpisać w uruchomionej sesji. W zależności od wersji Ollama i sposobu uruchamiania modelu obsługa opcji może się różnić. Warto sprawdzić pomoc dla zainstalowanej wersji:

```powershell
ollama run --help
```

Możliwe jest również przekazanie ustawienia w zapytaniu API lub konfiguracji integracji, jeżeli dany interfejs udostępnia taką opcję.

**Istotne rozróżnienie:** `think` nie jest uniwersalnym parametrem wszystkich modeli Ollama. Obsługa trybu myślenia zależy od modelu, jego szablonu oraz wersji Ollama. Jeśli ustawienie `--think=false` nie przynosi efektu, należy sprawdzić dokumentację konkretnego modelu i wersję narzędzia — nie należy zakładać, że każda nazwa modelu obsługuje tę opcję.

### Gdy trybu myślenia nie można wyłączyć

Jeśli dany model mimo ustawienia `--think=false` nadal generuje nadmiernie długi tekst, można:

1. sprawdzić, czy używana wersja Ollama obsługuje tę opcję dla konkretnego modelu;
2. sprawdzić, czy model korzysta z właściwego szablonu rozmowy;
3. przetestować wariant modelu, który domyślnie nie korzysta z trybu rozumowania;
4. ograniczyć maksymalną liczbę generowanych tokenów, jeśli używany interfejs na to pozwala — należy jednak pamiętać, że zbyt niski limit może uciąć także odpowiedź końcową;
5. jasno określić oczekiwany format, np. „Odpowiedz jednym krótkim zdaniem, bez wstępu”.

Samo polecenie „odpowiedz krótko” nie musi wyłączyć wewnętrznego trybu rozumowania. Może ograniczyć odpowiedź końcową, ale nie zawsze ogranicza ilość tekstu generowanego wcześniej.

---

## 5. Testowanie modelu przed integracją z LangChain

Przed podłączeniem modelu do aplikacji lub łańcucha w LangChain warto najpierw sprawdzić go bezpośrednio w terminalu — w **CMD** albo **PowerShellu**. Pozwala to szybko ocenić podstawową jakość odpowiedzi bez pisania kodu integracyjnego i diagnozowania jednocześnie kilku elementów.

### Szybki test w PowerShellu

```powershell
ollama run qwen2.5:1.5b "Cześć, co tutaj robisz? Odpowiedz po polsku jednym zdaniem."
ollama run qwen2.5:1.5b "Ile to 2 + 2? Odpowiedz po polsku jednym krótkim zdaniem."
ollama run qwen2.5:1.5b "Wyjaśnij w dwóch zdaniach, czym jest pamięć RAM."
```

Wystarczy podmienić `qwen2.5:1.5b` na nazwę testowanego modelu i porównać wyniki. Te same pytania należy zadawać każdemu modelowi, aby porównanie było możliwie uczciwe.

### Co sprawdzać przed integracją?

- Czy odpowiedzi są poprawne i logiczne?
- Czy model poprawnie posługuje się danym językiem?
- Czy przestrzega wymagań dotyczących długości i formatu?
- Czy nie generuje nadmiernie długiego tekstu pomocniczego?
- Czy czas odpowiedzi jest akceptowalny?

Jeżeli model już w prostym teście terminalowym udziela niezrozumiałych odpowiedzi, miesza języki albo ignoruje polecenia, integracja z LangChain zwykle nie rozwiąże problemu jakości samego modelu. Najpierw warto przetestować inny model lub jego wariant.

Test terminalowy nie zastępuje testów integracyjnych: LangChain, prompt, parser, historia rozmowy i ustawienia generowania mogą później wpływać na wynik. Pozwala jednak oddzielić podstawowe możliwości modelu od problemów w kodzie aplikacji.

---

## 5. Praktyczna metoda testowania modeli

Aby porównać modele, warto zadać im te same pytania i ocenić wyniki według kilku kryteriów:

- **Poprawność:** czy odpowiedź jest merytorycznie prawidłowa?
- **Język:** czy tekst jest poprawny gramatycznie i ortograficznie?
- **Zgodność z poleceniem:** czy model stosuje się do wskazanego języka, długości i formatu?
- **Zwięzłość:** czy odpowiada bez niepotrzebnych dygresji?
- **Stabilność:** czy podobne pytania prowadzą do równie sensownych odpowiedzi?

Przykładowe polecenie testowe:

```text
Ile to 2 + 2? Odpowiedz po polsku jednym krótkim zdaniem.
```

Następnie można sprawdzić krótkie pytanie opisowe:

```text
Cześć, co tutaj robisz? Odpowiedz po polsku w jednym zdaniu.
```

Wyniki najlepiej zapisywać wraz z dokładną nazwą modelu, jego wariantem, użytymi parametrami oraz wersją Ollama. Ułatwia to ustalenie, czy problem wynika z ograniczeń modelu, jego konfiguracji czy sposobu uruchomienia.

---

