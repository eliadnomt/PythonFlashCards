# main.py
"""
Main module for the Flashcards application

Added:
- Fixed bug with multiple choice game where the other three options would repeat
- Modularized code structure
- Added comprehensive error handling and user input validation
- Added type hints throughout
- Separated main application logic into app_controller module

Would still like to add:
- More complex json files, that store notes and images
- Record words which user answered right and wrong in memory
- Make different quizzes into quiz class to cut down on length of functions
- Matching test
- Multitype combined quiz
"""
import glob
import os

from app_controller import get_program_directory, handle_import_functionality, get_valid_deck_choice, load_deck, \
	run_deck_menu
from deck_utils import deck_menu_constructor
from constants import WELCOME


def main() -> None:
	"""Main application controller function."""
	program_directory = get_program_directory()
	print(WELCOME)

	while True:
		try:
			# Find all json files in local directory
			decks = glob.glob(os.path.join(program_directory, "*.json"))
			if not decks:
				print("No deck files found. Please add some .json deck files or use the importer.")
				if not handle_import_functionality(program_directory):
					break
				continue

			deck_choice = get_valid_deck_choice(decks)

			if deck_choice == "i":
				# Handle import functionality
				if not handle_import_functionality(program_directory):
					continue
			else:
				# Load selected deck
				numbered_paths_and_names = deck_menu_constructor(decks)
				deck_file_path = numbered_paths_and_names[int(deck_choice) - 1][2]

				deck = load_deck(deck_file_path)
				if deck is None:
					continue

				# Run the deck menu
				if not run_deck_menu(deck, deck_file_path):
					break  # Exit application

		except KeyboardInterrupt:
			print("\n\nGoodbye!")
			break
		except Exception as e:
			print(f"An unexpected error occurred: {e}")
			continue


if __name__ == "__main__":
    main()
