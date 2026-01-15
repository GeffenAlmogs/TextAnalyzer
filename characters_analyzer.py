from graph import Graph, Node
import helper

class CharactersAnalyzer:
    def __init__(self, characters_names_and_nicknames_dict: dict[str,list[str]],
                 sentences: list[list[str]]):
        self.characters_names = characters_names_and_nicknames_dict
        self.sentences = sentences


    """
    ______________________Task 3________________________
    """


    def filter_and_convert_characters_count_to_list(self, characters_mentions_dict) -> list[list[str, int]]:
        """
        Filter the characters count dictonary from character without a count,
        and converts the filtered dictionary of characters count into a list of key-value pairs,
        where each pair is represented as a list [character, count].
        
        Parameters:
        characters_count (dict): A dictionary where keys are character's main names (strings)
                                    and values are their respective counts (integers).

        Returns:
        list of lists: A list where each element is a list of the form [character, count] 
                        representing the character count names.
        """

        # Sort the characters mentions dict keys alphabetically, by the characters names
        characters_mentions_sorted_dict = self._sort_characters_mentions_count_dict(characters_mentions_dict)
        filtered_characters_mentions = {}

        # Iterate over the characters and their mention counts
        for character, count in characters_mentions_sorted_dict.items():
            # Only add characters with non-zero mentions to the new dictionary
            if count > 0:
                filtered_characters_mentions[character] = count

        character_count_pairs_list = []

        # Iterate through each character and its count in the dictionary
        for character, count in filtered_characters_mentions.items():
            # Create a pair (sublist) with the current character and its count, and append it
            character_count_pair = [character, count]
            character_count_pairs_list.append(character_count_pair)

        return character_count_pairs_list
    


    def count_characters_mentions(self, sentences_window: list[list[str]] = []) -> dict[str,int]:
        """
        Count the total number of mentions of characters in a given window of sentences or in the entire text.
        
        Parameters:
        sentences_window (list[list[str]], optional): A list of sentences (each sentence is a list of words) to limit the search to. 
                                                    If None, the entire text is used (default is None).
        
        Returns:
        dict: A dictionary where the keys are character names and the values are the total counts of their mentions in the sentences.
        """

        # Use the provided sentence window if available, otherwise use the entire text
        sentences = sentences_window if sentences_window != [] else self.sentences

        characters_mentions_amount = {}

        # Initialize the count for each character in the text
        for name in self.characters_names.keys():
            characters_mentions_amount[name] = 0

            # Iterate over each sentence in the sentence window (or entire text)
            for sentence in sentences:
                # Convert the sentence list into a single string
                sentence_str = " ".join(sentence)

                # Count how many times the main name and nicknames are mentioned in the sentence
                main_name_count = self._count_main_name_in_sentence(name, self.characters_names[name], sentence)
                nicknames_count = self._count_nicknames_in_sentence(self.characters_names[name], sentence_str)

                # Add the counts to the character's total mentions
                characters_mentions_amount[name] = characters_mentions_amount[name] + main_name_count + nicknames_count

        return characters_mentions_amount



    def _sort_characters_mentions_count_dict(self, characters_mentions_dict) -> dict[str,int]:
        """
        Sorts the character count dictionary by the keys (character names) in alphabetical order.

        Parameters:
        sequence_count_dict (dict): A dictionary where keys are character names (strings)
                                    and values are their respective counts.

        Returns:
        dict: A new dictionary with the same key-value pairs as the input, but with the keys
              sorted in alphabetical order.
        """

        # Sort the keys alphabetically
        sorted_keys = list(characters_mentions_dict.keys())
        sorted_keys.sort()

        sorted_dict = {}

        # Add the key-value pairs to the new dictionary in sorted order
        for key in sorted_keys:
            sorted_dict[key] = characters_mentions_dict[key]

        return sorted_dict



    def _count_main_name_in_sentence(self, main_name: str, nicknames: list[str], sentence: list[str]) -> int:
        """
        Count the occurrences of parts of the main name in the sentence, only if those are not already in a nickname.
        
        Parameters:
        main_name (str): The full main name (it may consist of multiple words).
        nicknames (list[str]]): A list of nicknames to be excluded from the count.
        sentence (list[str]): The sentence in which the occurrences of parts of the main name are counted.
        
        Returns:
        int: The total count of occurrences of parts of the main name in the sentence, excluding nicknames.
        """
    
        name_appearence_count = 0

        partial_main_name = main_name.split(" ")

        # Loop through each part of the main name
        for partial_name in partial_main_name:
            for word in sentence:
                # Check if the partial name exists in the sentence and is not in the list of nicknames
                # To avoid multiple counts of name, because we'd count this part also as a nickname
                if partial_name == word and partial_name not in nicknames:
                        # Count occurrences of this part in the sentence and add to the total count
                        name_appearence_count = name_appearence_count + 1
        
        return name_appearence_count



    def _count_nicknames_in_sentence(self, nicknames: list[str], sentence: str) -> int:
        """
        Count the occurrences of nicknames in the given sentence.
        
        Parameters:
        nicknames (list[list[str]]): A list of strings that represents a nickname.
        sentence (str): The sentence in which we want to count the occurrences of the nicknames.
        
        Returns:
        int: The total count of appearances of all nicknames in the sentence.
        """

        nicknames_appearence_count = 0
        # Loop through each nickname in the list of nicknames
        for nickname in nicknames:
            # # Join the words of the nickname into a single string, because we search only whole nicknames and not partial
            # whole_nickname_str = " ".join(nickname)
            # Count how many times the full nickname appears in the sentence and add to the counter
            nicknames_appearence_count = nicknames_appearence_count + sentence.count(nickname)
        return nicknames_appearence_count
    

    
    """
    ______________________Task 5________________________
    """



    def _get_all_sentences_containing_character_mention(self, character_name) -> list[str]:
        """
        Retrieves all sentences that mention a given character by their main name or any associated nicknames.

        Parameters:
        character_name (str): The name of the character to search for in the sentences.

        Returns:
        list[str]: A list of sentences (as strings) where the character is mentioned by their main name or nickname.
        """

        all_sentences_mentioning_character = []

        for sentence in self.sentences:
            # Initilaize a variable to count characters mentions is the current sentence
            current_sentence_character_mentions_amount = 0
            # Convert the sentence list into a single string
            sentence_str = " ".join(sentence)

            # Count how many times the main name and nicknames are mentioned in the sentence
            main_name_count = self._count_main_name_in_sentence(character_name, self.characters_names[character_name], sentence)
            nicknames_count = self._count_nicknames_in_sentence(self.characters_names[character_name], sentence_str)

            # Add the counts to the character's total mentions
            current_sentence_character_mentions_amount = main_name_count + nicknames_count

            # If the overall count of the character mentions in the sentence is greater than zero
            if current_sentence_character_mentions_amount > 0:
                # Append the sentence to the list of all sentences mentioning the character
                all_sentences_mentioning_character.append(sentence_str)
        return all_sentences_mentioning_character



    def _get_kseq_of_sentences_mentioning_character(self, sentences_mentioning_character: list[str], kseq_max_length: int):
        """
        Generates all possible subsequences of words (k-sequences) from sentences that mention a specific character.

        Parameters:
        sentences_mentioning_character (list[str]): List of sentences containing the character's name or nickname.
        kseq_max_length (int): The maximum length of the k-sequence to generate.

        Returns:
        list[list[str]]: A list of k-sequences (subsequences of words) from the sentences.
        """
        all_kseq_of_all_sentences = []

        for current_sentence in sentences_mentioning_character:
            current_sentence_words = current_sentence.split()  # Split the sentence into words
            # Loop to generate sequences of word lengths from 1 up to kseq_max_length
            for length in range(1, kseq_max_length + 1):  # Go through all possible length for 1 to kseq_max_length
                # Iterate through the sentence and generate sub-sequences of the current length
                for i in range(len(current_sentence_words) - length + 1):
                    # The loop generates sub-sequences of the current length by slicing the words list from index i to i+length
                    # append any new sub-sequences
                    if current_sentence_words[i:i+length] not in all_kseq_of_all_sentences:
                        all_kseq_of_all_sentences.append(current_sentence_words[i:i+length])  # Append the sequence of words
        
        return all_kseq_of_all_sentences
    


    def _sort_associated_kseqs_of_character(self, character_associated_kseqs):
        """
        Sorts a list of k-sequences associated with a character.

        Parameters:
        character_associated_kseqs (list[list[str]]): List of k-sequences for a specific character.

        Returns:
        list[list[str]]: The sorted list of k-sequences.
        """
        # Sort the k-sequences (lexicographically by default)
        character_associated_kseqs.sort()
        return character_associated_kseqs # Return the sorted k-sequences
    


    def get_associated_kseqs_of_all_characters(self, max_kseq_length: int):
        """
        Retrieves and sorts the k-sequences for all characters by iterating over sentences that mention them.

        Parameters:
        max_kseq_length (int): The maximum length for the generated k-sequences.

        Returns:
        A list of key-value pairs where each pair is represented as a list [character, kseqs], 
        with 'character' being the character's name (str) and 'kseqs' being the sorted list of their associated k-sequences (list of list of strings).
        """

        characters_contexts_kseqs = []

        sorted_characters_names = list(self.characters_names.keys()) # Get a sorted list of character names
        sorted_characters_names.sort() # Sort the names alphabetically

        for name in sorted_characters_names:
            # Get all sentences mentioning the current character
            all_sentences_mentioning_character = self._get_all_sentences_containing_character_mention(name)
            # Get the k-sequences associated with the character
            character_associated_kseqs = self._get_kseq_of_sentences_mentioning_character(all_sentences_mentioning_character, max_kseq_length)
            # Sort the k-sequences for the current character
            sorted_character_associated_kseqs = self._sort_associated_kseqs_of_character(character_associated_kseqs)

            # Only add to the results if there are any k-sequences for the character
            if sorted_character_associated_kseqs != []:
                characters_contexts_kseqs.append([name, sorted_character_associated_kseqs])
        
        return characters_contexts_kseqs




    """
    ______________________Task 6________________________
    """

    
    def _get_all_names_in_sentences_window(self, sentences_window: list[list[str]]) -> list[str]:
        """
        Extracts all characters mentioned within a given window of sentences.

        Parameters:
        sentences_window (list[list[str]]): A list of sentences (each represented as a list of words) within a specific window.

        Returns:
        list[str]: A list of characters' names mentioned in the given window of sentences.
        """
        # Retrive a dictonary with characters and their matching count in the given senteces window
        names_count_in_window_dict = self.count_characters_mentions(sentences_window)

        # Initialize an empty list to store the characters mentioned
        characters_mentioned_in_window = []

        # Loop through the dictionary of counted names
        for character_main_name in names_count_in_window_dict.keys():
            # If the character is mentioned at least once, add them to the list
            if names_count_in_window_dict[character_main_name] > 0:
                characters_mentioned_in_window.append(character_main_name)

        return characters_mentioned_in_window
            


    def get_direct_connections_between_characters(self, window_size:int, threshold:int) -> list[list[list[str]]]:
        """
        Retrieves the direct connections between characters based on a sliding window of sentences,
        where connections are determined by their co-occurrences in the same sentence windows.

        Parameters:
        window_size (int): The size of the sliding window (in terms of sentences) to consider when analyzing character co-occurrences.
        threshold (int): The minimum number of sentence windows in which characters must appear together for a connection to be valid.

        Returns:
        list[list[str]]: A sorted list of lists representing pairs of characters that are directly connected, 
                    based on their co-occurrence in enough sentence windows.
        """
        # Check if the provided window size is valid.
        if window_size > len(self.sentences):
            print("invalid input: Window-size cannot be larger than the amount of sentences.")
            exit()

        # Build the characters' connection graph - this creates edges based on appearances of both characters in the same sentence window
        connections_graph: Graph = self._build_characters_connections_graph(window_size)
        # Retrieve the connected pairs that meet the threshold - they must appear together in enough sentence windows
        connections_sets = connections_graph.get_connected_pairs(threshold)
        # Convert the character pairs from sets to sorted lists and return the result
        sorted_connections_list = self._convert_characters_connections_pairs_to_lists(connections_sets)
        return sorted_connections_list


    def _convert_characters_connections_pairs_to_lists(self, characters_direct_connections: list[set[str]]) -> list[list[list[str]]]:
        """
        Converts a list of sets of character pairs into a sorted list of lists.

        Parameters:
        characters_direct_connections (list[set[str]]): A list of sets, where each set contains pairs of characters that are directly connected.

        Returns:
        list[list[str]]: A sorted list of character pairs, where each pair is represented as a list of two characters.
        """

        sorted_character_connections_list = []

        # Iterate over each set of connected character pairs
        for connection_set in characters_direct_connections:
            # Create a list to hold the separated (and sorted) names for this character pair
            sorted_pair_list = []

            # Split each character name (if it contains multiple words) and append to the pair list
            for character_name in connection_set:
                separated_name = character_name.split(" ")  # Split the full character name into individual words
                sorted_pair_list.append(separated_name)

            # Sort the character names alphabetically within the pair
            sorted_pair_list.sort()

            # Add the sorted pair to the list of character pairs
            sorted_character_connections_list.append(sorted_pair_list)

        # Finally, sort the list of character pairs alphabetically
        sorted_character_connections_list.sort()

        return sorted_character_connections_list


    """
    ______________________Task 7 + 8________________________
    """

    def determinate_connections_up_to_max_length(self, connections_to_analyze: list[list[str]], window_size: int, threshold: int, maximal_distance: int, premade_graph: Graph = None):
        """
        Analyzes pairs of characters to determine if a connection exists between them within a given threshold and maximum distance.
        This method builds a graph of character connections based on their appearances in the same sentence window, or uses a premade graph if provided. It then checks whether a connection exists between each pair of characters, and appends the result (True or False) to the list for each pair.

        Parameters:
        connections_to_analyze (list[list[str]]): A list of character pairs (as two-element lists) to check for connections.
        window_size (int): The size of the window to analyze character co-occurrences.
        threshold (int): The maximum number of sentences the characters can appear apart before being considered connected.
        maximal_distance (int): The maximum distance (in terms of sentence separation) at which characters are considered connected.
        premade_graph (Graph, optional): A pre-built graph to use for analysis instead of creating a new one. Default is None.

        Returns:
        list[list[Union[str, bool]]]: A list of the analyzed character pairs with a boolean indicating if a connection was found (True/False).
        """
        
        analyzed_connections = []
        
        # Use the premade graph if provided, otherwise build a new one
        if premade_graph == None:
            # Check if the provided window size is valid.
            if window_size > len(self.sentences):
                print("invalid input: Window-size cannot be larger than the amount of sentences.")
                exit()
            # Build the characters' connection graph - this creates edges based on appearances of both characters in the same sentence window
            connections_graph: Graph = self._build_characters_connections_graph(window_size)
        else:
            connections_graph = premade_graph

        # Loop through each character pair to analyze their connection
        for characters_pair in connections_to_analyze:
            first_character = characters_pair[0]
            second_character = characters_pair[1]

            pair_connection_with_desicion = []

            # Check if a path exists between the characters within the given thresholds
            if connections_graph.path_exists_up_to_length(first_character, second_character, threshold, maximal_distance):
                pair_connection_with_desicion = sorted(characters_pair) # Sort the pair lexicographically
                pair_connection_with_desicion.append(True) # Connection exists
            else:
                pair_connection_with_desicion = sorted(characters_pair) # Sort the pair lexicographically
                pair_connection_with_desicion.append(False) # No connection
            
            analyzed_connections.append(pair_connection_with_desicion)
            analyzed_connections.sort() # Sort the list lexicographically

        return analyzed_connections
    

    def determinate_connections_of_exact_length(self, connections_to_analyze: list[list[str]], window_size: int, threshold: int, exact_distance: int, premade_graph: Graph = None):
        """
        Analyzes pairs of characters to determine if a connection exists between them with an exact distance within a given threshold.
        This method builds a graph of character connections based on their appearances in the same sentence window, or uses a premade graph if provided. It then checks whether a connection exists between each pair of characters at the exact specified distance and within the threshold.

        Parameters:
        connections_to_analyze (list[list[str]]): A list of character pairs (as two-element lists) to check for connections.
        window_size (int): The size of the window to analyze character co-occurrences.
        threshold (int): The maximum number of sentences the characters can appear apart before being considered connected.
        exact_distance (int): The exact distance (in terms of sentence separation) at which characters are considered connected.
        premade_graph (Graph, optional): A pre-built graph to use for analysis instead of creating a new one. Default is None.

        Returns:
        list[list[Union[str, bool]]]: A list of the analyzed character pairs with a boolean indicating if a connection was found (True/False).
        """
        
        analyzed_connections = []
        
        # Use the premade graph if provided, otherwise build a new one
        if premade_graph == None:
            # Check if the provided window size is valid.
            if window_size > len(self.sentences):
                print("invalid input: Window-size cannot be larger than the amount of sentences.")
                exit()
            # Build the characters' connection graph - this creates edges based on appearances of both characters in the same sentence window
            connections_graph: Graph = self._build_characters_connections_graph(window_size)
        else:
            connections_graph = premade_graph

        # Loop through each character pair to analyze their connection
        for characters_pair in connections_to_analyze:
            first_character = characters_pair[0]
            second_character = characters_pair[1]

            pair_connection_with_desicion = []
            if connections_graph.path_exists_exact_length(first_character, second_character, threshold, exact_distance):
                pair_connection_with_desicion = sorted(characters_pair) # Sort the pair lexicographically
                pair_connection_with_desicion.append(True) # Connection exists
            else:
                pair_connection_with_desicion = sorted(characters_pair) # Sort the pair lexicographically
                pair_connection_with_desicion.append(False) # No connection
            
            analyzed_connections.append(pair_connection_with_desicion)
            analyzed_connections.sort() # Sort the list lexicographically

        return analyzed_connections
       
        
        
    """
    ______________________helper for 6,7,8________________________
    """

    def _build_characters_connections_graph(self, sentences_window_size) -> Graph:
        """
        Builds a graph of character connections based on sentences windows.

        Parameters:
        sentences_window_size (int): The size of each window of sentences to analyze character mentions and connections.

        Returns:
        Graph: A graph representing the connections between characters, where each character is a node and edges represent mentions in the same sentence window.
        """

        graph = Graph()

        # Add a node for each character using their name as indetifier-key and associated nicknames as values
        for name in self.characters_names.keys():
            node = Node(name, self.characters_names[name])
            graph.add_node(node)
            
        # Get all possible sentence windows of the specified size
        all_sentences_windows = helper.get_sentences_windows(self.sentences, sentences_window_size)

        # For each sentence window, get the characters mentioned together and link them in the graph
        for sentences_window in all_sentences_windows:
            names_in_window = self._get_all_names_in_sentences_window(sentences_window)
            graph.link_all_names_in_window(names_in_window)
        
        return graph
    

    def build_graph_with_preprocessed_pairs(self, character_pairs_connections: list[list[list[str]]]):
        """
        Builds a graph from preprocessed character pairs connections.
        Each pair of characters is connected by an edge in the graph.

        Parameters:
        connections (list[list[list[str]]]): A list of character pairs, 
                                            where each pair is represented by a list of character names 
                                            (each name may be split into multiple words).

        Returns:
        Graph: A graph object with nodes representing characters and edges connecting characters that appear in pairs.
        """
        graph = Graph()

        # Iterate over each group of character pairs
        for connection_pair in character_pairs_connections:
            # List to store the full characters main names for this current connection 
            pair_connection_names = []
            
            # Iterate over each character pair in the group
            for character_parted_main_name in connection_pair:
                # Join the parts of the character name into a full name (if split)
                full_character_main_name = " ".join(character_parted_main_name)

                # Create a new node for this character and add it to the graph
                character_node = Node(full_character_main_name, [])
                graph.add_node(character_node)

                # Add the full character name to the pair names list for edge creation
                pair_connection_names.append(full_character_main_name)

            # Create an edge between the two characters in the pair
            # This connects the first character with the second in the pair
            graph.create_edge_between_nodes_by_keys(pair_connection_names[0], pair_connection_names[1])

        return graph

                