import sys
import uuid

from PySide6.QtWidgets import QApplication
from widgets.main_window import MainWindow

flash_cards = {}

def create_flash_card(question, answer):
    # Create a unique ID for the card
    card_id = uuid.uuid4() # Version 4 UUID
    flash_cards[card_id] = {
        "question": question, 
        "answer": answer
    }
    return card_id

def main():
    # Create and show our application's window
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    # Pass the exit code provided by the QApplication
    return app.exec()

# Check if the user is executing, not importing the module
if __name__ == "__main__":
    sys.exit(main())