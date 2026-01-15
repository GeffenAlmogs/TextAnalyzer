import json
from graph import Graph, Node, Edge

MAIN_NAME = 0
NICKNAMES = 1

class PreProcessedHandler:
    
    def __init__(self, preprocessed_json_path: str):
        self.preprocessed_json_path = preprocessed_json_path
        


    def extract_processed_sentences(self) -> list[list[str]]:
        try:
            with open(self.preprocessed_json_path, 'r') as file:
                data = json.load(file)

            # Since the file contains only one question, access the first (and only) question
            processed_sentences = data.get("Question 1", {}).get("Processed Sentences", [])
            return processed_sentences
        except:
            print("invalid input: There's a problem with the preprocessed sentences json file.")
            exit()



    def extract_processed_names(self) -> list[list[list[str]]]:
        try:
            with open(self.preprocessed_json_path, 'r') as file:
                data = json.load(file)

            # Since the file contains only one question, access the first (and only) question
            processed_names = data.get("Question 1", {}).get("Processed Names", [])
            return processed_names
        except:
            print("invalid input: There's a problem with the preprocessed names json file.")
            exit()

    

    
    def extract_query_keys(self) -> list[list[str]]:
        try:
            with open(self.preprocessed_json_path, 'r') as file:
                data = json.load(file)
        
        except:
            print("invalid input: There's a problem with the query keys json file.")
            exit()

        try:
            # Since the file contains only one field, access it directly
            query_keys = data['keys']
            return query_keys
        
        except:
            print("invalid input: The query keys json file isn't of the right format.")
            exit()
        

    
    
    
    def extract_people_connections(self) -> list[list[str]]:
        try:
            with open(self.preprocessed_json_path, 'r') as file:
                data = json.load(file)
        
        except:
            print("invalid input: There's a problem with the people connections json file.")
            exit()

        try:
            # Since the file contains only one field, access it directly
            query_keys = data['keys']
            return query_keys
        
        except:
            print("invalid input: The people connections json file isn't of the right format.")
            exit()
    


    def extract_processed_pairs(self) -> list[list[list[str]]]:
        try:
            with open(self.preprocessed_json_path, 'r') as file:
                data = json.load(file)

            # Since the file contains only one question, access the first (and only) question
            processed_pairs = data.get("Question 6", {}).get("Pair Matches", [])
            return processed_pairs
        except:
            print("invalid input: There's a problem with the pairs json file.")
            exit()



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

                if full_character_main_name not in graph.nodes.keys():
                    # Create a new node for this character and add it to the graph
                    character_node = Node(full_character_main_name, [])
                    graph.add_node(character_node)

                # Add the full character name to the pair names list for edge creation
                pair_connection_names.append(full_character_main_name)

            # Create an edge between the two characters in the pair
            # This connects the first character with the second in the pair
            graph.create_edge_between_nodes_by_keys(pair_connection_names[0], pair_connection_names[1])

        return graph