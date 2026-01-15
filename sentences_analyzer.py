import json
import helper
from graph import Graph, Node

class SentencesAnalyzer:

    def __init__(self, sentences:  list[list[str]]):
        self.sentences: list[list[str]] = sentences

    
    """
    ___________________Task 2___________________
    """


    def create_k_sequences_counts_up_to_max_k(self, max_k: int):
        """
        Creates a list where each element represents k-sequence counts for k from 1 to max_k.

        Parameters:
        max_k (int): The maximum value of k for which k-sequence counts will be generated.

        Returns:
        list of lists: A list where each element is a list of the form 
                        [f"{k}_seq", list_of_k_sequence_counts], 
                        where list_of_k_sequence_counts contains k-sequence 
                        and their counts for the given k.
        """
        # Initialize an empty list to hold the results for all k-sequence counts
        all_k_sequences = []

        for k in range(1, max_k + 1):
            # Get all k-length word sequences in the sentences and count their ocurrences
            current_k_sequence_count_dict = self._count_k_word_sequences(k)

            # Sort the k-sequence count dictionary by the keys (k-sequences) by alphabetical order
            sorted_dict_of_k_seq_count = self._sort_k_seq_count_dict(current_k_sequence_count_dict)
           
            # Convert the sorted k-sequence counts into a list of [k-sequence, count] pairs
            current_k_sequence_count_list = self._convert_k_sequence_count_to_list(sorted_dict_of_k_seq_count)
            
            # Append the result for this value of k to the main list
            all_k_sequences.append([f"{k}_seq", current_k_sequence_count_list])

        return all_k_sequences
        


    def _count_k_word_sequences(self, k: int) -> dict[str,int]:
        """
        Get all k-length word sequences and the counts of their ocurrences across a list of sentences.
        (the sentences are a list of list of str, a list where each element is a sentence represented as a list of words (strings).)
        
        Parameters:
        k (int): The length of the word sequences to count.

        Returns:
        dict: A dictionary where keys are the k-word sequences (as strings) and the values 
            are the counts of their ocurrences.
        """

        # Init an empty dictionary to store the counts of k-word sequences
        sequence_counts : dict = {}

        for sentence in self.sentences:
            words_amount = len(sentence)
            
            # Iterate through the sentence to extract all possible k-word sequences, without exceeding the sentence
            for i in range(words_amount - k + 1):

                # Get the current k-word sequence from the sentence, as a string
                current_k_sequence = sentence[i:i+k]
                current_k_sequence_str = " ".join(current_k_sequence)

                # If this sequence has already been encountered, increment its count
                if current_k_sequence_str in sequence_counts:
                    sequence_counts[current_k_sequence_str] += 1
                else:
                    # Else, init it's count to 1
                    sequence_counts[current_k_sequence_str] = 1

        return sequence_counts
    


    def _sort_k_seq_count_dict(self, sequence_count_dict) -> dict[str,int]:
        """
        Sorts the k-sequence count dictionary by the keys (k-sequences) in alphabetical order.

        Parameters:
        sequence_count_dict (dict): A dictionary where keys are k-sequences (strings)
                                    and values are their respective counts.

        Returns:
        dict: A new dictionary with the same key-value pairs as the input, but with the keys
              sorted in alphabetical order.
        """

        # Sort the keys alphabetically
        sorted_keys = list(sequence_count_dict.keys())
        sorted_keys.sort()

        sorted_dict = {}

        # Add the key-value pairs to the new dictionary in sorted order
        for key in sorted_keys:
            sorted_dict[key] = sequence_count_dict[key]

        return sorted_dict
    


    def _convert_k_sequence_count_to_list(self, sequence_count_dict) -> list[list[str, int]]:
        """
        Converts a dictionary of k-sequence counts into a list of key-value pairs,
        where each pair is represented as a list [k-sequence, count].
        
        Parameters:
        sequence_count_dict (dict): A dictionary where keys are k-sequences (strings)
                                    and values are their respective counts (integers).

        Returns:
        list of lists: A list where each element is a list of the form [k-sequence, count] 
                        representing the k-sequence and its count.
        """
    
        sequence_count_pairs_list = []

        # Iterate through each k-sequence and its count in the dictionary
        for k_sequence, count in sequence_count_dict.items():
            # Create a pair (sublist) with the current k-sequence and its count, and append it
            k_sequence_pair = [k_sequence, count]
            sequence_count_pairs_list.append(k_sequence_pair)

        return sequence_count_pairs_list
        



    """
    ___________________Task 4___________________
    """



    def get_kseqs_matching_sentences(self, kseqs_to_search: list[list[str]]):
        """
        Searches for k-sequences across a list of k-length sequences, retrieves matching sentences - which are sentences containing those sequences, 
        sorts the matches, and returns them in a list of key-value pairs.

        Parameters:
        query_keys (list of lists of strings): A list where each element is a list of words 
                                                representing k-sequences to search for.

        Returns:
        list of lists: A list where each element is a list of the form [k-sequence, matching_sentences_list], 
                        representing the k-sequence and its corresponding sorted matching sentences.
        """

        # Retrieve a dictionary of sequences and their matching sentences based on the query keys
        sequences_to_matching_sentences_dict = self.search_sequences_matching_sentences(kseqs_to_search)
        # Sort the sequences and their corresponding matching sentences
        sorted_sequences_to_matching_sentences_dict = self._sort_sequences_matches_dict(sequences_to_matching_sentences_dict)
        # Convert the sorted dictionary into a list of key-value pairs
        sequence_sentences_pairs_list = self._convert_kseq_matches_dict_to_list(sorted_sequences_to_matching_sentences_dict)

        return sequence_sentences_pairs_list
    


    def _get_words_seqs_lens(self, words_seqs: list[list[str]]) -> set[int]:
        """
        Given list of lists of words sequences, return the different lengths of those sequences.
        
        Parameters:
        words_seqs: List of words sequences (where each words sequences is a list of words).
        
        Returns: 
        A set of integers representing the different lengths of the words sequences
        """

        words_seqs_lens = set()
        # Iterate through each words-sequence in the given list of words-sequences
        for words_seq in words_seqs:
            # Get the length of the current sequence
            words_seqs_lens.add(len(words_seq))
        # Sort the lengths from the smallest to the largest
        sorted_words_seqs_lens = sorted(words_seqs_lens)
        return sorted_words_seqs_lens



    def _init_k_seq_matches_dict(self, query_keys: list[list[str]]) -> dict[str,list[any]]:
        """
        Initializes a dictionary where each key is a sequence of words (as a string),
        and the corresponding value is an empty list.

        Parameters:
        query_keys: A list of word sequences, where each sequence is a list of words.

        Returns:
        dict: A dictionary where the keys are word sequences as strings, and the values are empty lists.
        """
        k_seq_matches = {}
        for key in query_keys:
            current_key = " ".join(key)
            k_seq_matches[current_key] = []
        return k_seq_matches



    def create_dict_of_all_possible_seqs_in_all_sentences(self, words_seqs_lens: list[int]):
        """
        This function generates a dictionary of all possible word sequences of different lengths
        from the given list of sentences. Each key in the dictionary is a sequence of words,
        and the corresponding value is a list of sentences in which that sequence appears.

        Parameters:
        sentences: List of sentences (where each sentence is a list of words).
        sequence_lengths: List of integers representing the lengths of word sequences to extract.
        
        Returns: 
        A dictionary where keys are word sequences (as strings) and values are lists of sentences containing those sequences.
        
        Example:
        Input:
        sentences = [
            ["snitch", "flew", "away"],
            ["hermione", "snitch"]
        ]
        words_seqs_lens = [1, 2]
        
        Output:
        {'snitch': [['snitch', 'flew', 'away'], ['hermione', 'snitch']],
        'flew': [['snitch', 'flew', 'away']],
        'away': [['snitch', 'flew', 'away']],
        'hermione': [['hermione', 'snitch']]
        'snitch flew': [['snitch', 'flew', 'away']],
        'flew away': [['snitch', 'flew', 'away']],
        'hermione snitch': [['hermione', 'snitch']]}
        """

        # Dictionary to store sequences and sentences containing them
        sequence_to_sentences = {}

        for k_seq_len in words_seqs_lens:
            for sentence in self.sentences:
                words_amount = len(sentence)
                # Looping through the sentence to get all possible sequences of the current length
                for i in range(words_amount - k_seq_len + 1): # Sliding within the array boundries
                    current_words_seq = sentence[i:i+k_seq_len] # Extract the current sequence of words
                    current_seq_key = " ".join(current_words_seq) # Convert the sequence into a string (space-separated) to use as a dictionary key
                    
                    # If the sequence already exists in the dictionary
                    if current_seq_key in sequence_to_sentences.keys():
                        # Append the current sentence to it, only if it's not already found due to the word appearing more than once in the sentence - so it was found already
                        if sentence not in sequence_to_sentences[current_seq_key]:
                            sequence_to_sentences[current_seq_key].append(sentence)
                    
                    # Otherwise, create a new entry for this sequence
                    else:
                        sequence_to_sentences[current_seq_key] = []
                        sequence_to_sentences[current_seq_key].append(sentence)
        return sequence_to_sentences



    def search_sequences_matching_sentences(self, sequences_to_search: list[list[str]]) -> dict[str,list[list[str]]]:
        """
        Finding all matches (specificly, the matching sentences) for given word sequences across a list of sentences.
        In other words, searching the sequence across all sentences, and return the sentences that contains this sequence
        
        Parameters:
        sequences_to_search: A list of word sequences to search for in the sentences.

        Returns:
        A dict where the keys are the word sequences as strings, and the values are lists of sentences containing those sequences.

        Note: 
        The search for each word-sequence in the dictionary `all_seqs_in_all_sentences` is O(1) because Python 
        dictionaries use hash tables, which allow for constant-time lookups. 
        When you check if a key exists, Python hashes the key and directly accesses its value in memory, regardless of the size of the dictionary.
        In this case, each word-sequence gets hashed which allows direct accesses to its value, which is all the sentences containing the sequence,
        meaning the search of specific sequence across all sentences is O(1)!
        """
        # Initialize the dict for matching sentences
        sequence_matches = self._init_k_seq_matches_dict(sequences_to_search)
        # Get all desired sequences lengths in sentences
        words_seqs_lens = self._get_words_seqs_lens(sequences_to_search)
        # Create a dictionary of all possible sequences in all sentences
        all_sequences_in_sentences = self.create_dict_of_all_possible_seqs_in_all_sentences(words_seqs_lens)

        for current_words_seq in sequences_to_search:
            # Convert the current word sequence into a string so it could be used as a dict key
            words_seq_key = " ".join(current_words_seq)

            # Check if the word sequence exists in the dictionary of all sequences in the sentences
            # O(1) lookup: Hash tables provide constant-time key lookups
            if words_seq_key in all_sequences_in_sentences.keys():
                # Update the sequence_matches dictionary with the matching sentences
                sequence_matches[words_seq_key] = all_sequences_in_sentences[words_seq_key]
        
        return sequence_matches



    def _sort_sequences_matches_dict(self, sequences_to_matching_sentences_dict):
        """
        Sorts the input dictionary by its keys and also sorts the sentences for each key alphabetically.

        Parameters:
        sequences_to_matching_sentences_dict (dict): A dictionary where the keys are sequences (strings) 
                                                    and the values are lists of sentences (list of strings) containing those seqs.

        Returns:
        dict: A new dictionary where the sequences are sorted alphabetically and each list of sentences 
            corresponding to those sequences is also sorted alphabetically.
        """
        # Extract the keys (sequences) from the dictionary and store them in a list
        original_dict_keys = list(sequences_to_matching_sentences_dict.keys())
        
        # Sort the keys (sequences) alphabetically in ascending order
        # This means the keys (which are strings) will be ordered lexicographically
        original_dict_keys.sort()

        sorted_dict = {}

        # Iterate over each sorted key (sequence)
        for key in original_dict_keys:
            # Sort the list of matching sentences for the current sequence (key) alphabetically
            sequences_to_matching_sentences_dict[key].sort() 
            # Add the sorted sequence and its corresponding sorted list of sentences to the new dictionary
            sorted_dict[key] = sequences_to_matching_sentences_dict[key]

        return sorted_dict



    def _convert_kseq_matches_dict_to_list(self, sequences_to_matching_sentences_sorted: dict[str,list[list[str]]]):
        """
        Converts a dictionary of k-sequence matches into a list of key-value pairs, 
        where each pair is represented as a list [k-sequence, matching_sentences_list].

        Parameters:
        sequence_matches_sorted (dict): A dictionary where keys are k-sequences (strings) 
                                        and values are lists of matching sentences (lists of strings).

        Returns:
        list of lists: A list where each element is a list of the form [k-sequence, matching_sentences_list], 
                        representing the k-sequence and its corresponding matching sentences.
        """
        sequence_sentences_pairs = []

        # Iterate over each sequence in the sorted dictionary (sequence_matches_sorted)
        for sequence in sequences_to_matching_sentences_sorted.keys():
            # Check if the list of matching sentences for this key is not empty
            if sequences_to_matching_sentences_sorted[sequence] != []:
                # Append a list of the form [key, matching_sentences] to the result list
                sequence_sentences_pairs.append([sequence, sequences_to_matching_sentences_sorted[sequence]])

        return sequence_sentences_pairs
    


    """
    ___________________Task 9___________________
    """



    def group_sentences_by_shared_words(self, threshold: int):
        """
        Groups sentences by shared words. Sentences are connected if they share at least `threshold` words.
        
        Parameters:
        threshold (int): Minimum shared words to consider sentences connected.
            
        Returns:
        list: A list of sentence groups where sentences are connected by shared words.

        Note:
        Time complexity in the worst case for fully connected graph could be: O(n^2)*O(m)
        [m - longest sentence length, n - sentences amount]
        """
        graph = Graph()

        # Create nodes for each sentence
        for i, sentence in enumerate(self.sentences):

            node = Node(f'sentence {i+1}', sentence)
            graph.add_node(node)

        # Sentence's key is the number of the sentence, the value of the sentence node is the words of the sentence
        # Compare sentence pairs for shared words
        sentences_nodes_keys_pairs = helper.get_combinations_of_two(graph.nodes.keys())

        # Loop time-complexity: O(n CHOOSE 2) <= O(n^2) - n is the sentences amount
        for sentences_keys_pair in sentences_nodes_keys_pairs:
            
            # Get the keys from the pairs
            sentences_keys_list = list(sentences_keys_pair) # O(2) = O(1)

            first_sentence_key, second_sentence_key = sentences_keys_list

            first_sentence_words_set = set(graph.nodes[first_sentence_key].values)  # convertion time-complexity: O(len(first_sentence_words_set)) <= O(M) - M is the length of the longest sentence
            second_sentence_words_set = set(graph.nodes[second_sentence_key].values) # convertion time-complexity: O(len(second_sentence_words_set)) <= O(M) - M is the length of the longest sentence

            # Check if sentences are connected
            # if time-complexity: O(len(first_sentence_set) + len(second_sentence_words_set)) <= O(M) - M is the length of the longest sentence
            if self._are_sentences_connected(first_sentence_words_set, second_sentence_words_set, threshold):
                graph.create_edge_between_nodes_by_keys(first_sentence_key, second_sentence_key) # O(1)

        connected_sentences_keys_groups = graph.get_connected_componnets() # O(E + V) = O(sentences_num + sentences_num CHOOSE 2) <= O(n^2)

        # Data arrangment
        # Collect sentences into groups based on their connections
        list_of_sentences_groups = []
        for keys_list_of_connected_sentences in connected_sentences_keys_groups:
            current_sentences_group = []
            for sentence_key in keys_list_of_connected_sentences:
                # Add sentences to the current group
                current_sentences_group.append(graph.nodes[sentence_key].values)
            list_of_sentences_groups.append(current_sentences_group)

        return list_of_sentences_groups
    

    
    def _sort_sentences_groups(self, list_of_sentences_groups: list[list[list[str]]]):
        """
        Sorts the sentence groups first by the number of sentences in each group, 
        and then alphabetically within each group. Additionally, each group is named 
        based on its order in the sorted list.

        Parameters:
        list_of_sentences_groups (list): A list of sentence groups, where each group is a list of sentences.

        Returns:
        list: A sorted list of sentence groups, each with a name ("Group X") indicating its order.
        """

        # Sort sentences within each group alphabetically
        for sentences_group in list_of_sentences_groups:
            sentences_group.sort()

        # Sort the groups by the number of sentences, then alphabetically if they are of the same amount pf sentences
        list_of_sentences_groups.sort(key=lambda group: (len(group), group))

        sorted_and_named_sentences_groups = []

        # Name each group according to its position in the sorted list
        for i, sentences_group in enumerate(list_of_sentences_groups):
            sorted_and_named_sentences_groups.append([f"Group {i+1}", sentences_group])
        
        return sorted_and_named_sentences_groups
    

    def get_sorted_sentences_groups(self, threshold: int):
        """
        Groups sentences based on shared words and returns the sorted groups.
        Sentences are connected if they share at least `threshold` words, and the groups  are sorted by the number of sentences and alphabetically.

        Parameters:
        threshold (int): Minimum shared words to connect sentences.
            
        Returns:
        list: Sorted and named sentence groups, based on shared words.
        """
        # Group sentences by shared words using the specified threshold
        list_of_sentences_groups = self.group_sentences_by_shared_words(threshold)
        # Sort and name the groups
        sorted_and_named_sentences_groups = self._sort_sentences_groups(list_of_sentences_groups)
        return sorted_and_named_sentences_groups
        

    def _are_sentences_connected(self, first_sentence: set, second_sentence: set, mininum_shared_words_amount: int) -> bool:
        """
        Determines if two sentences share enough words to be considered connected.

        Parameters:
            first_sentence (set): Set of words from the first sentence.
            second_sentence (set): Set of words from the second sentence.
            mininum_shared_words_amount (int): Minimum number of shared words to consider sentences connected.

        Returns:
        bool: True if sentences are connected (share enough words), otherwise False.

        Note:
        Time complexity of union: O(len(first_set)+len(second_set))
        """
        # Check if the number of shared words is greater than or equal to the threshold
        return (len(first_sentence) + len(second_sentence)) - len(first_sentence.union(second_sentence)) >= mininum_shared_words_amount 
