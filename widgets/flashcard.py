# Flashcard Widget

from PySide6.QtWidgets import QWidget, QFrame, QLabel, QVBoxLayout
from PySide6.QtCore import Qt, QRect

class Flashcard(QFrame):
    def __init__(self) -> None:
        # Initialise our parent class
        super().__init__()
        self.flashcard_layout = QVBoxLayout()

        # Add all widgets and stretch objects
        self.populate_card()

        # Set the card's appearance
        self.style_card()

        # Assign the layout to our parent card
        self.setLayout(self.flashcard_layout)

    def style_card(self) -> None:
        # Style our flashcard to look vaguely real
        self.setFixedSize(600, 400)
        self.setStyleSheet("""
        QFrame {
            background-color: rgb(230, 230, 230);
        }
        """)
        self.flashcard_question.setStyleSheet("color: black; font-size: 18pt;")
        self.flashcard_answer.setStyleSheet("color: black; font-size: 18pt; font-weight: bold;")

    def populate_card(self) -> None:
        # Initialise the question text
        self.flashcard_question = QLabel()
        self.flashcard_question.setWordWrap(True)
        self.flashcard_question.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Create a horizontal line
        self.flashcard_line = QFrame(self)
        self.flashcard_line.setFrameShape(QFrame.Shape.HLine)
        self.flashcard_line.setFrameShadow(QFrame.Shadow.Sunken)

        # Initialise our flashcard's label
        self.flashcard_answer = QLabel()
        self.flashcard_answer.setWordWrap(True)
        self.flashcard_answer.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.flashcard_question_widget = QWidget()
        self.flashcard_question_layout = QVBoxLayout()
        self.flashcard_question_layout.addStretch()
        self.flashcard_question_layout.addWidget(self.flashcard_question)
        self.flashcard_question_layout.addStretch()
        self.flashcard_question_widget.setLayout(self.flashcard_question_layout)

        self.flashcard_answer_widget = QWidget()
        self.flashcard_answer_layout = QVBoxLayout()
        self.flashcard_answer_layout.addStretch()
        self.flashcard_answer_layout.addWidget(self.flashcard_answer)
        self.flashcard_answer_layout.addStretch()
        self.flashcard_answer_widget.setLayout(self.flashcard_answer_layout)

        self.flashcard_indicator = QLabel()
        self.flashcard_indicator.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.flashcard_indicator.setStyleSheet("color: black;")

        # Center our text horizontally
        self.flashcard_layout.addStretch()
        self.flashcard_layout.addWidget(self.flashcard_question_widget)
        self.flashcard_layout.addWidget(self.flashcard_line)
        self.flashcard_layout.addWidget(self.flashcard_answer_widget)
        self.flashcard_layout.addStretch()
        self.flashcard_layout.addWidget(self.flashcard_indicator)

        # Hide our answer first
        self.hide_answer()

    def set_question(self, text) -> None:
        self.flashcard_question.setText(text)

    def set_answer(self, text) -> None:
        self.flashcard_answer.setText(text)

    def set_indicator(self, current_card, total_cards):
        self.flashcard_indicator.setText(current_card + "/" + total_cards)

    def hide_answer(self) -> None:
        self.flashcard_line.hide()
        self.flashcard_answer_widget.hide()

    def show_answer(self) -> None:
        self.flashcard_line.show()
        self.flashcard_answer_widget.show()