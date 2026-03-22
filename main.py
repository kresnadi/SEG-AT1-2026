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

# Modify card page variables
new_cards: list = []
editing_set: str = ""

# Extra variables
date_opened: datetime = datetime.now()

def get_current_set() -> list:
    # Get the global current set
    # This set could've been modified by the program

    global card_set
    return card_set

def get_original_set() -> list:
    # Get the original card set that had not been modified
    global flash_cards
    global current_set
    
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

def create_flash_card(question, answer) -> None:
    # Create a unique ID for the card
    card_set: list = get_original_set()
    card_set.append({
        "question": question, 
        "answer": answer
    })

def copy_current_card_set() -> None:
    # Copy our list of cards into a seperate variable so we can manipulate it
    # and not change the original set contents
    global card_set
    
    card_set = get_original_set().copy()

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
    
    # Reset our variables
    global current_question
    global answers

    current_question = 0
    answers = []

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

    # Loop through answers
    for index, answer in enumerate(answers):
        # Get the correct answer
        correct_answer: str = card_set[index]["answer"]

        # We'll get the user's answer and the correct answer in lowercase
        # so that it's not case sensitive.
        # We also want to remove leading and trailing spaces
        if correct_answer.lower().strip() == answer.lower().strip():
            correct_answers += 1
        else:
            incorrect_questions.append(card_set[index])

    # Get the percentage correct
    percentage = round(correct_answers / len(card_set) * 100)

    # Return percentage and incorrect questions as a list of cards
    return percentage, incorrect_questions

def get_mark_message(percentage: int) -> str:
    if percentage == 100:
        return "Perfect score! Congratulations"
    elif percentage > 80:
        return "Well done! You know your stuff"
    elif percentage > 60:
        return "Good job, but there's room to improve!"
    elif percentage > 40:
        return "Great attempt, but we're only just starting!"
    else:
        return "Don't be discouraged! Keep practicing!"

def display_mark() -> None:
    global card_set

    # Display our mark onto the GUI
    window.switch_page("mark")
    percent_correct, incorrect_questions = mark_quiz()
    window.set_quiz_mark(percent_correct, get_mark_message(percent_correct))
    
    # Fill our card_set value with only cards the user got incorrect
    card_set = incorrect_questions

    # Clear our user's answers
    answers.clear()

def next_question() -> None:
    global answers
    global current_question

    card_set = get_current_set()

    # Increment our question value, then update the question on the GUI
    if current_question + 1 < len(card_set):
        current_question += 1
        display_current_question()

        # Automatically grab the user's keyboard onto the answer field
        window.answer_field.setFocus()
    else:
        display_mark()

def handle_card_open():
    global card_set
    global current_set
    global current_card
    global current_question
    global answer_revealed

    # Reset all our card variables first

    current_card = 0
    current_question = 0
    answer_revealed = False
    window.flash_card.hide_answer()
    window.switch_next_button_icon("flip")

    item = window.card_set_list.currentItem()
    
    # Loop through all list widgets items to find the one that got clicked
    # We're searching for the key associated with the list item
    for set_name, set_item in window.set_items.items():
        if set_item == item:
            # Set the current set 
            current_set = set_name

            # Copy our list of cards into a seperate variable so we can manipulate it
            # without modifying the original set
            card_set = flash_cards[current_set]["cards"].copy()
            break

    window.card_set_list.clearSelection()
    
    display_current_card()
    window.switch_page("card")

def handle_quit_button():
    # Ask the user if they really want to exit
    if window.ask_question("End your session? You will lose all current progress."):
        # Return home
        window.switch_page("home")

def handle_new_card_button():
    global new_cards
    global editing_set

    # Clear new cards
    new_cards = []

    # When editing_set is empty, we indicate that we're creating a new set
    editing_set = ""
    
    window.clear_edit_page()
    window.switch_page("edit")
 
def handle_edit_card_button():
    global new_cards
    global editing_set
    global flash_cards
 
    # A set must be selected to edit
    selected_item = window.card_set_list.currentItem()
    if selected_item is None:
        window.show_dialog("Please select a card set to edit.")
        return
 
    # Find the set name from the selected item
    selected_set = ""
    for set_name, set_item in window.set_items.items():
        if set_item == selected_item:
            selected_set = set_name
            break
 
    if not selected_set:
        return
 
    # Load the existing cards into new_cards and populate the UI list
    editing_set = selected_set
    existing_cards = flash_cards[selected_set]["cards"]
    new_cards = [card.copy() for card in existing_cards]
 
    window.clear_edit_page()
    #window.set_add_card_page_edit_mode(selected_set)
    window.set_name_field.setText(selected_set)
 
    for card in new_cards:
        window.add_card_to_list(card["question"], card["answer"])
 
    window.card_set_list.clearSelection()
    window.switch_page("edit")
 
def handle_edit_card_back_button():
    global new_cards
    global editing_set
    if new_cards:
        if not window.ask_question("Go back? You will lose your unsaved changes."):
            return
    new_cards = []
    editing_set = ""
    window.clear_edit_page()
    window.switch_page("home")

def handle_delete_card_set_button():
    global flash_cards
    global new_cards
    global editing_set

    # Can't delete if we're creating a new set (nothing saved yet)
    if not editing_set:
        window.show_dialog("There is no saved set to delete.")
        return

    if not window.ask_question(f'Are you sure you want to delete "{editing_set}"? This cannot be undone.'):
        return

    # Remove from flash_cards dict and save
    del flash_cards[editing_set]
    save_cards()

    # Remove the entry from the home page list
    if editing_set in window.set_items:
        old_item = window.set_items.pop(editing_set)
        row = window.card_set_list.row(old_item)
        window.card_set_list.takeItem(row)

    # Reset and return home
    new_cards = []
    editing_set = ""
    window.clear_edit_page()
    window.switch_page("home")
 
def handle_add_card_button():
    term = window.term_field.text().strip()
    definition = window.definition_field.text().strip()
 
    if not term or not definition:
        window.show_dialog("Please enter both a term and a definition.")
        return
 
    global new_cards
    new_cards.append({"question": term, "answer": definition})
    window.add_card_to_list(term, definition)
 
    window.term_field.clear()
    window.definition_field.clear()
    window.term_field.setFocus()
 
def handle_remove_card_button():
    selected = window.added_cards_list.currentRow()
    if selected == -1:
        window.show_dialog("Please select a card to remove.")
        return
 
    global new_cards
    new_cards.pop(selected)
    window.added_cards_list.takeItem(selected)
 
def handle_save_set_button():
    global flash_cards
    global new_cards
    global editing_set
 
    set_name = window.set_name_field.text().strip()
 
    if not set_name:
        window.show_dialog("Please enter a name for your card set.")
        return
 
    if not new_cards:
        window.show_dialog("Please add at least one card before saving.")
        return
 
    # When creating a new set, warn before overwriting an existing one
    # When editing, set_name is locked to the original name so this won't trigger
    if not editing_set and set_name in flash_cards:
        if not window.ask_question(f'A set named "{set_name}" already exists. Overwrite it?'):
            return
 
    # Preserve the original creation date when editing; use today when creating
    if editing_set:
        creation_date = flash_cards[editing_set]["creation_date"]
    else:
        creation_date = datetime.now().strftime("%d/%m/%Y")
 
    flash_cards[set_name] = {
        "creation_date": creation_date,
        "cards": new_cards.copy()
    }
    save_cards()
 
    # Refresh the home page list entry
    if set_name in window.set_items:
        old_item = window.set_items.pop(set_name)
        row = window.card_set_list.row(old_item)
        window.card_set_list.takeItem(row)
 
    window.add_card_set_to_home(set_name, len(new_cards), creation_date)
 
    # Reset and return home
    new_cards = []
    editing_set = ""
    window.clear_edit_page()
    window.switch_page("home")
    
def handle_next_button():
    # Check if the answer is revealed
    global answer_revealed
    if answer_revealed:
        # Increment card, and revert the button's text
        increment_card()
        window.flash_card.hide_answer()
        window.next_button.setText("Reveal")
        window.switch_next_button_icon("flip")
        answer_revealed = False
    else:
        # Reveal our answer and change the button's text
        window.flash_card.show_answer()
        window.next_button.setText("Next")
        window.switch_next_button_icon("next")
        answer_revealed = True

def handle_previous_button():
    # Hide the answer and decrease our current card value
    window.flash_card.hide_answer()
    global current_card
    if current_card - 1 >= 0:
        current_card -= 1
        display_current_card()

def handle_revise_button():
    global current_card
    global current_question

    # Check if there are no more cards left
    if get_current_set() is []:
        if window.ask_question("You've correctly answered all of your cards. Restart them again?"):
            # Reload the original set
            load_cards()
            window.switch_page("card")
            current_card = 0
            current_question = 0
            display_current_card()
        return

    # We proceed here if there are still cards left
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
    # Check the hour, and set the greeting text accordingly
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
    # Home page
    window.create_set.pressed.connect(handle_new_card_button)
    window.edit_set.pressed.connect(handle_edit_card_button)
    window.open_set.pressed.connect(handle_card_open)
 
    # Add card page
    window.edit_back_button.pressed.connect(handle_edit_card_back_button)
    window.edit_delete_button.pressed.connect(handle_delete_card_set_button)
    window.add_card_button.pressed.connect(handle_add_card_button)
    window.remove_card_button.pressed.connect(handle_remove_card_button)
    window.save_set_button.pressed.connect(handle_save_set_button)
    # Allow pressing Enter in the definition field to add the card
    window.definition_field.returnPressed.connect(handle_add_card_button)
    window.term_field.returnPressed.connect(lambda: window.definition_field.setFocus())
 
    # Card page
    window.quit_button.pressed.connect(handle_quit_button)
    window.next_button.pressed.connect(handle_next_button)
    window.previous_button.pressed.connect(handle_previous_button)
    window.quiz_button.pressed.connect(switch_to_quiz)
 
    # Quiz page
    window.quit_button_2.pressed.connect(handle_quit_button)
    window.revise_button.pressed.connect(handle_revise_button)
    window.answer_button.pressed.connect(handle_answer_button)
    window.answer_field.returnPressed.connect(handle_answer_button)
 
    # Mark page
    window.quit_button_3.pressed.connect(handle_quit_button)
    window.revise_button_2.pressed.connect(handle_revise_button)

def main() -> int:
    # Get the global variable rather than creating in the scope
    global app
    global window

    # Create and show our application's window
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = MainWindow()
    window.show()

    # Initialise our flash cards from the flashcard.json file
    load_cards()

    # Initialise GUI
    connect_all_buttons()

    # Loop through card sets and display them
    create_card_listings()

    # Update our greeting message
    set_greeting()

    # Once complete, pass the exit code provided by the QApplication
    return app.exec()

# Check if the user is executing, not importing the module
if __name__ == "__main__":
    # Run the main function, quitting the program with the exit code provided
    exit_code = main()
    sys.exit(exit_code)