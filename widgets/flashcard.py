# Flashcard Widget

from PySide6.QtWidgets import QFrame, QLabel, QVBoxLayout
from PySide6.QtCore import Qt, QRect

class Flashcard(QFrame):
    def __init__(self):
        # Initialise our parent class
        super().__init__()
        self.flashcard_layout = QVBoxLayout()

        # Initialise our flashcard's label
        self.flashcard_text = QLabel()
        self.flashcard_text.setWordWrap(True)
        self.flashcard_text.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Add all widgets and stretch objects
        self.populate_card()

        # Set the card's appearance
        self.style_card()

        # Assign the layout to our parent card
        self.setLayout(self.flashcard_layout)

    def style_card(self):
        # Style our flashcard to look vaguely real
        self.setFixedSize(600, 400)
        self.setStyleSheet("""
        QFrame {
            background-color: rgb(230, 230, 230);
        }
        """)
        self.flashcard_text.setStyleSheet("color: black; font-size: 18pt;")

    def populate_card(self):
        # Center our text horizontally
        self.flashcard_layout.addStretch()
        self.flashcard_layout.addWidget(self.flashcard_text)
        self.flashcard_layout.addStretch()

    def set_text(self, text):
        self.flashcard_text.setText(text)