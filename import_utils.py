"""
Import utilities for converting flashcard files
"""
import json
import os


def import_quizlet_lineskip_fix(filepath, fbsep="\t", cardsep="\n"):
    """
    Take a Quizlet flashcard export either that by default uses tab for card front and back,
and linebreak for new card, or a custom export that uses custom characters to separate.

If a line doesnt have a tab, join with a "\n" to the line before it.

write a new file to same directory, using the same filename but changing the extension to .json

    :param str filepath: File path of file to be converted, must be a .txt file
    :param str fbsep: Separation value between front and back of card, default is tab "\t.
    :param str cardsep: Separation value between card and card, default is linebreak "\n".
    :return dict: converted dictionary.
    """
    with open(filepath) as fileobj:
        data0 = fileobj.readlines()
    # First combine all lines into a long string.
    data1 = ""
    for line1 in data0:
        data1 += line1
    # Then split by the cardsep
    data3 = data1.split(cardsep)
    # For default setting, we must rejoin the lines that were separated by a linebreak
    if cardsep == "\n":
        clean_counter = 0
        while clean_counter < len(data3):
            clean_counter = 0
            for itm0 in data3:
                if fbsep not in itm0:
                    data3[data3.index(itm0)-1] += "\n" + data3.pop(data3.index(itm0))
                    break
                elif fbsep in itm0:
                    clean_counter += 1
    # Then cull entries with too many fbsep's
    for itm1 in data3:
        if itm1.count(fbsep) > 1:
            # Reverse replace method
            data3[data3.index(itm1)] = "\n".join(itm1.rsplit(fbsep, 1))
    # Then separate by fbsep, culling trailing punctuation on the way
    data4 = []
    for itm2 in data3:
        if itm2 != "" and itm2 != "\n" and itm2 != "":
            data4.append(itm2.split(fbsep))
    # Then clean out wrong sized items, making sure our list of paired strings lists are all len(2) pairs
    data5 = []
    for itm3 in data4:
        if len(itm3) != 2:
            print(f"Item: '{itm3}' was not included in the deck.")
        else:
            data5.append(itm3)
    # Finally make the dictionary
    data6 = dict(data5)
    # Write the dictionary to a new file with the same name, but a .json extension
    write_file_path = os.path.splitext(filepath)[0] + ".json"
    write_to_file = open(write_file_path, 'w+')
    write_to_file.write(json.dumps(data6, sort_keys=True, indent=4))
    write_to_file.close()
    return data6
