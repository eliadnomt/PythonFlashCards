# app_controller.py
"""
Application controller module for the Flashcards application.
Contains the main application logic separated into modular functions.
"""
import json
import glob
import os
from typing import Dict, List, Tuple, Optional, Any

# Import all modules
from import_utils import import_quizlet_lineskip_fix
from deck_utils import deck_menu_constructor
from display_utils import display_deck
from quiz_multiple_choice import multiple_choice_quiz
from quiz_write_answer import write_answer_quiz
from quiz_self_report import self_report_quiz
from memory_game import memory_game
from constants import MENU_DECK, MENU_MAIN, MENU_GAME, TEST_TYPE_PROMPT, FRONT_TO_BACK_PROMPT


def get_program_directory() -> str:
	"""Get the program directory path safely."""
	try:
		return os.path.dirname(os.path.abspath(__file__))
	except Exception:
		return os.getcwd()


def get_valid_deck_choice(decks: List[str]) -> str:
	"""
	Get a valid deck choice from the user with proper validation.

	Args:
		decks: List of deck file paths

	Returns:
		User's deck choice as string
	"""
	numbered_paths_and_names = deck_menu_constructor(decks)
	decks_choice_display = ""
	for name_path_tup in numbered_paths_and_names:
		decks_choice_display += f"{name_path_tup[0]}) {name_path_tup[1]}\n"

	while True:
		try:
			deck_choice = input(
				f"Please choose a deck: \n{decks_choice_display}\n"
				f"Or type 'i' to skip to deck importer: "
			).strip()

			if deck_choice.lower() == "i":
				return "i"

			choice_num = int(deck_choice)
			if 1 <= choice_num <= len(decks):
				return deck_choice
			else:
				print(f"Error: Please enter a number between 1 and {len(decks)}, or 'i' for importer.")

		except ValueError:
			print("Error: Please enter a valid number or 'i' for importer.")


def load_deck(file_path: str) -> Optional[Dict[str, str]]:
	"""
	Load a deck from a JSON file with error handling.

	Args:
		file_path: Path to the JSON file

	Returns:
		Dictionary containing the deck data, or None if loading failed
	"""
	try:
		with open(file_path, 'r', encoding='utf-8') as file:
			return json.load(file)
	except FileNotFoundError:
		print(f"Error: File '{file_path}' not found.")
		return None
	except json.JSONDecodeError:
		print(f"Error: Invalid JSON format in file '{file_path}'.")
		return None
	except Exception as e:
		print(f"Error loading deck: {e}")
		return None


def save_deck(deck: Dict[str, str], file_path: str) -> bool:
	"""
	Save a deck to a JSON file with error handling.

	Args:
		deck: Dictionary containing the deck data
		file_path: Path to save the JSON file

	Returns:
		True if successful, False otherwise
	"""
	try:
		with open(file_path, 'w', encoding='utf-8') as file:
			json.dump(deck, file, sort_keys=True, indent=4, ensure_ascii=False)
		return True
	except Exception as e:
		print(f"Error saving deck: {e}")
		return False


def handle_display_deck(deck: Dict[str, str]) -> None:
	"""Handle displaying the current deck."""
	print(f"\nCurrent deck:\n{display_deck(deck)}\n")


def handle_add_card(deck: Dict[str, str]) -> None:
	"""Handle adding a new card to the deck."""
	new_item_front = input("Please type the card front: ").strip()
	if not new_item_front:
		print("Error: Card front cannot be empty.")
		return

	new_item_back = input("Please type the card back: ").strip()
	if not new_item_back:
		print("Error: Card back cannot be empty.")
		return

	if new_item_front not in deck:
		deck[new_item_front] = new_item_back
		print("Card added successfully!")
	else:
		print("Error: Card with this front already exists in deck.")


def handle_remove_card(deck: Dict[str, str]) -> None:
	"""Handle removing a card from the deck."""
	if not deck:
		print("Error: Deck is empty. No cards to remove.")
		return

	remove = input("Please input the card front you'd like to remove: ").strip()
	if not remove:
		print("Error: Please enter a valid card front.")
		return

	if remove in deck:
		print(f"Removed: {remove} --> {deck[remove]}")
		del deck[remove]
	else:
		print("Error: Card not found in deck.")


def get_valid_direction() -> str:
	"""
	Get a valid direction choice from the user.

	Returns:
		'f' for front-to-back or 'b' for back-to-front
	"""
	while True:
		direction = input(FRONT_TO_BACK_PROMPT).strip().lower()
		if direction in ['f', 'b']:
			return direction
		print("Error: Please enter 'f' for front-to-back or 'b' for back-to-front.")


def handle_quiz_selection(deck: Dict[str, str]) -> None:
	"""Handle quiz type selection and execution."""
	if not deck:
		print("Error: Deck is empty. Cannot start quiz.")
		return

	while True:
		try:
			test_type = input(TEST_TYPE_PROMPT).strip()

			if test_type == "1":
				direction = get_valid_direction()
				multiple_choice_quiz(deck, direction)
				break
			elif test_type == "2":
				direction = get_valid_direction()
				write_answer_quiz(deck, direction)
				break
			elif test_type == "3":
				direction = get_valid_direction()
				self_report_quiz(deck, direction)
				break
			else:
				print("Error: Please enter 1, 2, or 3 for quiz type.")

		except KeyboardInterrupt:
			print("\nQuiz cancelled.")
			break


def handle_memory_game(deck: Dict[str, str]) -> None:
	"""Handle memory game execution."""
	if not deck:
		print("Error: Deck is empty. Cannot start memory game.")
		return
	memory_game(deck)


def get_valid_file_choice(files: List[str]) -> int:
	"""
	Get a valid file choice from the user.

	Args:
		files: List of file paths

	Returns:
		Valid file choice index
	"""
	numbered_paths_and_names = deck_menu_constructor(files)
	files_choice_display = ""
	for name_path_tup in numbered_paths_and_names:
		files_choice_display += f"{name_path_tup[0]}) {name_path_tup[1]}\n"

	while True:
		try:
			file_choice = input(f"Please choose a file: \n{files_choice_display}").strip()
			choice_num = int(file_choice)
			if 1 <= choice_num <= len(files):
				return choice_num - 1  # Return 0-based index
			else:
				print(f"Error: Please enter a number between 1 and {len(files)}.")
		except ValueError:
			print("Error: Please enter a valid number.")


def get_yes_no_input(prompt: str) -> bool:
	"""
	Get a yes/no input from the user with validation.

	Args:
		prompt: The prompt to display to the user

	Returns:
		True for yes, False for no
	"""
	while True:
		response = input(f"{prompt}\nEnter y for yes or n for no: ").strip().lower()
		if response in ['y', 'yes']:
			return True
		elif response in ['n', 'no']:
			return False
		else:
			print("Error: Please enter 'y' for yes or 'n' for no.")


def handle_import_functionality(program_directory: str) -> bool:
	"""
	Handle the import functionality for text files.

	Args:
		program_directory: The program directory path

	Returns:
		True if import was successful and should exit menu, False otherwise
	"""
	txts = glob.glob(os.path.join(program_directory, "*.txt"))
	if not txts:
		print("Error: No .txt files found in the current directory.")
		return False

	try:
		file_index = get_valid_file_choice(txts)
		numbered_paths_and_names = deck_menu_constructor(txts)
		selected_file_path = numbered_paths_and_names[file_index][2]

		is_quizlet = get_yes_no_input("Is the file a Quizlet export or in the Quizlet export format?")

		if is_quizlet:
			is_default = get_yes_no_input(
				"Did you export using the default Quizlet export?\n"
				"Separating cards with spaces and card front and backs with tabs?"
			)

			# Check if file already exists as JSON
			json_path = selected_file_path.replace('.txt', '.json')
			if os.path.exists(json_path):
				overwrite = get_yes_no_input("JSON file already exists. Overwrite?")
				if not overwrite:
					print("Import cancelled.")
					return False

			print("Importing...")
			if is_default:
				import_quizlet_lineskip_fix(selected_file_path)
			else:
				fbsep = input("Please input the separator you used between card fronts and backs: ").strip()
				cardsep = input("Please input the separator you used between cards: ").strip()
				if not fbsep or not cardsep:
					print("Error: Separators cannot be empty.")
					return False
				import_quizlet_lineskip_fix(selected_file_path, fbsep=fbsep, cardsep=cardsep)

			print("Import completed successfully!")
			return True
		else:
			print("Error: Unsupported file type. Only Quizlet exports are currently supported.")
			return False

	except Exception as e:
		print(f"Error during import: {e}")
		return False


def run_main_menu(deck: Dict[str, str], deck_file_path: str) -> bool:
	"""
	Run the main deck menu loop.

	Args:
		deck: The current deck dictionary
		deck_file_path: Path to the deck file

	Returns:
		True to continue with main loop, False to exit application
	"""

	while True:
		try:
			menu_choice = input(MENU_MAIN).strip()

			if menu_choice == "1":
				run_deck_menu(deck, deck_file_path)
				return False
			elif menu_choice == "2":
				run_game_menu(deck, deck_file_path)
				return False
			elif menu_choice == "3":
				# Exit application
				print("Thanks for playing, see you next time!")
				save_deck(deck, deck_file_path)
				return False
			else:
				print("Error: Invalid menu choice. Please enter a number between 1 and 3.")

		except KeyboardInterrupt:
			print("\n\nExiting application...")
			save_deck(deck, deck_file_path)
			return False
		except Exception as e:
			print(f"An unexpected error occurred: {e}")


def run_deck_menu(deck: Dict[str, str], deck_file_path: str) -> bool:
	"""
	Run the deck management menu loop.

	Args:
		deck: The current deck dictionary
		deck_file_path: Path to the deck file

	Returns:
		True to continue with main loop, False to return to main menu
	"""
	program_directory = get_program_directory()

	while True:
		try:
			menu_choice = input(MENU_DECK).strip()

			if menu_choice == "1":
				handle_display_deck(deck)
			elif menu_choice == "2":
				handle_add_card(deck)
			elif menu_choice == "3":
				handle_remove_card(deck)
			elif menu_choice == "4":
				# Save and return to deck selection
				if save_deck(deck, deck_file_path):
					print("Deck saved successfully!")
				return True
			elif menu_choice == "5":
				# Import functionality
				if handle_import_functionality(program_directory):
					return True  # Return to deck selection after successful import
			elif menu_choice == "6":
				run_main_menu(deck, deck_file_path)
				return False
			else:
				print("Error: Invalid menu choice. Please enter a number between 1 and 6.")

		except KeyboardInterrupt:
			print("\n\nExiting application...")
			save_deck(deck, deck_file_path)
			return False
		except Exception as e:
			print(f"An unexpected error occurred: {e}")


def run_game_menu(deck: Dict[str, str], deck_file_path: str) -> bool:
	"""
	Run the game menu loop.

	Args:
		deck: The current deck dictionary
		deck_file_path: Path to the deck file

	Returns:
		True to continue with main loop, False to exit application
	"""

	while True:
		try:
			menu_choice = input(MENU_GAME).strip()

			if menu_choice == "1":
				handle_quiz_selection(deck)
			elif menu_choice == "2":
				handle_memory_game(deck)
			elif menu_choice == "3":
				run_main_menu(deck, deck_file_path)
				return False
			else:
				print("Error: Invalid menu choice. Please enter a number between 1 and 3.")

		except KeyboardInterrupt:
			print("\n\nExiting application...")
			save_deck(deck, deck_file_path)
			return False
		except Exception as e:
			print(f"An unexpected error occurred: {e}")
