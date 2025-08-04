"""
Memory game functionality
"""
from random import randrange
import math
import copy
from .display_utils import card_displayer

# memory_game.py
"""
Memory game functionality
"""
from random import randrange
import math
import copy
from .display_utils import card_displayer


class MemoryGame:
	"""Class to handle memory game functionality"""

	def __init__(self, deck_dict):
		"""
		Initialize the memory game with a deck of flashcards

		:param deck_dict: a dictionary containing pairs of flashcards
		"""
		self.deck_dict = deck_dict
		self.initial_pairs = [[key, value] for key, value in deck_dict.items()]
		self.f_b_pairs = []
		self.grid = []
		self.rows_count = 0
		self.columns_count = 0
		self.game_round = 0

	def choose_game_length(self):
		"""Allow user to choose how many cards to include in the game"""
		max_cards = len(self.initial_pairs)
		length_chosen = False

		while not length_chosen:
			game_length = input(
				f"Please choose how many cards you'd like to include in the game, between 2 and {min(24, max_cards)}: ")
			if game_length.isdigit():
				game_length_int = int(game_length)
				if 2 <= game_length_int <= min(24, max_cards):
					length_chosen = True
					return game_length_int
				else:
					print(f"Please pick a number between 2 and {min(24, max_cards)}")
			else:
				print("Please enter a valid number")

	def select_cards(self, game_length):
		"""Select random cards from the deck for the game"""
		self.f_b_pairs = []
		available_pairs = copy.deepcopy(self.initial_pairs)

		while len(self.f_b_pairs) < game_length:
			quest_to_add = available_pairs.pop(randrange(len(available_pairs)))
			self.f_b_pairs.append(quest_to_add)

	def calculate_board_size(self, game_length):
		"""Calculate optimal board dimensions"""
		total_cards = game_length * 2
		self.columns_count = math.floor(math.sqrt(total_cards))
		self.rows_count = math.ceil(total_cards / self.columns_count)

	def create_grid(self):
		"""Create and populate the game grid"""
		self.grid = [["0" for _ in range(self.columns_count)] for _ in range(self.rows_count)]

		# Create a list of all cards (each pair appears twice)
		all_cards = []
		for pair in self.f_b_pairs:
			all_cards.extend(pair)

		# Fill grid randomly
		for card in all_cards:
			placed = False
			while not placed:
				target_row = randrange(self.rows_count)
				target_col = randrange(self.columns_count)
				if self.grid[target_row][target_col] == "0":
					self.grid[target_row][target_col] = card
					placed = True

	def get_card_choice(self, prompt, excluded_card=None):
		"""Get a valid card choice from the user"""
		valid_choice = False
		while not valid_choice:
			choice = input(prompt)
			if len(choice) == 2 and choice[0].isdigit() and choice[1].isalpha():
				row = int(choice[0]) - 1
				col = ord(choice[1]) - 97

				if 0 <= row < self.rows_count and 0 <= col < self.columns_count:
					chosen_card = self.grid[row][col]
					if chosen_card != "0" and chosen_card != excluded_card:
						return choice, chosen_card

			print("Invalid choice. Please try again.")

	def check_match(self, card1, card2):
		"""Check if two cards form a matching pair"""
		for pair in self.f_b_pairs:
			if card1 in pair and card2 in pair:
				return True
		return False

	def remove_matched_cards(self, choice1, choice2):
		"""Remove matched cards from the grid"""
		row1, col1 = int(choice1[0]) - 1, ord(choice1[1]) - 97
		row2, col2 = int(choice2[0]) - 1, ord(choice2[1]) - 97
		self.grid[row1][col1] = "0"
		self.grid[row2][col2] = "0"

	def is_game_complete(self):
		"""Check if all cards have been matched"""
		for row in self.grid:
			for card in row:
				if card != "0":
					return False
		return True

	def play(self):
		"""Main game loop"""
		if len(self.initial_pairs) < 2:
			print("Not enough cards in deck to play memory game. Need at least 2 pairs.")
			return

		# Setup game
		game_length = self.choose_game_length()
		self.select_cards(game_length)
		self.calculate_board_size(game_length)
		self.create_grid()

		print("Pick two cards. Try to find the pairs!\nWhen guessing, input row # and column letter")
		print("eg. Row 3, Column b would be '3b'")

		self.game_round = 0

		while not self.is_game_complete():
			self.game_round += 1
			print_grid(self.grid, self.columns_count)

			# Get first card choice
			choice1, card1 = self.get_card_choice("Please pick a card to turn over: ")
			print(card_displayer(card1))

			# Get second card choice
			choice2, card2 = self.get_card_choice("Try to find the match!: ", excluded_card=card1)
			print(card_displayer(card2))

			# Check for match
			if self.check_match(card1, card2):
				print("Congratulations! You found a match!")
				self.remove_matched_cards(choice1, choice2)
			else:
				print("Sorry, please try again.")

		print(f"Congratulations, you won! It took you {self.game_round} rounds.")


def memory_game(deck_dict):
	"""
	Plays a game of 'memory' using the MemoryGame class

	:param deck_dict: a dictionary containing pairs of flashcards
	"""
	game = MemoryGame(deck_dict)
	game.play()


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
