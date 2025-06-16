"""
Self report quiz functionality
"""
from random import randrange
from display_utils import card_displayer


def self_report_quiz(deck_dict, quiz_direction):
    """
    give a flashcard quiz where quiz taker guesses the word and records him/herself whether the answer was correct.

    :param dict deck_dict: A dictionary of word-definition pairs, must be at least 4 terms long.
    :param str quiz_direction:  "f" for front to back, and "b" for back to front.
    """
    # Converts dict into list of key/value tuples
    initial_pairs = [pair for pair in deck_dict.items()]
    # Make use choose quiz length
    length_chosen = False
    while not length_chosen:
        quiz_length = input("Please choose how many cards you'd like to include in the quiz")
        if int(quiz_length) > 0 and int(quiz_length) < len(initial_pairs):
            length_chosen = True
    # Add as many questions to the quiz as the user had specified
    f_b_pairs = []
    while len(f_b_pairs) < int(quiz_length):
        quest_to_add = initial_pairs[randrange(len(initial_pairs))]
        if quest_to_add not in f_b_pairs:
            f_b_pairs.append(quest_to_add)
    # Cause our default mode is "f" so lets let f's backs and fronts be correct
    front = 0
    back = 1
    # And "b" will be flipped
    if quiz_direction == "b":
        front = 0
        back = 1
    score = 0
    top_score = len(f_b_pairs)
    print("\nQuiz --- Self report\n----------------------------\n")
    # Front to back. Display front of card(key) in prompt, and answer must be its value
    while len(f_b_pairs) > 0:
        # From the tuple list, select a random index, and the 0th value of that (which is the card front)
        random_pair = f_b_pairs[randrange(0, len(f_b_pairs))]
        response = input(card_displayer(random_pair[front]) + "Input any key to show answer:")
        stop = False
        while len(response) >= 0 and not stop:
            correct_or_not = input(f"The answer is: {card_displayer(random_pair[back])} \nDid you guess correctly? "
                                   f"Answer y for yes and n for no: \n")
            if correct_or_not == "y":
                score += 1
                f_b_pairs.remove(random_pair)
                stop = True
            elif correct_or_not == "n":
                f_b_pairs.remove(random_pair)
                stop = True
            else:
                print("Incorrect input.")
    print(f"End of quiz. Your score was {str(round(100 * score / top_score, 2))}%. "
          f"You got {str(score)} out of {str(top_score)} questions correct.")
