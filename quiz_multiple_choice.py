"""
Multiple choice quiz functionality
"""
from random import randrange
from display_utils import card_displayer


def multiple_choice_quiz(deck_dict, quiz_direction):
    """
    give a flashcard quiz where quiz taker must type in the correct answer exactly as written on the card

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
    print("\nQuiz --- Multiple Choice\n----------------------------\n")
    # Front to back. Display front of card(key) in prompt, and answer must be its value
    while len(f_b_pairs) > 0:
        # From the tuple list, select a random index,
        random_pair = f_b_pairs[randrange(0, len(f_b_pairs))]
        # list of random card backs/fronts, including one that is the answer
        multi_dict = [" ", " ", " ", " "]
        multi_dict[randrange(0, 4)] = random_pair[back]
        answer = multi_dict.index(random_pair[back])
        # Build the list from the whole deck (to entries that might have been deleted in tuple_pair_list)
        # Generate the random index for where to insert, skip if the same as the answer index
        while multi_dict.count(" ") > 0:
            for pair in deck_dict.items():
                fill_location = randrange(0, 4)
                if pair[back] not in multi_dict:
                    if fill_location != answer and multi_dict[fill_location] == " ":
                        multi_dict[fill_location] = pair[back]
        # The 0th value of the tuple is the card front
        keep_guessing = True
        while keep_guessing:
            guess = input(card_displayer(random_pair[front]) + "\na) " + multi_dict[0] + "\nb) " + multi_dict[1] + "\nc) "
                          + multi_dict[2] + "\nd) " + multi_dict[3] + "\n")
            guess_test = 0
            if guess == "a":
                guess_test = 0
                keep_guessing = False
            elif guess == "b":
                guess_test = 1
                keep_guessing = False
            elif guess == "c":
                guess_test = 2
                keep_guessing = False
            elif guess == "d":
                guess_test = 3
                keep_guessing = False
            else:
                keep_guessing = True
        if guess_test == answer:
            print("Correct!")
            score += 1
            f_b_pairs.remove(random_pair)
            multi_dict = [" ", " ", " ", " "]
        else:
            print(f"Incorrect. The correct answer is：{card_displayer(random_pair[back])}")
            f_b_pairs.remove(random_pair)
            multi_dict = [" ", " ", " ", " "]
    print(f"End of quiz. Your score was {str(round(100 * score / top_score, 2))}%. "
          f"You got {str(score)} out of {str(top_score)} questions correct.")
