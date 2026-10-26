from app.speech.recognizer import record_audio, transcribe_audio
from app.translation.translator import translate_text
from app.speech.speaker import speak_text

def main():



    print("\nWybierz język docelowy:")
    print("1. Angielski")
    print("2. Niemiecki")
    print("3. Hiszpański")

    choice = input("Twój wybór (1-3): ")

    languages = {
        "1": "angielski",
        "2": "niemiecki",
        "3": "hiszpański",
    }

    target_language = languages.get(choice)

    if target_language is None:
        print("Nieprawidłowy wybór języka.")
        return

    audio = record_audio()

    print("\nRozpoznaję wypowiedź...")
    recognized_text = transcribe_audio(audio)

    if not recognized_text:
        print("Nie udało się rozpoznać tekstu.")
        return

    print(f"\nRozpoznany tekst: {recognized_text}")


    translation = translate_text(recognized_text, target_language)

    print(f"Tłumaczenie ({target_language}):")
    print(translation)

    print("\nOdtwarzam tłumaczenie...")
    speak_text(translation, target_language)

if __name__ == "__main__":
    main()