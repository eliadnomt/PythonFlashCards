""""
Main module for the Flashcards application

Added:
- Fixed bug with multiple choice game where the other three options would repeat
- Modularized code structure

Would still like to add:
- More complex json files, that store notes and images
- Record words which user answered right and wrong in memory
- Make different quizzes into quiz class to cut down on length of functions
- Matching test
- Multitype combined quiz
"""
import json
import glob
import os

# Import all modules
from import_utils import import_quizlet_lineskip_fix
from deck_utils import deck_menu_constructor
from display_utils import display_deck
from quiz_multiple_choice import multiple_choice_quiz
from quiz_write_answer import write_answer_quiz
from quiz_self_report import self_report_quiz
from memory_game import memory_game
from constants import WELCOME, MENU, TEST_TYPE_PROMPT, FRONT_TO_BACK_PROMPT


def main():
    """Main function to run the flashcard application"""
    try:
        program_directory = os.path.dirname(os.path.abspath(__file__))
    except Exception:
        program_directory = os.getcwd()
    
    print(WELCOME)
    running1 = True
    while running1:
        # Find all json files in local directory, decks will be a list of their paths
        decks = glob.glob(program_directory + "/*.json")
        numbered_paths_and_names = deck_menu_constructor(decks)
        # makes a variable to hold the list of deck names with a given number starting at 1
        decks_choice_display = ""
        for name_path_tup in numbered_paths_and_names:
            decks_choice_display += str(name_path_tup[0]) + ") " + str(name_path_tup[1]) + "\n"
        # Deck choice menu prompt
        deck_chosen = False
        while not deck_chosen:
            deck_choice = input(f"Please choose a deck: \n{decks_choice_display}\nOr type 'i' to skip to deck importer")
            if deck_choice == "i" or int(deck_choice) <= len(decks):
                deck_chosen = True
        running2 = True
        while running2:
            if deck_choice == "i":
                menu_choice = "6"
            else:
                # The number the user enters will be 1 more than the index for the tuple where the path is the 2th entry
                file_to_open = open(numbered_paths_and_names[int(deck_choice) - 1][2], 'r')
                menu_choice = input(MENU)
                deck = json.loads(file_to_open.read())
                file_to_open.close()
            if menu_choice == "1":
                print(f"\nCurrent deck:\n{display_deck(deck)} \n")
            elif menu_choice == "2":
                new_item_front = input("Please type the card front: ")
                new_item_back = input("Please type the card back: ")
                if new_item_front not in deck:
                    deck[new_item_front] = new_item_back
                    print("Added successfully!")
                else:
                    print("Word already in deck")
            elif menu_choice == "3":
                remove = input("Please input the card front you'd like to remove: ")
                if remove in deck:
                    print(f"Removed {remove} ---> {deck[remove]}")
                    del deck[remove]
                else:
                    print("Word not in deck")
            elif menu_choice == "4":
                test_type = True
                while test_type:
                    test_type = input(TEST_TYPE_PROMPT)
                    if test_type == "1":
                        direction = input(FRONT_TO_BACK_PROMPT)
                        if direction == "f" or direction == "b":
                            multiple_choice_quiz(deck, direction)
                            test_type = False
                        else:
                            print("Invalid entry")
                    elif test_type == "2":
                        direction = input(FRONT_TO_BACK_PROMPT)
                        if direction == "f" or direction == "b":
                            write_answer_quiz(deck, direction)
                            test_type = False
                        else:
                            print("Invalid entry")
                    elif test_type == "3":
                        direction = input(FRONT_TO_BACK_PROMPT)
                        if direction == "f" or direction == "b":
                            self_report_quiz(deck, direction)
                            test_type = False
                        else:
                            print("Invalid entry")
                    else:
                        print("Invalid choice")
            elif menu_choice == "5":
                memory_game(deck)
            elif menu_choice == "6":
                # Before switching to a new deck, or when closing the session, write the changes.
                file_to_write = open(numbered_paths_and_names[int(deck_choice) - 1][2], 'w+')
                file_to_write.write(json.dumps(deck, sort_keys=True, indent=4))
                file_to_write.close()
                running2 = False
            elif menu_choice == "7":
                # Find all txt files in local directory, txts variable will be a list of their paths
                txts = glob.glob(program_directory + "/*.txt")
                numbered_paths_and_names1 = deck_menu_constructor(txts)
                # makes a variable to hold the list of file names with a given number starting at 1
                files_choice_display = ""
                for name_path_tup in numbered_paths_and_names1:
                    files_choice_display += str(name_path_tup[0]) + ") " + str(name_path_tup[1]) + "\n"
                # File choice menu prompt
                file_choice = input(f"Please choose a file: \n{files_choice_display}")
                is_quizlet = input("Is the file a Quizlet export or in the Quizlet export format?"
                                   "\nEnter y for yes or n for no: ")
                if is_quizlet == "y":
                    is_default = input("Did you export using the default Quizlet export?\n"
                                       "Separating cards with spaces and card front and backs with tabs?")
                    if is_default == "y":
                        # The number the user enters will be 1 more than the index for the
                        # tuple where the path is the 2th entry
                        if numbered_paths_and_names1[int(file_choice) - 1][2] in program_directory:
                            overwrite = input("File already exists. Overwrite?"
                                              "\nEnter y for yes or n for no: ")
                            if overwrite == "y":
                                print("Importing...")
                                import_quizlet_lineskip_fix(numbered_paths_and_names1[int(file_choice) - 1][2])
                                running2 = False
                        else:
                            print("Importing...")
                            import_quizlet_lineskip_fix(numbered_paths_and_names1[int(file_choice) - 1][2])
                            running2 = False
                    else:
                        ask_fbsep = input("Please input the separator you used between card fronts and backs: ")
                        ask_cardsep = input("Please input the separator you used between cards: ")
                        print("Importing...")
                        import_quizlet_lineskip_fix(numbered_paths_and_names1[int(file_choice) - 1][2],
                                                    fbsep=ask_fbsep, cardsep=ask_cardsep)
                        running2 = False
                else:
                    print("Unsupported file type.")
                    running2 = False
            elif menu_choice == "8":
                print("Thanks for playing, see you next time!")
                # Before switching to a new deck, or when closing the session, write the changes.
                file_to_write = open(numbered_paths_and_names[int(deck_choice) - 1][2], 'w+')
                file_to_write.write(json.dumps(deck, sort_keys=True, indent=4))
                file_to_write.close()
                running1 = False
                running2 = False
            else:
                print("Invalid entry")


if __name__ == "__main__":
    main()
