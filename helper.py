
import json
from itertools import combinations
import csv

SECOND_LINE_START_INDEX = 1

MAIN_NAME = 0
NICKNAMES = 1

PAIR_COMBINATION = 2

STRING_PUNCTUATION = "!”#$%&'()*+,-./:;<=>?@[\]^_`{|}~\""

READ_MODE = 'r'
ENCODING_MODE = 'utf-8'




def parse_csv_to_list_str(file_path_to_csv: str) -> list[str]:
    """
    Reads a CSV file and returns its contents as a list of strings, excluding the header.

    Parameters:
    file_path_to_csv (str): The path to the CSV file to be read.

    Returns:
    list[str]: A list of strings, each representing a line from the CSV file, excluding the header.
    """

    try:
        with open(file_path_to_csv, READ_MODE, encoding=ENCODING_MODE) as file:
            # Read the lines from the file, strip whitespace, and skip the first line (header)
            return [line.strip() for line in file][SECOND_LINE_START_INDEX:]
    except:
        print("invalid input: Failed to open csv file.")
        exit()



def parse_csv_to_set_str(file_path_to_csv: str) -> set[str]:
    """
    Reads a CSV file and returns its contents as a set of strings, excluding the header.

    Parameters:
    file_path_to_csv (str): The path to the CSV file to be read.

    Returns:
    set[str]: A set of unique strings from the CSV file, excluding the header.
    """
    return set(parse_csv_to_list_str(file_path_to_csv))




def lower_list(word_list: list[str]) -> list[str]:
    """
    Converts all strings in a list to lowercase.

    Parameters:
    word_list (list[str]): A list of strings to be converted to lowercase.

    Returns:
    list[str]: A new list with all strings in lowercase.
    """
    return [word.lower() for word in word_list]



def get_combinations_of_two(input_list: list):
    """
    Generates all unique two-element combinations from the input list.

    Parameters:
    input_list (list): A list of elements from which pairs will be generated.

    Returns:
    list[set]: A list of sets, each containing a unique pair of elements from the input list.
    """
    return [set(combo) for combo in combinations(input_list, PAIR_COMBINATION)]



def get_sentences_windows(sentences: list[list[str]], window_size: int):
    """
    Creates sliding windows of sentences from a list of sentences.

    Parameters:
    sentences (list[list[str]]): A list of sentences, where each sentence is represented as a list of words (strings).
    window_size (int): The number of consecutive sentences each window should contain.

    Returns:
    list[list[list[str]]]: A list of sentence windows, where each window is a list of sentences (each sentence is a list of words).
    """

    all_sentences_windows = []
    # Loop through the list of sentences to create consecutive groups
    for i in range(len(sentences) - window_size + 1):
        # Take a slice of the list starting at index 'i' and ending at index 'i + k'
        current_window = sentences[i:i+window_size]
        # Append the group to the result list
        all_sentences_windows.append(current_window)
    return all_sentences_windows

        

def create_names_and_nicknames_dict(processed_names: list[list[list[str]]]) -> dict[str,list[str]]:
    """
    Creates a dictionary mapping main names to a list of corresponding nicknames.

    Parameters:
    processed_names (list[list[list[str]]]): A list of characters' names and nicknames, where each element is a list with the main name and a list of nicknames (each part of the name and nickname is a list of strings).

    Returns:
    dict[str, list[str]]: A dictionary where the keys are main names (strings) and the values are lists of nicknames (strings).
    """
        
    main_name_and_nicknames_dict = {}

    for character_names in processed_names:
        character_main_name_parted = character_names[MAIN_NAME]
        character_nicknames_parted = character_names[NICKNAMES]

        character_main_name = " ".join(character_main_name_parted)
        character_nicknames = []

        for parted_nickname in character_nicknames_parted:
            character_nickname = " ".join(parted_nickname)
            character_nicknames.append(character_nickname)

        main_name_and_nicknames_dict[character_main_name] = character_nicknames
        
    return main_name_and_nicknames_dict


# Sorting Helper Funcs:

# Helper function to sort sentences by length and alphabetically
def sentences_sort_key(sentence):
    return (len(sentence), sentence)


# Helper function to sort groups by number of sentences and alphabetically
def groups_sort_key(group):
    return (len(group), group)


# Helper function to sort groups by amount of sentences
def sort_by_group_size(group):
    return len(group)