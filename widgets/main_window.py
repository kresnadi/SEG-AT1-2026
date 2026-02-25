from PySide6.QtWidgets import QMainWindow, QWidget, QApplication, QHBoxLayout, QVBoxLayout
from widgets.flashcard import Flashcard

class MainWindow(QMainWindow):
    def __init__(self) -> None:
        # Initialise our parent class
        super().__init__()
        self.setMinimumSize(800, 600)

        # Create our central widget and layout
        self.central_widget = QWidget()
        self.central_layout = QHBoxLayout()
        self.setCentralWidget(self.central_widget)

        # Create the main content widget
        self.card_page = QWidget()
        self.card_layout = QHBoxLayout()

        # Add all widgets and stretch objects to layouts
        self.setup_central_widget()
        self.setup_card_page()

        # Assign layouts to our widgets
        self.central_widget.setLayout(self.central_layout)
        self.card_page.setLayout(self.card_layout)

    def setup_central_widget(self) -> None:
        # Center the main widget horizontally
        self.central_layout.addStretch()
        self.central_layout.addWidget(self.card_page)
        self.central_layout.addStretch()

    def setup_card_page(self) -> None:
        self.flash_card = Flashcard()
        # Center our content vertically
        self.card_layout.addStretch()
        self.card_layout.addWidget(self.flash_card)
        self.card_layout.addStretch()