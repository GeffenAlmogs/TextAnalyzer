import json
from helper import parse_csv_to_list_str, parse_csv_to_set_str, create_names_and_nicknames_dict
from sentences_processor import SentencesProcessor
from names_processor import NameProcessor
from sentences_analyzer import SentencesAnalyzer
from preprocessed_handler import PreProcessedHandler
from characters_analyzer import CharactersAnalyzer

import timeit


JSON_INDENT = 4


class TaskRunner:
    """
    A class that runs various tasks based on input CSV files and processes data.
    """

    def __init__(self, preprocessed_flow: bool = False, preprocessed_json_path: str = ''):
        # Initialize with a flag for preprocessed flow and path to the preprocessed JSON if applicable
        self.preprocessed_flow = preprocessed_flow
        self.preprocessed_json_path = preprocessed_json_path



    def _get_processed_data(self, sentences_csv_path, names_csv_path, unwanted_words_csv_path):
        """
        Process the sentences and names from CSV files.
        If preprocessed data is available, load that instead.
        """
        if self.preprocessed_flow:
            # Use preprocessed data if preprocessed_flow is True
            preprocessed_handler = PreProcessedHandler(self.preprocessed_json_path)
            processed_sentences = preprocessed_handler.extract_processed_sentences()
            processed_names = preprocessed_handler.extract_processed_names()
        else:
            # Parse and process sentences and names from CSV files
            sentences_list = parse_csv_to_list_str(sentences_csv_path)
            unwanted_words_set = parse_csv_to_set_str(unwanted_words_csv_path)
            sentences_processor = SentencesProcessor(sentences_list, unwanted_words_set)
            processed_sentences = sentences_processor.process_sentences()
           
            processed_names = []
            if names_csv_path:
                names_list = parse_csv_to_list_str(names_csv_path)
                names_processor = NameProcessor(names_list, unwanted_words_set)
                processed_names = names_processor.process_names()

        return processed_sentences, processed_names
    


    def run_task_1(self, sentences_csv_path, names_csv_path, unwanted_words_csv_path):
        """
        Task 1: Process the sentences and names, and return them in JSON format.
        """
        sentences_list_str = parse_csv_to_list_str(sentences_csv_path)
        names_list_str = parse_csv_to_list_str(names_csv_path)
        unwanted_words_set_str = parse_csv_to_set_str(unwanted_words_csv_path)

        sentences_processor = SentencesProcessor(sentences_list_str, unwanted_words_set_str)
        names_processor = NameProcessor(names_list_str, unwanted_words_set_str)

        processed_sentences = sentences_processor.process_sentences()
        processed_names = names_processor.process_names()

        result_json = {
            "Question 1": {
                "Processed Sentences": processed_sentences,
                "Processed Names": processed_names
            }
        }

        return json.dumps(result_json, indent=JSON_INDENT)



    def run_task_2(self, sentences_csv_path, unwanted_words_csv_path, maximal_kseq):
        """
        Task 2: Analyze k-sequences from the processed sentences and return counts of sequences up to maximal_kseq.
        """

        processed_sentences, _ = self._get_processed_data(sentences_csv_path, None, unwanted_words_csv_path)
        
        sentences_analyzer = SentencesAnalyzer(processed_sentences)
        k_sequences_counts_up_to_max_k = sentences_analyzer.create_k_sequences_counts_up_to_max_k(maximal_kseq)

        result_json = {
            "Question 2": {
                f"{maximal_kseq}-Seq Counts": k_sequences_counts_up_to_max_k
            }
        }

        return json.dumps(result_json, indent=JSON_INDENT)



    def run_task_3(self, sentences_csv_path, names_csv_path, unwanted_words_csv_path):
        """
        Task 3: Count character mentions in the processed sentences and names, then return them in JSON format.
        """

        processed_sentences, processed_names = self._get_processed_data(sentences_csv_path, names_csv_path, unwanted_words_csv_path)
        
        characters_names_and_nicknames_dict = create_names_and_nicknames_dict(processed_names)
        characters_analyzer = CharactersAnalyzer(characters_names_and_nicknames_dict, processed_sentences)

        characters_mentions_dict = characters_analyzer.count_characters_mentions()
        character_mentions_pairs_list = characters_analyzer.filter_and_convert_characters_count_to_list(characters_mentions_dict)

        result_json = {
            "Question 3": {
                "Name Mentions": character_mentions_pairs_list
            }
        }

        return json.dumps(result_json, indent=JSON_INDENT)



    def run_task_4(self, sentences_csv_path, unwanted_words_csv_path, qseq_json_path):
        """
        Task 4: Match k-sequences to sentences containing them and return matching results.
        """

        kseq_preprocessed_handler = PreProcessedHandler(qseq_json_path)
        kseq_list = kseq_preprocessed_handler.extract_query_keys()

        processed_sentences, _ = self._get_processed_data(sentences_csv_path, None, unwanted_words_csv_path)
        
        sentences_analyzer = SentencesAnalyzer(processed_sentences)
        kseq_matches = sentences_analyzer.get_kseqs_matching_sentences(kseq_list)

        result_json = {
            "Question 4": {
                "K-Seq Matches": kseq_matches
            }
        }

        return json.dumps(result_json, indent=JSON_INDENT)



    def run_task_5(self, sentences_csv_path, names_csv_path, unwanted_words_csv_path, max_kseq_length):
        """
        Task 5: Get associated k-sequences of characters and return them in JSON format.
        """

        processed_sentences, processed_names = self._get_processed_data(sentences_csv_path, names_csv_path, unwanted_words_csv_path)

        characters_names_and_nicknames_dict = create_names_and_nicknames_dict(processed_names)
        characters_analyzer = CharactersAnalyzer(characters_names_and_nicknames_dict, processed_sentences)

        characters_contexts = characters_analyzer.get_associated_kseqs_of_all_characters(max_kseq_length)

        result_json = {
            "Question 5": {
                "Person Contexts and K-Seqs": characters_contexts
            }
        }

        return json.dumps(result_json, indent=JSON_INDENT)



    def run_task_6(self, sentences_csv_path, names_csv_path, unwanted_words_csv_path, window_size, treshold):
        """
        Task 6: Get direct connections between characters and return them in JSON format.
        """

        processed_sentences, processed_names = self._get_processed_data(sentences_csv_path, names_csv_path, unwanted_words_csv_path)

        characters_names_and_nicknames_dict = create_names_and_nicknames_dict(processed_names)
        characters_analyzer = CharactersAnalyzer(characters_names_and_nicknames_dict, processed_sentences)

        characters_direct_connections = characters_analyzer.get_direct_connections_between_characters(window_size, treshold)

        result_json = {
            "Question 6": {
                "Pair Matches": characters_direct_connections
            }
        }

        return json.dumps(result_json, indent=JSON_INDENT)



    def run_task_7(self, sentences_csv_path, names_csv_path, unwanted_words_csv_path, window_size, treshold, people_connections_json_path, maximal_distance):
        """
        Task 7: Find ondirect connections between characters based on people connections and return them in JSON format.
        """

        people_connections_preprocessed_handler = PreProcessedHandler(people_connections_json_path)
        people_connections_list = people_connections_preprocessed_handler.extract_people_connections()

        premade_people_connections_graph = None

        if self.preprocessed_flow:
            preprocessed_pairs_handler = PreProcessedHandler(self.preprocessed_json_path)
            preprocessed_people_connections = preprocessed_pairs_handler.extract_processed_pairs()
            premade_people_connections_graph = preprocessed_pairs_handler.build_graph_with_preprocessed_pairs(preprocessed_people_connections)
            # If the graph is premade, threshold doesn't matter
            treshold = 1 # We've pre-built the graph, so every connection's weight is not 1 - and the treshold doesn't matter
        
        processed_sentences, processed_names = self._get_processed_data(sentences_csv_path, names_csv_path, unwanted_words_csv_path)
        
        characters_names_and_nicknames_dict = create_names_and_nicknames_dict(processed_names)
        characters_analyzer = CharactersAnalyzer(characters_names_and_nicknames_dict, processed_sentences)

        characters_direct_connections = characters_analyzer.determinate_connections_up_to_max_length(
            people_connections_list, window_size, treshold, maximal_distance, premade_people_connections_graph
        )

        result_json = {
            "Question 7": {
                "Pair Matches": characters_direct_connections
            }
        }

        return json.dumps(result_json, indent=JSON_INDENT)



    def run_task_8(self, sentences_csv_path, names_csv_path, unwanted_words_csv_path, window_size, treshold, people_connections_json_path, exact_distance):
        """
        Task 8: Find indirect connections between characters at an exact distance and return them in JSON format.
        """

        people_connections_preprocessed_handler = PreProcessedHandler(people_connections_json_path)
        people_connections_list = people_connections_preprocessed_handler.extract_people_connections()

        premade_people_connections_graph = None
        if self.preprocessed_flow:
            preprocessed_pairs_handler = PreProcessedHandler(self.preprocessed_json_path)
            preprocessed_people_connections = preprocessed_pairs_handler.extract_processed_pairs()
            premade_people_connections_graph = preprocessed_pairs_handler.build_graph_with_preprocessed_pairs(preprocessed_people_connections)
            # If the graph is premade, threshold doesn't matter
            treshold = 1 # We've pre-built the graph, so every connection's weight is not 1 - and the treshold doesn't matter
        
        processed_sentences, processed_names = self._get_processed_data(sentences_csv_path, names_csv_path, unwanted_words_csv_path)
        
        characters_names_and_nicknames_dict = create_names_and_nicknames_dict(processed_names)
        characters_analyzer = CharactersAnalyzer(characters_names_and_nicknames_dict, processed_sentences)

        characters_direct_connections = characters_analyzer.determinate_connections_of_exact_length(
            people_connections_list, window_size, treshold, exact_distance, premade_people_connections_graph
        )

        result_json = {
            "Question 8": {
                "Pair Matches": characters_direct_connections
            }
        }

        return json.dumps(result_json, indent=JSON_INDENT)



    def run_task_9(self, sentences_csv_path, unwanted_words_csv_path, treshold):
        """
        Task 9: Group sentences based on a threshold of common words and return the result in JSON format.
        """

        processed_sentences, _ = self._get_processed_data(sentences_csv_path, None, unwanted_words_csv_path)
        
        sentences_analyzer = SentencesAnalyzer(processed_sentences)
        sentences_groups = sentences_analyzer.get_sorted_sentences_groups(treshold)


        result_json = {
            "Question 9": {
                "group Matches": sentences_groups
            }
        }

        return json.dumps(result_json, indent=JSON_INDENT)



