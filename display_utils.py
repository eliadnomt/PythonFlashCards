"""
Display utilities for formatting and showing flashcards
"""

def grid_builder(cardstr, rowlen=80):
	"""Take a string and make it into a list of items not more than rowlen long"""
	initial_grid = cardstr.split("\n")
	grid = []
	for itm in initial_grid:
		if len(itm) <= rowlen:
			grid.append(itm)
		else:
			to_grid = []
			x = 0
			times_through = 1
			while len(to_grid) < len(itm) // rowlen + 1:
				if len(itm[x:]) > rowlen:
					if itm[x + rowlen - 1].isalpha() and itm[x + rowlen] != " ":
						to_grid.append(itm[x: x + rowlen].lstrip() + "-")
						x += rowlen
					else:
						to_grid.append(itm[x: x + rowlen].lstrip())
						x += rowlen
				else:
					to_grid.append(itm[x:].lstrip())

			for itm2 in to_grid:
				grid.append(itm2)
	return grid


def out_put_builder(grid):
	"""Put lines around strings in a grid"""
	output = ""
	longest_line = 0
	for itm3 in grid:
		if len(itm3) > longest_line:
			longest_line = len(itm3)
	top_line = '\n__' + ('_' * longest_line) + '__\n'
	empty_line = '| ' + (' ' * longest_line) + ' |\n'
	bottom_line = '|_' + ('_' * longest_line) + '_|\n'

	def text_line(column):
		white_space = longest_line - len(grid[column])
		text_lne = '| ' + (grid[column]) + " " * white_space + ' |\n'
		return text_lne

	output += top_line + empty_line
	for row in grid:
		output += text_line(grid.index(row))
	output += bottom_line
	return output

def card_displayer(card):
    """Take a string and put a box graphic around it. Returns a multiline string"""
    return out_put_builder(grid_builder(card))


def display_deck(deck_dict):
    """Display all of the card pairs in the deck, separated by a '-->'."""
    printout = card_displayer("Front") + '   |\n   V' + card_displayer("Back") + '\n'
    for key, value in deck_dict.items():
        printout += card_displayer(key) + '   |\n   V' + card_displayer(value) + "\n"
    return printout
