import os
import sys
import json
from datetime import datetime

from PySide6.QtWidgets import QApplication
from widgets.main_window import MainWindow

# switch working directory to program location so that data files can be found
os.chdir(os.path.dirname(os.path.realpath(__file__)))

# Initialise our core variables
app: QApplication = None
window: MainWindow = None

# Initialise flashcard variables
flash_cards: dict = {}
card_set: list = []

current_set: str = ""
current_card: int = 0
answer_revealed: bool = False

# Quiz variables
current_question: int = 0
answers: list = []

# Extra variables
date_opened: datetime = datetime.now()

def get_current_set() -> list:
    # Get the global variable, not create one in our scope
    global card_set
    
    # Return it
    return card_set

def get_original_set() -> list:
    # Get the global variable, not create one in our scope
    global flash_cards
    global current_set
    
    # Return it
    return flash_cards[current_set]["cards"]

def create_cards_file():
    # Create the file using the "x" mode
    with open("flashcards.json", "x") as file:
        global flash_cards
        json.dump(flash_cards, file)
        
def load_cards() -> None:
    # Check that flashcards.json has been made
    if os.path.isfile("flashcards.json") is not True:
        create_cards_file()
    
    # open the file on read only mode
    with open("flashcards.json", "r") as file:
        global flash_cards
        flash_cards = json.load(file)

def save_cards() -> None:
    # The file should be created before this function is called,
    # however we dont want to make any assumptions
    # so check that the file actually exists
    if os.path.isfile("flashcards.json") is not True:
        create_cards_file()

    # Open using the "w" mode so we overwrite existing data
    with open("flashcards.json", "w") as file:
        global flash_cards
        json.dump(flash_cards, file)

def create_card_listings() -> None:
    # Add all our card sets to the home page
    for key, value in flash_cards.items():
        window.add_card_set_to_home(key, len(value["cards"]), value["creation_date"])

def create_flash_card(question, answer) -> int:
    # Create a unique ID for the card
    card_set: list = get_current_set()
    card_set.append({
        "question": question, 
        "answer": answer
    })

    return len(card_set)

def copy_current_card_set() -> None:
    # Copy our list of cards into a seperate variable so we can manipulate it
    # and not change the original set contents

    global flash_cards
    global current_set
    global card_set
    
    card_set = flash_cards[current_set]["cards"].copy()

def display_current_card() -> None:
    # Show the current card's question on the flash card
    card_set = get_current_set()
    card = card_set[current_card]
    window.flash_card.set_question(card["question"])
    window.flash_card.set_answer(card["answer"])
    window.flash_card.set_indicator(str(current_card + 1), str(len(card_set)))

def display_current_question() -> None:
    # Reuse the card's question for our quiz
    card_set = get_current_set()
    card = card_set[current_question]
    window.set_quiz_question(card["question"])
    window.set_quiz_indicator(str(current_question + 1), str(len(card_set)))

def start_quiz() -> None:
    # Switch page and display the current question
    window.switch_page("quiz")
    display_current_question()

def switch_to_quiz() -> bool:
    # Ask the user to start the quiz
    if window.ask_question("Are you ready to start the quiz?"):
        start_quiz()
        return True
    else:
        # Return status so we can restart the flashcards if needed
        return False

def increment_card() -> None:
    # Fetch the global variable
    global current_card

    # If the current card is more than the length of flashcards,
    # start the quiz
    card_set = get_current_set()
    if current_card + 1 < len(card_set):
        current_card += 1
        display_current_card()
    else:
        switched = switch_to_quiz()
        # If not switched, restart the flashcards
        if not switched:
            current_card = 0
            display_current_card()

def mark_quiz() -> tuple[int, list]:
    # Mark the quiz responses, returning percentage correct 
    # & list of questions answered incorrectly
    global answers
    global card_set
    correct_answers = 0
    incorrect_questions = []
    for index, answer in enumerate(answers):
        correct_answer: str = card_set[index]["answer"]
        print(correct_answer.lower().strip(), answer.lower().strip())
        if correct_answer.lower().strip() == answer.lower().strip():
            print("You smart nigga")
            correct_answers += 1
        else:
            print("You dumb nigga")
            incorrect_questions.append(card_set[index])

    percentage = correct_answers / len(card_set)
    print(percentage, correct_answers, incorrect_questions)

    return round(percentage * 100), incorrect_questions

def display_mark() -> None:
    global card_set

    window.switch_page("mark")
    percent_correct, incorrect_questions = mark_quiz()
    window.set_quiz_mark(percent_correct, "You migth be retarded")
    card_set = incorrect_questions
    answers.clear()

def next_question() -> None:
    global answers
    global current_question

    card_set = get_current_set()

    if current_question + 1 < len(card_set):
        current_question += 1
        display_current_question()
        window.answer_field.setFocus()
    else:
        # placeholder, go to mark page
        display_mark()

def handle_card_open(item):
    global card_set
    global current_set
    
    for set_name, set_item in window.set_items.items():
        if set_item == item:
            current_set = set_name

            # Copy our list of cards into a seperate variable so we can manipulate it
            card_set = flash_cards[current_set]["cards"].copy()
            break

    window.card_set_list.clearSelection()
    
    display_current_card()
    window.switch_page("card")

def handle_quit_button():
    global current_card
    global current_question
    if window.ask_question("End your session? You will lose all current progress."):
        current_card = 0
        current_question = 0
        window.switch_page("home")

def handle_new_card_button():
    print('new')
    window.switch_page("add")

def handle_next_button():
    global answer_revealed
    if answer_revealed:
        increment_card()
        window.flash_card.hide_answer()
        window.next_button.setText("Reveal")
        window.switch_next_button_icon("flip")
        answer_revealed = False
    else:
        window.flash_card.show_answer()
        window.next_button.setText("Next")
        window.switch_next_button_icon("next")
        answer_revealed = True

def handle_previous_button():
    window.flash_card.hide_answer()
    global current_card
    if current_card - 1 >= 0:
        current_card -= 1
        display_current_card()

def handle_revise_button():
    global current_card
    global current_question

    if get_current_set() is []:
        if window.ask_question("You've correctly answered all of your cards. Restart them again?"):
            # Reload the original set
            load_cards()
            window.switch_page("card")
            current_card = 0
            current_question = 0
            display_current_card()
        return

    if window.ask_question("End the quiz and go back to revising? You will lose all current progress."):
        window.switch_page("card")
        current_card = 0
        current_question = 0
        display_current_card()

def handle_answer_button():
    # Check if text is valid
    if window.answer_field.text():
        answers.append(window.answer_field.text())
        window.answer_field.clear()
        next_question()

def set_greeting():
    hour = date_opened.hour
    time = ""
    
    if hour < 12:
        time = "Morning"
    elif hour < 17:
        time = "Afternoon"
    else:
        time = "Evening"

    window.set_greeting_text("Good " + time)

def connect_all_buttons() -> None:
    # Connect events to a function
    window.card_set_list.itemClicked.connect(handle_card_open)
    window.create_set.pressed.connect(handle_new_card_button)
    window.quit_button.pressed.connect(handle_quit_button)
    window.quit_button_2.pressed.connect(handle_quit_button)
    window.quit_button_3.pressed.connect(handle_quit_button)
    window.add_card_back_button.pressed.connect(handle_quit_button)
    window.next_button.pressed.connect(handle_next_button)
    window.previous_button.pressed.connect(handle_previous_button)
    window.quiz_button.pressed.connect(switch_to_quiz)
    window.revise_button.pressed.connect(handle_revise_button)
    window.revise_button_2.pressed.connect(handle_revise_button)
    window.answer_button.pressed.connect(handle_answer_button)

def main() -> int:
    # Get the global variable rather than creating in the scope
    global app
    global window

    # Create and show our application's window
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    load_cards()
    connect_all_buttons()
    create_card_listings()
    set_greeting()
    #display_current_card()

    # Once complete, pass the exit code provided by the QApplication
    return app.exec()

# Check if the user is executing, not importing the module
if __name__ == "__main__":
    sys.exit(main())