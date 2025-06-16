"""
Memory game functionality
"""
from random import randrange
import math
import copy
from display_utils import card_displayer


def memory_game(deck_dict):
    """
    Plays a game of 'memory'

    :param deck_dict: a dictionary containing pairs of flashcards.
    """
    # Choose cards from deck
    # Converts dict into list of key/value tuples
    initial_pairs0 = [(i for i in pair) for pair in deck_dict.items()]
    initial_pairs = [[i for i in pair] for pair in initial_pairs0]
    # Make user choose quiz length
    length_chosen = False
    while not length_chosen:
        game_length = input("Please choose how many cards you'd like to include in the game, between 5 and 24")
        if game_length.isdigit():
            if 24 >= int(game_length) >= 5 and int(game_length) < len(initial_pairs):
                length_chosen = True
        else:
            print("Please pick again")
    # Add as many questions to the quiz as the user had specified
    f_b_pairs = []
    while len(f_b_pairs) < int(game_length):
        quest_to_add = initial_pairs[randrange(len(initial_pairs))]
        if quest_to_add not in f_b_pairs:
            f_b_pairs.append(quest_to_add)
    # Calculate the board size
    # Columns_count will be width, rows_count height
    columns_count = math.floor(math.sqrt(int(game_length) * 2))
    rows_count = math.ceil((int(game_length) * 2) / columns_count)
    # Because we pop out elements of the list when filling the grid, we need to copy for later reference.
    f_b_pairs1 = copy.deepcopy(f_b_pairs)

    grid = grid_maker(rows_count, columns_count)
    # Fill grid, make sure the target location is empty ("0"), pop the itm and fill till each item in the list is empty
    for itm4 in f_b_pairs:
        while len(itm4) > 0:
            target_row = randrange(rows_count)
            target_col = randrange(columns_count)
            target = grid[target_row][target_col]
            if target == "0":
                grid[target_row][target_col] = itm4.pop()

    # Start the game here
    print("Pick two cards. Try to find the pairs!\nWhen guessing, input row # and column letter"
          "\neg. Row 3, Column b would be '3b' ")
    game_round = 0
    game_over = False
    while not game_over:
        game_round += 1
        print_grid(grid, columns_count)
        # Pick first card
        valid_choice = False
        while not valid_choice:
            choice1 = input("Please pick a card to turn over:   ")
            if choice1[0].isdigit() and choice1[1].isalpha():
                if len(choice1) == 2 and int(choice1[0]) <= rows_count and ord(choice1[1]) < columns_count + 97:
                    choice1_picked = grid[int(choice1[0]) - 1][ord(choice1[1]) - 97]
                    if choice1_picked != "0":
                        valid_choice = True

        print(card_displayer(choice1_picked))
        # Pick second card
        valid_choice2 = False
        while not valid_choice2:
            choice2 = input("Try to find the match!:   ")
            if choice2[0].isdigit() and choice2[1].isalpha():
                if len(choice2) == 2 and int(choice2[0]) <= rows_count and ord(choice2[1]) < columns_count + 97:
                    choice2_picked = grid[int(choice2[0]) - 1][ord(choice2[1]) - 97]
                    if choice2_picked != "0" and choice2_picked != choice1_picked:
                        valid_choice2 = True
        print(card_displayer(choice2_picked))
        is_match = False
        for itm5 in f_b_pairs1:
            if choice1_picked in itm5 and choice2_picked in itm5:
                is_match = True

        if is_match:
            print("Congratulations! You found a match!")
            grid[int(choice1[0]) - 1][ord(choice1[1]) - 97] = "0"
            grid[int(choice2[0]) - 1][ord(choice2[1]) - 97] = "0"
        else:
            print("Sorry, please try again.")

        for row in grid:
            for itm6 in row:
                if itm6 == "0":
                    game_over = True
                else:
                    game_over = False
        if game_over:
            print(f"Congratulations, you won! It took you {str(game_round)} rounds.")

def grid_maker(h, w):
	grid1 = [["0" for i in range(w)] for i in range(h)]
	return grid1


def print_grid(grid2, columns_count):
	y = 0
	print("\n      columns\n      ", end="")
	for i in range(columns_count):
		# 'a' is ord(97), chr(97) is 'a'
		print(chr(97 + y), end="  ")
		y += 1
	print()
	x = 1
	for row1 in grid2:
		print("row " + str(x), end=" ")
		x += 1
		for e in row1:
			# Print a blank if the card is empty, otherwise print a square
			if e == "0":
				print("   ", end="")
			else:
				print("口 ", end="")
		print()
