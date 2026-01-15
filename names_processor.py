import helper

MAIN_NAME_IND = 0
NICKNAMES_IND = 1

STRING_PUNCTUATION = "!”#$%&'()*+,-./:;<=>?@[\]^_`{|}~\""
STRING_QUOTAS = '"'

class NameProcessor:
    def __init__(self, names: list[str], unwanted_words:set[str] = set()):
        self.names_lines_as_joined_string = names
        self.unwanted_words = unwanted_words
        self.processed_names : list[list[list[str]]] = []
    


    def seperate_names_and_nicknames_to_words(self) -> list[list[list[str]]]:
        """
        Separates names and nicknames into individual words.
        This method processes each line of a CSV file containing character names and nicknames, where the main name and nicknames are separated by commas. It splits each name and nickname into individual words and stores them in a nested list structure. The first part of the list contains the main name, and the second part contains the nicknames.
        """
        
        all_parted_names_and_nicknames = []

        # Parse each line of the names csv file, which was joined to single string
        # Example for those lines:
        # Line 1: "Main Name,"
        # Line 2: "Main Name, First Nickname,Last Nickname "

        for csv_line_of_character_names in self.names_lines_as_joined_string:
            # Split by commas to get all character names
            all_character_names = csv_line_of_character_names.split(',')

            # Strip each name and store in a list
            stripped_character_names = []
            for character_name in all_character_names:
                stripped_character_names.append(character_name.strip())
            
            character_main_name_parts = stripped_character_names[0].split()  # Split the main name into separate words
            
            # Extract the nicknames list (if such exists)
            all_character_nicknames_parts_list = [] 

            if len(stripped_character_names) > 1:
                # Nicknames is a sub-list of all names list, starting after the main name index
                nicknames_list = stripped_character_names[1:]
                if nicknames_list != ['']:
                    
                    # Process each nickname into a list of words
                    for nickname in nicknames_list:
                        nickname_stripped_parts = nickname.strip().split()
                        all_character_nicknames_parts_list.append(nickname_stripped_parts)
            
            # Append the formatted result for this entry
            all_parted_names_and_nicknames.append([character_main_name_parts, all_character_nicknames_parts_list])
        
        self.processed_names = all_parted_names_and_nicknames
    


    def remove_repeating_white_spaces_from_string(self, string: str) -> str:
        """
        Removes repeating whitespaces from a string.
        """
        return ' '.join(string.split())
    


    def lower_name_list(self) -> list[list[list]]:
        """
        Converts all names and nicknames to lowercase.
        Processes each character's main name and nicknames in the 'processed_names' list, converting all words to lowercase. The result is stored back in the 'processed_names' attribute.
        """

        result_list = []

        # Iterate through each character's name and nickname
        for character in self.processed_names:
            first_name_list = character[MAIN_NAME_IND]
            other_names_lists = character[NICKNAMES_IND]

            # Convert the main name and nicknames to lowercase
            lower_first_name_list = helper.lower_list(first_name_list)
            lower_other_names_lists = [helper.lower_list(names_words) for names_words in other_names_lists]
            
            lower_character = [lower_first_name_list, lower_other_names_lists] # Combine lowercase main name and nicknames
            result_list.append(lower_character)

        self.processed_names = result_list
    


    def lower_list(self, word_list: list[str]) -> list[str]:
        """
        Converts a list of words to lowercase.
        """
        return [word.lower() for word in word_list]



    def remove_punctuation_from_name_parts(self, names_parts: list[str]) -> list[str]:
        """
        Removes punctuation from the provided list of name parts and returns a list of cleaned name parts.
        Joins the name parts into a single string, replaces punctuation with spaces, removes repeating whitespace, and then splits the cleaned string back into individual words (name parts).

        Parameters:
        names_parts (list[str]): A list of parts of a name (each word that are in the name is a part).

        Returns:
        list[str]: A list of cleaned name parts with punctuation removed and no extra whitespace.
        """

        full_name = ' '.join(names_parts) # Combine name parts into a single string
        name_with_punctuation_to_whitespaces = self.replace_punctuation_with_whitespace(full_name) # Combine name parts into a single string
        no_whitespaces_dups_name = self.remove_repeating_white_spaces_from_string(name_with_punctuation_to_whitespaces) # Remove repeating whitespace
        return no_whitespaces_dups_name.split(' ') # Split the cleaned name back into individual parts




    def remove_punctuations_from_all_names(self):
        """
        Removes punctuation from all characters names and nicknames.
        """

        no_punctuation_names = []

        # Iterate over each character's names (main name and nicknames)
        for character_names in self.processed_names:

            main_name_parts_list = character_names[MAIN_NAME_IND]
            nicknames_parts_lists = character_names[NICKNAMES_IND]

            # Clean the main name by removing punctuation
            clean_main_name_parts_list = self.remove_punctuation_from_name_parts(main_name_parts_list)
            
            # Clean each nickname by removing punctuation
            clean_nicknames_parts_lists = []
            for nickname_parts_list in nicknames_parts_lists:
                cleaned_nickname_parts_list = self.remove_punctuation_from_name_parts(nickname_parts_list)
                clean_nicknames_parts_lists.append(cleaned_nickname_parts_list)
            
            # Combine the cleaned main name and nicknames into a full character name
            clean_character_full_name = [clean_main_name_parts_list, clean_nicknames_parts_lists]
            no_punctuation_names.append(clean_character_full_name)

        self.processed_names = no_punctuation_names
    



    def replace_punctuation_with_whitespace(self, character_name: str) -> str:
        """
        Replaces punctuation characters in a string with whitespace.
        
        Parameters:
        - character_name (str): The input string (character name) that may contain punctuation.

        Returns:
        - str: A new string with punctuation replaced by spaces, preserving alphanumeric characters and spaces.
        """

        cleaned_name = ''

        # Iterate over each character in the input string
        for char in character_name:
            if char in STRING_PUNCTUATION:
                cleaned_name += ' ' # Replace punctuation with a space
            elif char.isalnum() or char.isspace(): # If the character is alphanumeric or a space
                cleaned_name += char # Keep the character as it is
        return cleaned_name
    

    
    def remove_unwanted_words(self, list_to_clean: list[str]) -> list[str]:
        """
        Removes unwanted words from a list of words.
        """
        return [word for word in list_to_clean if not word in self.unwanted_words]



    def remove_unwanted_words_from_all_names(self) -> list[list[list]]:
        """
        Removes punctuation from all character names and nicknames.
        Processes each character's main name and nicknames in the 'processed_names' list.
        It removes any punctuation from each part of the names and nicknames.
        """

        no_unwanted_words_names = []

        # Iterate over each character's names (main name and nicknames)
        for character_names in self.processed_names:

            main_name_parts_list = character_names[MAIN_NAME_IND]
            nicknames_parts_lists = character_names[NICKNAMES_IND]

            # Clean the main name by removing punctuation
            clean_main_name_parts_list = self.remove_unwanted_words(main_name_parts_list)

            # Clean each nickname by removing punctuation
            clean_nicknames_parts_lists = []
            for nickname_parts_list in nicknames_parts_lists:
                cleaned_nickname_parts_list = self.remove_unwanted_words(nickname_parts_list)
                clean_nicknames_parts_lists.append(cleaned_nickname_parts_list)

            # Combine the cleaned main name and nicknames into a full character name
            clean_character_full_name = [clean_main_name_parts_list, clean_nicknames_parts_lists]
            no_unwanted_words_names.append(clean_character_full_name)

        self.processed_names = no_unwanted_words_names
    


    def remove_duplicate_names(self):
        """
        Removes duplicate character names from the 'processed_names' list.
        """
        results_list = []
        viewed_characters = set() # Set to keep track of the names we've already seen

        # Iterate through each character's name
        for character in self.processed_names:
            first_name = ''.join(character[MAIN_NAME_IND]) # Join the main name parts into a single string
            
            # If the main name has not been seen before, add it to the results list
            if not first_name in viewed_characters:
                viewed_characters.add(first_name)
                results_list.append(character) # Add the character to the results list

        self.processed_names = results_list
    


    def remove_empty_main_names(self):
        """
        Removes characters with empty main names from the 'processed_names' list.
        """

        results_list = []
        
        # Iterate through each character's name
        for character in self.processed_names:
            first_name = ''.join(character[MAIN_NAME_IND])

            # If the main name is not empty, add the character to the results list
            if not len(first_name) == 0:
                results_list.append(character)
                
        self.processed_names = results_list
    

    
    def process_names(self) -> list[list[list[str]]]:
        # Perform the processing steps
        self.seperate_names_and_nicknames_to_words()
        self.lower_name_list()
        self.remove_punctuations_from_all_names()
        self.remove_unwanted_words_from_all_names()
        self.remove_duplicate_names()
        self.remove_empty_main_names()
        return self.processed_names