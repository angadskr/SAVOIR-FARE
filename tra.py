import sys
from PyQt5.QtWidgets import ( # type: ignore
    QApplication,
    QMainWindow,
    QLabel,
    QLineEdit,
    QTextEdit,
    QPushButton,
    QComboBox,
    QVBoxLayout,
    QWidget,
    QMessageBox,
)
from googletrans import Translator, LANGUAGES


class TranslatorApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Text Translation App")
        self.setGeometry(100, 100, 600, 400)

        
        self.translator = Translator()

        
        self.initUI()

    def initUI(self):
        # Source Text Label and TextEdit
        source_label = QLabel("Source Text:", self)
        self.source_text = QTextEdit(self)

        # Target Language ComboBox
        target_label = QLabel("Target Language:", self)
        self.target_language = QComboBox(self)
        self.target_language.addItems(LANGUAGES.values())

        # Translate Button
        translate_button = QPushButton("Translate", self)
        translate_button.clicked.connect(self.translate_text)

        # Translated Text Label and TextEdit
        translated_label = QLabel("Translated Text:", self)
        self.translated_text = QTextEdit(self)
        self.translated_text.setReadOnly(True)

        # Layout Setup
        layout = QVBoxLayout()
        layout.addWidget(source_label)
        layout.addWidget(self.source_text)
        layout.addWidget(target_label)
        layout.addWidget(self.target_language)
        layout.addWidget(translate_button)
        layout.addWidget(translated_label)
        layout.addWidget(self.translated_text)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def translate_text(self):
        try:
            # Get source text and target language
            source_text = self.source_text.toPlainText()
            target_lang = list(LANGUAGES.keys())[
                self.target_language.currentIndex()
            ]

            # Perform translation
            translation = self.translator.translate(source_text, dest=target_lang)
            self.translated_text.setPlainText(translation.text)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Translation failed: {str(e)}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TranslatorApp()
    window.show()
    sys.exit(app.exec_())