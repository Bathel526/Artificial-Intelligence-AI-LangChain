# Voice Translator - Notatki

### 1. `sounddevice` - nagrywanie dźwięku z mikrofonu

`sounddevice` to biblioteka Pythona umożliwiająca nagrywanie i
odtwarzanie dźwięku. Korzysta z PortAudio i współpracuje m.in. z
tablicami NumPy.

W projekcie biblioteka służy do pobierania dźwięku z mikrofonu. Nie
rozpoznaje sama słów, dostarcza ona dane audio, które następnie mogą
zostać przekazane do modelu rozpoznawania mowy.

Przykład użycia:

``` python
import sounddevice as sd

with sd.InputStream(
    samplerate=16000,
    channels=1,
    dtype="float32",
):
    ...
```

Parametry oznaczają:

- `InputStream` - otwiera strumień dźwięku wejściowego, np. z
mikrofonu.
- `samplerate=16000` - częstotliwość próbkowania wynosi 16 000
próbek na sekundę.
- `channels=1` - nagrywanie jednego kanału, czyli mono.
- `dtype="float32"` - próbki dźwięku są przechowywane jako liczby
zmiennoprzecinkowe 32-bitowe.
- `callback` - funkcja wywoływana w trakcie odbierania kolejnych
fragmentów audio.

W omawianym projekcie fragmenty nagrania są gromadzone, a następnie
łączone w jedną tablicę NumPy. Po zakończeniu nagrywania takie dane
trafiają do funkcji rozpoznającej mowę.

[Dokumentacja
sounddevice](https://python-sounddevice.readthedocs.io/)

---

### 3. `faster-whisper` - rozpoznawanie mowy

`faster-whisper` to implementacja modelu Whisper służącego do
automatycznego rozpoznawania mowy (*speech-to-text*, STT). Pozwala
przekształcić nagranie audio w tekst.

W projekcie: Dźwięk jest nagrywany przez `sounddevice`. Dane audio
są przekazywane do modelu `WhisperModel`, który analizuje mowę i
zwraca rozpoznane fragmenty tekstu. Fragmenty te są łączone w jeden
tekst, który można przetłumaczyć.

Przykład:

``` python
from faster_whisper import WhisperModel

whisper_model = WhisperModel(
    "small",
    device="cpu",
    compute_type="int8",
)

segments, info = whisper_model.transcribe(
    audio,
    language="pl",
    vad_filter=True,
)

text = " ".join(segment.text.strip() for segment in segments)
```

Znaczenie wybranych ustawień:

- `"small"` - wariant modelu; większe modele zwykle mogą lepiej
rozpoznawać mowę, ale potrzebują więcej zasobów (`"basic"` jest
mniejszym modelem ale po kilku próbach zmieniłem na `"small"` myślac,
że lepiej rozpozna wszystkie słowa. Mówiłem np. wazon, a łapało
azom, można spokojnie zmienić na lżejszy `basic`)
- `device="cpu"` - obliczenia wykonywane są na procesorze.
- `compute_type="int8"` - wykorzystuje obliczenia o niższej
precyzji, co może zmniejszyć zużycie pamięci i przyspieszyć pracę na
CPU.
- `language="pl"` - informacja, że nagranie jest w języku polskim.
- `vad_filter=True` - włącza filtr wykrywający aktywność głosową,
aby ograniczyć przetwarzanie ciszy.

Model może pobrać potrzebne pliki przy pierwszym uruchomieniu.
Dokładność zależy m.in. od jakości mikrofonu, hałasu, wymowy i wybranego
modelu.

---

### 4. Piper TTS - zamiana tekstu na mowę

**TTS** (*text-to-speech*) oznacza syntezę mowy, czyli zamianę tekstu na
dźwięk. Piper umożliwia generowanie mowy lokalnie, z użyciem pobranego
modelu głosu.

W projekcie tekst po tłumaczeniu jest przekazywany do Piper, który
generuje plik WAV. Następnie dźwięk jest odtwarzany w systemie Windows.

Przykładowy schemat:

``` python
from piper import PiperVoice

voice = PiperVoice.load("sciezka/do/glosu.onnx")
```

W projekcie używane są głosy zapisane w plikach `.onnx`. Do głosu
potrzebny jest również plik konfiguracyjny o tej samej nazwie z końcówką
`.onnx.json`.

### Głosy słyszę (pobieranie):

[Dokumentacja głosów Piper](https://tderflinger.github.io/piper-docs/about/voices/)

Przy pobieraniu głosu należy sprawdzić, czy pobrano zarówno plik
`.onnx`, jak i odpowiadający mu `.onnx.json`.

---

### 5. `winsound` i `wave` - zapis i odtwarzanie pliku WAV

W projekcie wykorzystywane są również standardowe moduły Pythona:

### `wave`

Moduł `wave` umożliwia zapisywanie i odczytywanie plików WAV.

``` python
import wave

with wave.open("output.wav", "wb") as wav_file:
    voice.synthesize_wav(text, wav_file)
```

- `"output.wav"` - nazwa pliku wyjściowego.
- `"wb"` - otwarcie pliku do zapisu w trybie binarnym.

### `winsound`

`winsound` to moduł dostępny w Pythonie dla Windows, który pozwala m.in.
odtwarzać dźwięki.

``` python
import winsound

winsound.PlaySound("output.wav", winsound.SND_FILENAME)
```

Moduł ten jest zależny od systemu Windows. W aplikacji wieloplatformowej
należałoby rozważyć inne rozwiązanie do odtwarzania dźwięku.

Dokumentacja:
- [`wave`](https://docs.python.org/3/library/wave.html)
- [`winsound`](https://docs.python.org/3/library/winsound.html)

---

### 6. Font Awesome - ikony interfejsu

tak zostawiam dla potomnych, można znaleźć te ikony wszędzie jednak ja najbardziej lubię tą stronkę

[Font Awesome](https://fontawesome.com/) to biblioteka ikon używanych
m.in. w stronach internetowych i interfejsach aplikacji. Zawiera ikony
przedstawiające popularne czynności i elementy, np. mikrofon,
zatrzymanie, głośnik czy język.

W projekcie ikony pobrano w formacie **SVG**, a następnie
przekonwertowano do **PNG**, aby można było wczytać je przez Pillow i
wyświetlić w CustomTkinter.

### SVG a PNG  różnice

- **SVG** (*Scalable Vector Graphics*) - format wektorowy; obraz
jest opisany za pomocą kształtów i ścieżek, więc można go skalować
bez typowej utraty ostrości.
- **PNG** - format rastrowy; obraz składa się z pikseli. Jest
szeroko obsługiwany przez biblioteki do wyświetlania obrazów.

Przykładowe ikony w projekcie:

- `microphone.png` - ikona nagrywania.
- `stop.png` - ikona zatrzymania.
- `volume-high.png` - ikona odtwarzania dźwięku.
- `language.png` - ikona języka lub tłumaczenia.

[Strona Font Awesome](https://fontawesome.com/)

---

### 7. Pillow i CustomTkinter - obrazy oraz interfejs graficzny

### Pillow (`PIL`)

Pillow to biblioteka do otwierania, przekształcania i zapisywania
obrazów. W projekcie służy do wczytywania plików PNG z ikonami.

``` python
from PIL import Image

image = Image.open("microphone.png").convert("RGBA")
```

- `Image.open(...)` - otwiera plik obrazu.
- `.convert("RGBA")` - konwertuje obraz do trybu z kanałem alfa,
    który pozwala obsługiwać przezroczystość.




## test

randomowy tekst jak daje tytuł z dwoma: "##" to jest kreska jak daje z trzema: "### to jej nie ma

### test