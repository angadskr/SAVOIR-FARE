import sys
import speech_recognition as sr
import pyttsx3
from googletrans import Translator, LANGUAGES
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QLabel,
    QPushButton,
    QComboBox,
    QTextEdit,
    QVBoxLayout,
    QWidget,
    QMessageBox,
)
from PyQt5.QtCore import Qt


class SpeechTranslationApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Speech Recognition and Translation App")
        self.setGeometry(100, 100, 600, 500)

        # Initialize Translator, Speech Recognizer, and Text-to-Speech Engine
        self.translator = Translator()
        self.recognizer = sr.Recognizer()
        self.tts_engine = pyttsx3.init()

        # UI Components
        self.initUI()

    def initUI(self):
        # Source Speech Recognition Button
        self.speech_button = QPushButton("Record Speech", self)
        self.speech_button.clicked.connect(self.recognize_speech)

        # Recognized Text Display
        recognized_label = QLabel("Recognized Text:", self)
        self.recognized_text = QTextEdit(self)
        self.recognized_text.setReadOnly(True)

        # Target Language Selection
        target_label = QLabel("Target Language:", self)
        self.target_language = QComboBox(self)
        self.target_language.addItems(LANGUAGES.values())

        # Translate Button
        translate_button = QPushButton("Translate", self)
        translate_button.clicked.connect(self.translate_text)

        # Translated Text Display
        translated_label = QLabel("Translated Text:", self)
        self.translated_text = QTextEdit(self)
        self.translated_text.setReadOnly(True)

        # Text-to-Speech Button
        speak_button = QPushButton("Speak Translated Text", self)
        speak_button.clicked.connect(self.speak_translated_text)

        # Layout Setup
        layout = QVBoxLayout()
        layout.addWidget(self.speech_button)
        layout.addWidget(recognized_label)
        layout.addWidget(self.recognized_text)
        layout.addWidget(target_label)
        layout.addWidget(self.target_language)
        layout.addWidget(translate_button)
        layout.addWidget(translated_label)
        layout.addWidget(self.translated_text)
        layout.addWidget(speak_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def recognize_speech(self):
        try:
            with sr.Microphone() as source:
                QMessageBox.information(self, "Recording", "Speak now...")
                self.recognizer.adjust_for_ambient_noise(source)
                audio = self.recognizer.listen(source)

                # Recognize speech using Google Web Speech API
                recognized_text = self.recognizer.recognize_google(audio)
                self.recognized_text.setPlainText(recognized_text)

        except sr.UnknownValueError:
            QMessageBox.warning(self, "Error", "Could not understand the audio.")
        except sr.RequestError as e:
            QMessageBox.critical(self, "Error", f"Speech recognition failed: {e}")

    def translate_text(self):
        try:
            # Get recognized text and target language
            source_text = self.recognized_text.toPlainText()
            target_lang = list(LANGUAGES.keys())[
                self.target_language.currentIndex()
            ]

            # Perform translation
            translation = self.translator.translate(source_text, dest=target_lang)
            self.translated_text.setPlainText(translation.text)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Translation failed: {e}")

    def speak_translated_text(self):
        try:
            # Get the translated text
            text_to_speak = self.translated_text.toPlainText()
            if not text_to_speak.strip():
                QMessageBox.warning(self, "Error", "No translated text to speak.")
                return

            # Speak the text using pyttsx3
            self.tts_engine.say(text_to_speak)
            self.tts_engine.runAndWait()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Text-to-Speech failed: {e}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SpeechTranslationApp()
    window.show()
    sys.exit(app.exec())