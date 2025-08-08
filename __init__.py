"""
Flashcards - A Python flashcard application
"""

__version__ = "0.5"
__author__ = "Your Name"

# Import main components if needed
from .import_utils import import_quizlet_lineskip_fix
from .deck_utils import deck_menu_constructor
from display_utils import card_displayer, display_deck
from .quiz_multiple_choice import multiple_choice_quiz
from .quiz_write_answer import write_answer_quiz
from .quiz_self_report import self_report_quiz
from .memory_game import memory_game

__all__ = [
    'import_quizlet_lineskip_fix',
    'deck_menu_constructor',
    'card_displayer',
    'display_deck',
    'multiple_choice_quiz',
    'write_answer_quiz',
    'self_report_quiz',
    'memory_game'
]
