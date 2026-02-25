import sys
import uuid

from PySide6.QtWidgets import QApplication
from widgets.main_window import MainWindow

# Initialise our variables
flash_cards: dict = {}
current_card: int = 0
window: MainWindow = None

def create_flash_card(question, answer) -> str:
    # Create a unique ID for the card
    card_id: str = uuid.uuid4() # Version 4 UUID
    flash_cards[card_id] = {
        "question": question, 
        "answer": answer
    }
    return card_id

def get_card_by_index(index) -> dict:
    # Get the card entry by it's index instead of the ID
    card_keys: list = list(flash_cards.keys())
    return flash_cards[card_keys[index]]

def display_current_card() -> None:
    window.flash_card.

def increment_card() -> None:
    current_card += 1
    display_current_card()

def main() -> int:
    # Create and show our application's window
    app: QApplication = QApplication(sys.argv)
    window: MainWindow = MainWindow()
    window.show()

    # Pass the exit code provided by the QApplication
    return app.exec()

# Check if the user is executing, not importing the module
if __name__ == "__main__":
    sys.exit(main())