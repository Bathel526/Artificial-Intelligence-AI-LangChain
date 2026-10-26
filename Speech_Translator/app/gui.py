from pathlib import Path

from PIL import Image

import threading
from tkinter import messagebox

import customtkinter as ctk

from app.speech.recognizer import record_audio, transcribe_audio
from app.speech.speaker import speak_text
from app.translation.translator import translate_text


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


LANGUAGES = {
    "Angielski (GB)": "angielski",
    "Niemiecki (DE)": "niemiecki",
    "Hiszpański (ES)": "hiszpański",
}


class SpeechTranslatorApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Voice Translator")
        self.geometry("820x760")
        self.minsize(680, 650)

        self.recording = False
        self.audio_chunks = []
        self.audio_stream = None
        self.audio_lock = threading.Lock()
        self.processing = False

        self.icons = self._load_icons()
        self._build_ui()
        self.protocol("WM_DELETE_WINDOW", self._on_close)

    def _load_icons(self):
        icons_dir = Path(__file__).parent / "assets" / "icons"
        loaded_icons = {}

        for name in ("microphone", "stop", "volume-high", "language"):
            png_path = icons_dir / f"{name}.png"
            image = Image.open(png_path).convert("RGBA")

            loaded_icons[name] = ctk.CTkImage(
                light_image = image,
                dark_image = image,
                size = (24, 24),
            )

        return loaded_icons

    def _build_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(4, weight=1)
        self.grid_rowconfigure(6, weight=1)

        # Nagłówek
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.grid(row=0, column=0, padx=28, pady=(24, 12), sticky="ew")

        ctk.CTkLabel(
            header,
            text="Voice Translator",
            font=ctk.CTkFont(size=30, weight="bold"),
        ).pack(anchor="w")

        # Wybór języka
        ctk.CTkLabel(
            self,
            text="Język docelowy",
            font=ctk.CTkFont(size=15, weight="bold"),
        ).grid(row=1, column=0, padx=30, pady=(12, 6), sticky="w")

        self.language_menu = ctk.CTkOptionMenu(
            self,
            values=list(LANGUAGES.keys()),
            width=250,
            height=38,
        )
        self.language_menu.grid(
            row=2, column=0, padx=30, pady=(0, 16), sticky="w"
        )

        # Przyciski nagrywania
        buttons = ctk.CTkFrame(self, fg_color="transparent")
        buttons.grid(row=3, column=0, padx=30, pady=(0, 16), sticky="ew")
        buttons.grid_columnconfigure((0, 1), weight=1)

        self.start_button = ctk.CTkButton(
            buttons,
            text="Rozpocznij nagrywanie",
            image=self.icons["microphone"],
            compound="left",
            height=46,
            font=ctk.CTkFont(size=15, weight="bold"),
            command=self.start_recording,
        )
        self.start_button.grid(
            row=0, column=0, padx=(0, 8), sticky="ew"
        )

        self.stop_button = ctk.CTkButton(
            buttons,
            text="Zatrzymaj i tłumacz",
            image=self.icons["stop"],
            compound="left",
            height=46,
            fg_color="#343847",
            hover_color="#454B5E",
            font=ctk.CTkFont(size=15, weight="bold"),
            command=self.stop_recording,
            state="disabled",
        )
        self.stop_button.grid(
            row=0, column=1, padx=(8, 0), sticky="ew"
        )

        # Rozpoznany tekst
        ctk.CTkLabel(
            self,
            text="Rozpoznany tekst (polski)",
            font=ctk.CTkFont(size=16, weight="bold"),
        ).grid(row=4, column=0, padx=30, pady=(0, 6), sticky="nw")

        self.original_text = ctk.CTkTextbox(
            self,
            height=130,
            corner_radius=12,
            font=ctk.CTkFont(size=15),
            wrap="word",
            state="disabled",
        )
        self.original_text.grid(
            row=4, column=0, padx=30, pady=(30, 12), sticky="nsew"
        )

        # Tłumaczenie
        ctk.CTkLabel(
            self,
            text="Tłumaczenie   ",
            image=self.icons["language"],
            compound="right",
            font=ctk.CTkFont(size=16, weight="bold"),
        ).grid(row=5, column=0, padx=30, pady=(0, 6), sticky="w")

        self.translated_text = ctk.CTkTextbox(
            self,
            height=130,
            corner_radius=12,
            font=ctk.CTkFont(size=15),
            wrap="word",
            state="disabled",
        )
        self.translated_text.grid(
            row=6, column=0, padx=30, pady=(0, 12), sticky="nsew"
        )

        # Odtwarzanie
        self.speak_button = ctk.CTkButton(
            self,
            text="Odtwórz tłumaczenie",
            image=self.icons["volume-high"],
            compound="left",
            height=42,
            command=self.play_translation,
            state="disabled",
        )
        self.speak_button.grid(
            row=7, column=0, padx=30, pady=(0, 12), sticky="ew"
        )

        self.status_label = ctk.CTkLabel(
            self,
            text="Gotowy. Wybierz język i rozpocznij nagrywanie.",
            text_color="#62C99A",
            wraplength=740,
        )
        self.status_label.grid(
            row=8, column=0, padx=30, pady=(0, 20), sticky="w"
        )

    def set_status(self, text, color="#A5ADBC"):
        self.status_label.configure(text=text, text_color=color)

    def start_recording(self):
        if self.recording or self.processing:
            return

        self.audio_chunks = []

        try:
            import sounddevice as sd
            import numpy as np

            def audio_callback(indata, frames, time_info, status):
                if status:
                    print(f"Informacja o nagrywaniu: {status}")

                with self.audio_lock:
                    if self.recording:
                        self.audio_chunks.append(indata.copy())

            self.recording = True

            self.audio_stream = sd.InputStream(
                samplerate=16000,
                channels=1,
                dtype="float32",
                callback=audio_callback,
            )
            self.audio_stream.start()

            self.start_button.configure(state="disabled")
            self.stop_button.configure(state="normal")
            self.language_menu.configure(state="disabled")
            self.set_status("🔴 Nagrywam... Mów po polsku.", "#FF6B6B")

        except Exception as error:
            self.recording = False
            self.set_status("Nie udało się rozpocząć nagrywania.", "#FF6B6B")
            messagebox.showerror("Błąd mikrofonu", str(error))

    def stop_recording(self):
        if not self.recording:
            return

        self.recording = False

        try:
            if self.audio_stream is not None:
                self.audio_stream.stop()
                self.audio_stream.close()
                self.audio_stream = None

            with self.audio_lock:
                chunks = list(self.audio_chunks)

            if not chunks:
                self._finish_processing()
                self.set_status("Nie nagrano dźwięku. Spróbuj ponownie.", "#FF6B6B")
                return

            import numpy as np
            audio = np.concatenate(chunks, axis=0).flatten()

            selected_language = LANGUAGES[self.language_menu.get()]

            self.processing = True
            self.stop_button.configure(state="disabled")
            self.set_status(
                "Rozpoznaję mowę i tłumaczę. To może chwilę potrwać...",
                "#F0B45A",
            )

            threading.Thread(
                target=self._process_audio,
                args=(audio, selected_language),
                daemon=True,
            ).start()

        except Exception as error:
            self._finish_processing()
            messagebox.showerror("Błąd nagrywania", str(error))

    def _process_audio(self, audio, target_language):
        try:
            recognized = transcribe_audio(audio)

            if not recognized:
                self.after(0, self._show_no_speech)
                return

            translation = translate_text(recognized, target_language)

            self.after(
                0,
                lambda: self._show_results(recognized, translation),
            )

        except Exception as error:
            self.after(
                0,
                lambda err=error: self._show_error(err),
            )

    def _show_results(self, recognized, translation):
        recognized = recognized[:1].upper() + recognized[1:] if recognized else recognized
        translation = translation[:1].upper() + translation[1:] if translation else translation
        self.original_text.configure(state="normal")
        self.original_text.delete("1.0", "end")
        self.original_text.insert("1.0", recognized)
        self.original_text.configure(state="disabled")

        self.translated_text.configure(state="normal")
        self.translated_text.delete("1.0", "end")
        self.translated_text.insert("1.0", translation)
        self.translated_text.configure(state="disabled")

        self.last_translation = translation
        self.last_language = LANGUAGES[self.language_menu.get()]

        self.speak_button.configure(state="normal")
        self._finish_processing()
        self.set_status("Gotowe! Tłumaczenie jest dostępne.", "#62C99A")

    def _show_no_speech(self):
        self._finish_processing()
        self.set_status("Nie udało się rozpoznać mowy. Spróbuj ponownie.", "#FF6B6B")

    def _show_error(self, error):
        self._finish_processing()
        self.set_status("Wystąpił błąd.", "#FF6B6B")
        messagebox.showerror("Błąd", str(error))

    def _finish_processing(self):
        self.processing = False
        self.start_button.configure(state="normal")
        self.stop_button.configure(state="disabled")
        self.language_menu.configure(state="normal")

    def play_translation(self):
        translation = self.translated_text.get("1.0", "end").strip()

        if not translation:
            return

        target_language = LANGUAGES[self.language_menu.get()]

        self.speak_button.configure(state="disabled")
        self.set_status("Odtwarzam tłumaczenie...", "#F0B45A")

        def worker():
            try:
                speak_text(translation, target_language)
                self.after(
                    0,
                    lambda: self._speech_finished(),
                )
            except Exception as error:
                self.after(
                    0,
                    lambda err=error: self._show_error(err),
                )

        threading.Thread(target=worker, daemon=True).start()

    def _speech_finished(self):
        self.speak_button.configure(state="normal")
        self.set_status("Odtwarzanie zakończone.", "#62C99A")

    def _on_close(self):
        if self.recording and self.audio_stream is not None:
            self.recording = False
            try:
                self.audio_stream.stop()
                self.audio_stream.close()
            except Exception:
                pass

        self.destroy()


if __name__ == "__main__":
    app = SpeechTranslatorApp()
    app.mainloop()
