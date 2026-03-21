from PySide6.QtWidgets import QMainWindow, QWidget, QStackedWidget, QHBoxLayout, QVBoxLayout, QPushButton, QLabel, QLineEdit, QListWidget, QListWidgetItem, QMessageBox
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt, QSize
from widgets.flashcard import Flashcard

class MainWindow(QMainWindow):
    def __init__(self) -> None:
        # Initialise our parent class
        super().__init__()
        self.setMinimumSize(800, 600)

        self.set_items = {}
        self.current_page = "home"

        # Create our central widget and layout
        self.central_widget = QWidget()
        self.central_layout = QHBoxLayout()
        self.setCentralWidget(self.central_widget)

        # Create our stacked widget
        self.widget_page = QStackedWidget()

        # Create card widgets
        self.home_page = QWidget()
        self.home_layout = QHBoxLayout()

        self.edit_page   = QWidget()
        self.edit_layout = QVBoxLayout()

        # Create card widgets
        self.card_page = QWidget()
        self.card_layout = QVBoxLayout()
        
        # Create quiz widgets
        self.quiz_page = QWidget()
        self.quiz_layout = QHBoxLayout()

        # Create mark (results) widgets
        self.mark_page = QWidget()
        self.mark_layout = QHBoxLayout()

        self.pages = {
            "home": self.home_page,
            "card": self.card_page,
            "quiz": self.quiz_page,
            "mark": self.mark_page,
            "edit": self.edit_page
        }

        self.icons = {
            "flip": "./icons/flip.png",
            "next": "./icons/next.png"
        }

        # Add all widgets and stretch objects to layouts
        self.setup_central_widget()
        self.setup_home_page()
        self.setup_edit_page()
        self.setup_card_page()
        self.setup_quiz_page()
        self.setup_mark_page()

        # Assign layouts to our widgets
        self.central_widget.setLayout(self.central_layout)
        self.home_page.setLayout(self.home_layout)
        self.edit_page.setLayout(self.edit_layout)
        self.card_page.setLayout(self.card_layout)
        self.quiz_page.setLayout(self.quiz_layout)
        self.mark_page.setLayout(self.mark_layout)

    def setup_central_widget(self) -> None:
        # Center the main widget horizontally
        self.central_layout.addStretch()
        self.central_layout.addWidget(self.widget_page)
        self.central_layout.addStretch()

    def setup_home_page(self) -> None:
        self.home_content_layout = QVBoxLayout()

        self.welcome_label = QLabel()
        self.welcome_label.setText("Good Morning")
        self.welcome_label.setStyleSheet("font-size: 18pt;")
        self.welcome_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.card_set_list = QListWidget()
        self.card_set_list.setAlternatingRowColors(True)
        self.card_set_list.setFixedSize(500, 400)

        self.button_layout = QHBoxLayout()

        self.create_set = QPushButton()
        self.create_set.setIconSize(QSize(48, 48))
        self.create_set.setIcon(QPixmap("./icons/add.png"))

        self.edit_set = QPushButton()
        self.edit_set.setIconSize(QSize(48, 48))
        self.edit_set.setIcon(QPixmap("./icons/edit.png"))

        self.open_set = QPushButton()
        self.open_set.setIconSize(QSize(48, 48))
        self.open_set.setIcon(QPixmap("./icons/play.png"))
        
        self.button_layout.addStretch()
        self.button_layout.addWidget(self.create_set)
        self.button_layout.addWidget(self.edit_set)
        self.button_layout.addWidget(self.open_set)
        self.button_layout.addStretch()

        self.home_content_layout.addStretch()
        self.home_content_layout.addStretch()
        self.home_content_layout.addWidget(self.welcome_label)
        self.home_content_layout.addStretch()
        self.home_content_layout.addWidget(self.card_set_list)
        self.home_content_layout.addStretch()
        self.home_content_layout.addLayout(self.button_layout)
        self.home_content_layout.addStretch()
        self.home_content_layout.addStretch()

        self.home_layout.addStretch()
        self.home_layout.addLayout(self.home_content_layout)
        self.home_layout.addStretch()

        self.widget_page.addWidget(self.home_page)

    def setup_edit_page(self) -> None:
        self.edit_top_layout = QHBoxLayout()

        self.edit_back_button = QPushButton()
        self.edit_back_button.setText("Back")
        self.edit_back_button.setIconSize(QSize(24, 24))
        self.edit_back_button.setIcon(QPixmap("./icons/return.png"))

        self.edit_delete_button = QPushButton()
        self.edit_delete_button.setText("Delete Set")
        self.edit_delete_button.setIconSize(QSize(24, 24))
        self.edit_delete_button.setIcon(QPixmap("./icons/delete.png"))

        # self.edit_title_label = QLabel()
        # self.edit_title_label.setText("New Card Set")
        # self.edit_title_label.setStyleSheet("font-size: 16pt;")
        # self.edit_title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.edit_top_layout.addWidget(self.edit_back_button)
        #self.edit_top_layout.addWidget(self.edit_title_label)
        self.edit_top_layout.addStretch()
        self.edit_top_layout.addWidget(self.edit_delete_button)

        self.set_name_layout = QHBoxLayout()

        self.set_name_label = QLabel()
        self.set_name_label.setText("Set name:")

        self.set_name_field = QLineEdit()
        self.set_name_field.setPlaceholderText("e.g. Biology Chapter 3")
        self.set_name_field.setFixedHeight(28)

        self.set_name_layout.addWidget(self.set_name_label)
        self.set_name_layout.addWidget(self.set_name_field)

        self.card_entry_layout = QHBoxLayout()

        self.term_field = QLineEdit()
        self.term_field.setPlaceholderText("Term")
        self.term_field.setFixedHeight(28)

        self.definition_field = QLineEdit()
        self.definition_field.setPlaceholderText("Definition")
        self.definition_field.setFixedHeight(28)

        self.add_card_button = QPushButton()
        self.add_card_button.setIconSize(QSize(24, 24))
        self.add_card_button.setFixedSize(28, 28)
        self.add_card_button.setIcon(QPixmap("./icons/add.png"))

        self.card_entry_layout.addWidget(self.term_field)
        self.card_entry_layout.addWidget(self.definition_field)
        self.card_entry_layout.addWidget(self.add_card_button)

        self.added_cards_list = QListWidget()
        self.added_cards_list.setAlternatingRowColors(True)
        self.added_cards_list.setFixedSize(500, 300)

        self.edit_bottom_layout = QHBoxLayout()

        self.remove_card_button = QPushButton()
        self.remove_card_button.setText("Remove Selected Card")
        self.remove_card_button.setIconSize(QSize(24, 24))
        self.remove_card_button.setIcon(QPixmap("./icons/delete.png"))

        self.save_set_button = QPushButton()
        self.save_set_button.setText("Save Set")
        self.save_set_button.setIconSize(QSize(24, 24))
        self.save_set_button.setIcon(QPixmap("./icons/check.png"))

        self.edit_bottom_layout.addStretch()
        self.edit_bottom_layout.addWidget(self.remove_card_button)
        self.edit_bottom_layout.addWidget(self.save_set_button)
        self.edit_bottom_layout.addStretch()

        self.edit_content_layout = QVBoxLayout()

        self.edit_content_layout.addStretch()
        self.edit_content_layout.addLayout(self.edit_top_layout)
        self.edit_content_layout.addStretch()
        self.edit_content_layout.addLayout(self.set_name_layout)
        self.edit_content_layout.addLayout(self.card_entry_layout)
        self.edit_content_layout.addStretch()
        self.edit_content_layout.addWidget(
            self.added_cards_list,
            alignment=Qt.AlignmentFlag.AlignHCenter,
        )
        self.edit_content_layout.addStretch()
        self.edit_content_layout.addLayout(self.edit_bottom_layout)
        self.edit_content_layout.addStretch()

        self.edit_layout.addStretch()
        self.edit_layout.addLayout(self.edit_content_layout)
        self.edit_layout.addStretch()

        self.widget_page.addWidget(self.edit_page)

    def setup_card_page(self) -> None:
        self.flash_card = Flashcard()
        self.top_button_layout = QHBoxLayout()
        self.button_layout = QHBoxLayout()

        self.quit_button = QPushButton()
        self.quit_button.setText("Quit")
        self.quit_button.setIconSize(QSize(24, 24))
        self.quit_button.setIcon(QPixmap("./icons/return.png"))

        self.quiz_button = QPushButton()
        self.quiz_button.setText("Skip to Quiz")
        self.quiz_button.setIconSize(QSize(24, 24))
        self.quiz_button.setIcon(QPixmap("./icons/skip.png"))

        self.previous_button = QPushButton()
        self.previous_button.setText("Previous")
        self.previous_button.setIconSize(QSize(24, 24))
        self.previous_button.setIcon(QPixmap("./icons/back.png"))

        self.next_button = QPushButton()
        self.next_button.setText("Reveal")
        self.next_button.setIconSize(QSize(24, 24))
        self.next_button.setIcon(QPixmap("./icons/flip.png"))

        self.card_label = QLabel()
        
        # Add the top buttons
        self.top_button_layout.addWidget(self.quit_button)
        self.top_button_layout.addStretch()
        self.top_button_layout.addWidget(self.quiz_button)

        # Center the control buttons
        self.button_layout.addStretch()
        self.button_layout.addWidget(self.previous_button)
        self.button_layout.addWidget(self.next_button)
        self.button_layout.addStretch()

        # Center our content vertically
        self.card_layout.addStretch()
        self.card_layout.addLayout(self.top_button_layout)
        self.card_layout.addStretch()
        self.card_layout.addWidget(self.flash_card)
        self.card_layout.addStretch()
        self.card_layout.addLayout(self.button_layout)
        self.card_layout.addStretch()

        self.widget_page.addWidget(self.card_page)

    def setup_quiz_page(self) -> None:
        self.quiz_content_layout = QVBoxLayout()

        self.question_label = QLabel()
        self.question_label.setText("Question")
        self.question_label.setStyleSheet("font-size: 12pt;")

        self.answer_layout = QHBoxLayout()

        self.answer_field = QLineEdit()
        self.answer_field.setPlaceholderText("Type your answer here...")
        self.answer_field.setFixedSize(250, 28)

        self.answer_button = QPushButton()
        self.answer_button.setIconSize(QSize(24, 24))
        self.answer_button.setFixedSize(28, 28)
        self.answer_button.setIcon(QPixmap("./icons/check.png"))

        self.button_layout = QHBoxLayout()

        self.revise_button = QPushButton()
        self.revise_button.setText("Revise")
        self.revise_button.setIconSize(QSize(24, 24))
        self.revise_button.setIcon(QPixmap("./icons/revise.png"))

        self.quit_button_2 = QPushButton()
        self.quit_button_2.setText("Quit")
        self.quit_button_2.setIconSize(QSize(24, 24))
        self.quit_button_2.setIcon(QPixmap("./icons/return.png"))

        self.question_indicator = QLabel()
        self.question_indicator.setText("1/1")
        self.question_indicator.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.answer_layout.addWidget(self.answer_field)
        self.answer_layout.addWidget(self.answer_button)

        self.quiz_layout.addStretch()
        self.quiz_layout.addLayout(self.quiz_content_layout)
        self.quiz_layout.addStretch()

        self.button_layout.addStretch()
        self.button_layout.addWidget(self.revise_button)
        self.button_layout.addWidget(self.quit_button_2)
        self.button_layout.addStretch()

        self.quiz_content_layout.addStretch()
        self.quiz_content_layout.addStretch()
        self.quiz_content_layout.addWidget(self.question_label)
        self.quiz_content_layout.addLayout(self.answer_layout)
        self.quiz_content_layout.addWidget(self.question_indicator)
        self.quiz_content_layout.addStretch()
        self.quiz_content_layout.addLayout(self.button_layout)
        self.quiz_content_layout.addStretch()

        self.widget_page.addWidget(self.quiz_page)
    
    def setup_mark_page(self) -> None:
        # Create the page responsible for displaying marks
        self.mark_content_layout = QVBoxLayout()

        self.mark_title_label = QLabel()
        self.mark_title_label.setText("Your Mark")
        self.mark_title_label.setStyleSheet("font-size: 18pt;")
        self.mark_title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.mark_label = QLabel()
        self.mark_label.setText("100%")
        self.mark_label.setStyleSheet("font-size: 36pt;")
        self.mark_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.mark_message_label = QLabel()
        self.mark_message_label.setText("Great job! You aced your revision")
        self.mark_message_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.button_layout = QHBoxLayout()

        self.revise_button_2 = QPushButton()
        self.revise_button_2.setText("Revise Incorrect")
        self.revise_button_2.setIconSize(QSize(24, 24))
        self.revise_button_2.setIcon(QPixmap("./icons/revise.png"))

        self.quit_button_3 = QPushButton()
        self.quit_button_3.setText("Quit")
        self.quit_button_3.setIconSize(QSize(24, 24))
        self.quit_button_3.setIcon(QPixmap("./icons/return.png"))

        self.button_layout.addWidget(self.revise_button_2)
        self.button_layout.addWidget(self.quit_button_3)
        
        self.mark_content_layout.addStretch()
        self.mark_content_layout.addWidget(self.mark_title_label)
        self.mark_content_layout.addWidget(self.mark_label)
        self.mark_content_layout.addWidget(self.mark_message_label)
        self.mark_content_layout.addStretch()
        self.mark_content_layout.addLayout(self.button_layout)
        self.mark_content_layout.addStretch()

        self.mark_layout.addStretch()
        self.mark_layout.addLayout(self.mark_content_layout)
        self.mark_layout.addStretch()

        self.widget_page.addWidget(self.mark_page)

    def switch_next_button_icon(self, icon) -> None:
        self.next_button.setIcon(QPixmap(self.icons[icon]))

    def switch_page(self, page):
        self.current_page = page
        self.widget_page.setCurrentWidget(self.pages[page])
    
    def add_card_set_to_home(self, name, total_cards, creation_date):
        item = QListWidgetItem()
        item_widget = QWidget()
        item_layout = QVBoxLayout()
        item_layout.setSpacing(4)

        item_name = QLabel()
        item_name.setText(name)

        item_subtitle = QLabel()
        item_subtitle.setStyleSheet("color: rgb(150, 150, 150);")
        item_subtitle.setText(f"{total_cards} cards • Created on {creation_date}")

        item_layout.addWidget(item_name)
        item_layout.addWidget(item_subtitle)
        item_widget.setLayout(item_layout)
        item.setSizeHint(item_widget.sizeHint())

        self.set_items[name] = item

        self.card_set_list.addItem(item)
        self.card_set_list.setItemWidget(item, item_widget)

    def add_card_to_list(self, term: str, definition: str) -> None:
        item = QListWidgetItem()
        item_widget = QWidget()
        item_layout = QVBoxLayout()
        item_layout.setSpacing(4)

        term_label = QLabel()
        term_label.setText(term)

        definition_label = QLabel()
        definition_label.setStyleSheet("color: rgb(150, 150, 150);")
        definition_label.setText(definition)

        item_layout.addWidget(term_label)
        item_layout.addWidget(definition_label)
        item_widget.setLayout(item_layout)
        item.setSizeHint(item_widget.sizeHint())

        self.added_cards_list.addItem(item)
        self.added_cards_list.setItemWidget(item, item_widget)

    def clear_edit_page(self) -> None:
        self.set_name_field.clear()
        self.term_field.clear()
        self.definition_field.clear()
        self.added_cards_list.clear()

    def set_quiz_question(self, question):
        self.question_label.setText(question)

    def set_quiz_indicator(self, current_question, total_questions):
        self.question_indicator.setText(current_question + "/" + total_questions)

    def set_quiz_mark(self, mark, message):
        self.mark_label.setText(str(mark) + "%")
        self.mark_message_label.setText(message)

    def set_greeting_text(self, text):
        self.welcome_label.setText(text)

    def show_dialog(self, text) -> None:
        QMessageBox.information(self, "Information", text)
    
    def ask_question(self, question) -> bool:
        button = QMessageBox.question(self, "Question", question, buttons=QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        return button == QMessageBox.StandardButton.Yes