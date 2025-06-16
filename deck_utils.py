"""
Deck utilities for managing flashcard decks
"""
import os


def deck_menu_constructor(paths):
    """
    Takes a list of file paths and returns a three part tuple with a label number,
the truncated filename, and the file path.

    :param list paths: a list of file file paths, must be json files containing dictionaries
    :return: a list of three part tuples (number, filename, file path)
    """
    output_list = []
    counter = 1
    for path in paths:
        file_name_w_ext = os.path.basename(path)
        file_name, file_ext = os.path.splitext(file_name_w_ext)
        tup = (counter, file_name, path)
        counter += 1
        output_list.append(tup)
    return output_list
