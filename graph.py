import copy
import helper

class Edge:

    def __init__(self, verts: set):
        """Initialize edge with a set of vertices."""

        self.weight: int = 0 
        self.verts: set[Node] = verts

    
    def __eq__(self, other):
        """Check if two edges are equal based on vertices."""

        # Check if the type of the compared object is the same
        if type(self) != type(other):
            return False
        
        # Check if the number of vertices in both edges is the same
        if len(self.verts) != len(other.verts):
            return False
        
        # Check if all vertices in the current edge are also present in the other edge
        for ver in self.verts:
            if not ver in other.verts:
                return False
        return True
    
        
    def increment_weight(self):
        """Increment the edge's weight by 1."""
        self.weight += 1
        


class Node:

    def __init__(self, key: str, values: list[str]):
        """Initialize node with a key and associated values."""
        self.key: str = key # The unique identifier for the node
        self.values = values # List of associated values for the node
        self.linked_nodes: list[Node] = []# List of nodes linked to this node
        


class Graph:

    def __init__(self):
        """Initialize an empty graph with nodes and edges."""
        self.nodes : dict[str:Node] = {}
        self.edges: list[Edge] = []
        


    def add_node(self, node: Node) -> bool:
        """Add a node to the graph if it doesn't already exist."""
        if node.key in self.nodes.keys():
            return False # Return False if the node already exists in the graph
        self.nodes[node.key] = node
        return True # Return True if the node was successfully added
    


    def create_edge_between_nodes_by_keys(self, first_node_key, second_node_key) -> bool:
        """
        Create an edge between two nodes identified by their keys and increment the edge's weight.

        Parameters:
        first_node_key (str): The key (unique identifier) of the first node in the graph.
        second_node_key (str): The key (unique identifier) of the second node in the graph.

        Returns:
        bool: True if the edge was successfully created or its weight was incremented, 
            False if either node doesn't exist in the graph.
        """
        
        # Check if both nodes exist in the graph by their keys
        if not (first_node_key in self.nodes.keys() and second_node_key in self.nodes.keys()):
            return False

        # Check if an edge already exists between the two nodes
        node_edge = self.get_edge_by_node_keys(first_node_key, second_node_key)

        # If no edge exists between the nodes, create a new edge
        if node_edge == None:
            first_node: Node = self.nodes[first_node_key]
            second_node: Node = self.nodes[second_node_key]

            node_edge = Edge({first_node, second_node})
            
            first_node.linked_nodes.append(second_node)
            second_node.linked_nodes.append(first_node)

            self.edges.append(node_edge)

        # Increment the weight of the edge (representing the link between the two nodes)
        node_edge.increment_weight()

        return True
    

    
    def get_edge_by_node_keys(self, first_node_key: str, second_node_key: str):
        """
        Retrieve an edge between two nodes identified by their keys.

        Parameters:
        first_node_key (str): The key of the first node in the graph.
        second_node_key (str): The key of the second node in the graph.

        Returns:
        Edge: The edge connecting the two nodes if it exists, or None if no edge exists.
        """
        # O(1) look-up to check if both the source and destination nodes exist in the graph
        if not (first_node_key in self.nodes.keys() and second_node_key in self.nodes.keys()):
            return None
        
        node1 = self.nodes[first_node_key]
        node2 = self.nodes[second_node_key]

        nodes_pair: set = {node1, node2} # Create a set containing the two nodes (unordered)
        node_edge = Edge(nodes_pair) # Create a temporary edge with the nodes pair

        # Iterate through the existing edges in the graph and compare
        for edge in self.edges:
           if edge == node_edge: # If an edge with the same nodes is found, return it
               return edge
           
        return None # If no matching edge was found, return None
        


    def get_connected_pairs(self, threshold: int) -> list[set]:
        """
        Get pairs of nodes that are connected by an edge with weight greater than or equal to a given threshold.

        Parameters:
        threshold (int): The minimum weight for an edge to be considered for the connected pairs.

        Returns:
        list[set]: A list of sets, each containing two nodes (as keys) that are connected by an edge with a weight
                greater than or equal to the threshold.
        """

        # Get all combinations of two nodes from the list of node keys
        all_possible_pairs = helper.get_combinations_of_two(list(self.nodes.keys()))
        # Initialize an empty list to store the connected pairs
        connected_pairs: list[set] = []

        # Iterate through all possible pairs of nodes
        for pair in all_possible_pairs:

            pair_list = list(pair)

            # Retrieve the edge between the two nodes in the current pair (if such exists)
            edge = self.get_edge_by_node_keys(pair_list[0], pair_list[1]) 
            
            # If an edge exists and its weight is greater than or equal to the threshold, add the pair to the result
            if edge != None and edge.weight >= threshold:
                connected_pairs.append(pair)

        return connected_pairs
    

            
    def directly_linked(self, first_node: Node, second_node: Node, threshold: int = 1):
        """
        Check if two nodes are directly linked by an edge with weight greater than or equal to the threshold.

        Parameters:
        first_node (Node): The first node to check.
        second_node (Node): The second node to check.
        threshold (int, optional): The minimum weight for the edge to be considered a valid link. Default is 1.

        Returns:
        bool: True if the two nodes are directly linked by an edge with weight >= threshold, False otherwise.
        """
    
        edge: Edge = self.get_edge_by_node_keys(first_node.key, second_node.key)

        if edge == None:
            return False
        
        return edge.weight >= threshold
    

    
    def check_if_path_exists(self, source_node_key: str, dest_node_key: str, threshold: int = 1):
        """
        Check if there exists a path between two nodes where all edges in the path have weight >= threshold.

        Parameters:
        source_node_key (str): The key of the source node.
        dest_node_key (str): The key of the destination node.
        threshold (int, optional): The minimum weight for edges in the path. Default is 1.

        Returns:
        bool: True if a valid path exists, otherwise False.
        """

        # O(1) look-up to check if both the source and destination nodes exist in the graph 
        if not (source_node_key in self.nodes.keys() and dest_node_key in self.nodes.keys()): 
            return False
        
        source_node = self.nodes[source_node_key]
        dest_node = self.nodes[dest_node_key]

        # Call the recursive method to check for a path between the source and destination
        visited : set = set()
        return self.check_if_path_exists_rec(source_node, dest_node, threshold, visited)
    

        
    def check_if_path_exists_rec(self, source_node: Node, dest_node: Node, threshold: int, visited: set[Node]):
        """
        Recursive helper method to explore if a path exists between the source and destination nodes,
        where all edges meet or exceed the given threshold.

        Parameters:
        source_node (Node): The current node being explored.
        dest_node (Node): The target destination node.
        threshold (int): The minimum weight for edges to be considered part of the path.
        visited (set, optional): A set of nodes already visited to avoid cycles. Default is empty set.

        Returns:
        bool: True if a valid path exists, otherwise False.
        """
        
        # Base case: if the current node is the destination node, return True
        if source_node == dest_node:
            return True
        
        # Mark the current node as visited to avoid revisiting it and prevent infinite loops
        visited.add(source_node)
        # Initilaize a list to hold the next nodes to visit
        to_visit = []
        
        # Explore all nodes directly linked to the current node (neighbors)
        for node in source_node.linked_nodes:
            # Check if the node has not been visited and if there is a valid edge between source and the node
            if not node in visited and self.directly_linked(source_node, dest_node, threshold):
                to_visit.append(node)

        # If there are no more nodes to visit from the current node, return False
        if len(to_visit) == 0:
            return False
        
        # Recursively visit each node in the "to_visit" list
        for node in to_visit:
            if self.check_if_path_exists_rec(node, dest_node, threshold, visited):
                return True # If any node we've visit from the list, is connected to the destination node, return True
            
        return False # Return False if no valid path was found in any of the recursive calls
    


    def path_exists_up_to_length(self, source_node_key: str, dest_node_key: str, threshold: int, max_length: int) -> bool:
        """
        Check if a path exists between two nodes where all edges in the path have weight >= threshold,
        and the total number of edges in the path does not exceed the max_length.

        Parameters:
        source_node_key (str): The key of the source node.
        dest_node_key (str): The key of the destination node.
        threshold (int): The minimum weight for edges to be considered part of the path.
        max_length (int): The maximum allowed number of edges in the path.

        Returns:
        bool: True if a valid path exists within the given constraints, otherwise False.
        """

        # O(1) look-up to check if both the source and destination nodes exist in the graph 
        if not (source_node_key in self.nodes.keys() and dest_node_key in self.nodes.keys()): 
            return False
        
        source_node = self.nodes[source_node_key]
        dest_node = self.nodes[dest_node_key]
        
        # Call the recursive method to check for a path between the source and destination, without exceeding max-length
        visited : set = set()
        return self.path_exists_up_to_length_rec(source_node, dest_node, threshold, max_length, visited)
    


    def path_exists_up_to_length_rec(self, source_node: Node, dest_node: Node, threshold: int, max_length: int, visited: set[Node] = set()):
        """
        Recursive helper method to explore if a path exists between the source and destination nodes, 
        where all edges meet or exceed the given threshold and the path does not exceed max_length.

        Parameters:
        source_node (Node): The current node being explored.
        dest_node (Node): The target destination node.
        threshold (int): The minimum weight for edges to be considered part of the path.
        max_length (int): The maximum allowed number of edges in the path.
        visited (set, optional): A set of nodes already visited to avoid cycles. Default is an empty set.
        current_length (int, optional): The current path length (number of edges visited so far). Default is 0.

        Returns:
        bool: True if a valid path exists, otherwise False.
        """

        # Base case: if the current node is the destination node and the path length is within the allowed limit
        if source_node == dest_node:
            return True
        
        # `max_length` limits the number of edges. Each step decreases it, 
        # and if it reaches zero, no more edges are allowed, returning False.
        if max_length == 0:
            return False
        
        # Add the current node to the visited set to avoid revisiting and causing cycles.
        visited.add(source_node)
        to_visit = []

        # Explore all nodes directly linked to the current node (neighbors)
        # Check if the edge between the source and the destination node meets the threshold weight
        # and ensure that the destination node has not already been visited.
        for node in source_node.linked_nodes:
            if not node in visited and self.directly_linked(source_node, node, threshold):
                to_visit.append(node)

        # If no nodes to visit are found, return False as no valid path exists.
        if len(to_visit) == 0:
            return False
        
        # For each node in the to_visit list, recursively call the function to check if a valid path exists.
        for node in to_visit:
            # Decrease the max_length by 1 as we move one step further down the path.
            if self.path_exists_up_to_length_rec(node, dest_node, threshold, max_length - 1, visited):
                return True # If any recursive call returns True, indicating we've found a path - return True
            
        # If no path is found after visiting all possible nodes, return False.
        return False
    



    def path_exists_exact_length(self, source_node_key: str, dest_node_key: str, threshold: int, length: int) -> bool:
        """
        Check if there exists a path between two nodes where all edges in the path have weight >= threshold.
        and the total number of edges in the path is length.

        Parameters:
        source_node_key (str): The key of the source node.
        dest_node_key (str): The key of the destination node.
        threshold (int, optional): The minimum weight for edges in the path. Default is 1.
        length (int): The only allowed number of edges in the path.

        Returns:
        bool: True if a valid path exists, otherwise False.
        """

        # O(1) look-up to check if both the source and destination nodes exist in the graph 
        if not(source_node_key in self.nodes.keys() and dest_node_key in self.nodes.keys()): 
            return False
        
        source_node = self.nodes[source_node_key]
        dest_node = self.nodes[dest_node_key]

        # Call the recursive method to check for a path between the source and destination
        
        return self.path_exists_exact_length_rec(source_node, dest_node, threshold, length, [])
    

    def path_exists_exact_length_rec(self, source_node: Node, dest_node: Node, threshold: int, length: int, path_stack: list[str]):
        """
        Recursive helper method to determine if a path exists between the source and destination nodes,
        such that the path has an exact length, and all edges meet or exceed the given threshold.

        Parameters:
        source_node (Node): The current node being explored.
        dest_node (Node): The target destination node.
        threshold (int): The minimum weight for edges to be considered part of the path.
        length (int): The exact number of edges the path must have.
        path_stack (list, optional): A list to keep track of the current path (nodes visited so far). Default is an empty list.

        Returns:
        bool: True if a path exists with the exact specified length and threshold condition, otherwise False.


        Loop avoidance:
        - The function prevents revisiting nodes by checking `path_stack` before exploring neighbors.
        - If a neighbor is already in `path_stack`, it is skipped to avoid cycles.

        Note:
        Time-complexity: amount of all possible path in length of exact length <= O(exact_length!)
        Why? It's like trying to position exact-length Nodes in a row
        """

        # Base case: If the current path length matches the required length
        if length == len(path_stack):
            # Check if the current node is the destination node
            if source_node == dest_node:
                return True
            return False  # If not at the destination, return False
        
        # Add the current node to the path stack to track the path taken so far
        path_stack.append(source_node.key)

        # Get the neighbors of the current node that meet the threshold condition
        to_visit = []
        for neighbor_node in source_node.linked_nodes:
            if self.directly_linked(source_node, neighbor_node, threshold):
                to_visit.append(neighbor_node)

        # Explore each neighboring node
        for neighbor_node in to_visit:
            # Skip if the node has already been visited (exists in the current path stack) - node is allowed once i each path
            if neighbor_node.key in path_stack:
                continue

            # Recursively check if a path exists from the neighbor to the destination with the updated path stack
            if self.path_exists_exact_length_rec(neighbor_node, dest_node, threshold, length, path_stack.copy()):
                return True  # Return True if a valid path is found

        # If no path is found after exploring all neighbors, return False
        return False
    
        

    def get_connected_componnets(self):
        """
        Finds all connected components in the graph. A connected component is a group (/set) of nodes where
        each node is reachable from any other node within the same group (/set).

        Returns:
        list[list[str]]: A list of connected components, where each component is represented as a list of node keys.
        
        Note: Worst-Case - we have a fully connected Graph so we run at O(v^2) 
        """

        # Initialize a set of all node keys to visit and an empty list to store the connected components
        nodes_to_visit :set[str] = set(self.nodes.keys())
        connected_componnentes: list[list[str]] = []

        # Continue exploring until all nodes have been visited
        while len(nodes_to_visit) > 0:
            # Pop a node from the set to start exploring its component
            node_key = nodes_to_visit.pop()
            node = self.nodes[node_key]
            
            # List to store nodes within the same connected component (nodes within reaching of the current node)
            nodes_within_reaching:list[str] = []

            # Find all nodes connected to the current node and remove them from the 'nodes_to_visit' set
            self.find_all_connected_nodes_to_node(node, nodes_within_reaching, nodes_to_visit)
            
            # Append the found component (connected nodes) to the result list
            connected_componnentes.append(nodes_within_reaching)
            
        return connected_componnentes
    


    def find_all_connected_nodes_to_node(self, node: Node, nodes_within_reaching: list[str], nodes_to_visit: set[str]):
        """
        Recursively explores all nodes connected to the given node and adds them to the 'nodes_within_reaching' list.
        Also removes visited nodes from the 'nodes_to_visit' set to avoid revisiting them.

        Parameters:
        node (Node): The current node being explored.
        nodes_within_reaching (list[str]): A list to store the keys of nodes that are reachable from the given node.
        nodes_to_visit (set[str]): A set of node keys that still need to be visited.
        
        Note:
        The rumtime complexity here on O(V + E), because for each node, we check all of it's edges once.
        In total, we go over each Edge only once, because we only visit each Edge once, than it won't be repeated.
        We also manage a set of nodes to visit and once we see the current node, we remove it in order to only view it once.
        """
        
        # Add the current node's key to the list of connected nodes
        nodes_within_reaching.append(node.key)

        # Remove the current node from the 'nodes_to_visit' set since it's now visited
        if node.key in nodes_to_visit:
            nodes_to_visit.remove(node.key)

        # Recursively explore all neighbors (linked nodes) of the current node
        for neighbor_node in node.linked_nodes:
            # Visit only unvisited neighbors, and recurse to explore them
            if neighbor_node.key in nodes_to_visit:
                self.find_all_connected_nodes_to_node(neighbor_node, nodes_within_reaching, nodes_to_visit)

        
    """
    ______________________Task 6________________________
    """

    def link_all_names_in_window(self, names_list):
        names_pairs = helper.get_combinations_of_two(names_list)
        for pair in names_pairs:
            pair_to_list = list(pair)
            if not self.create_edge_between_nodes_by_keys(pair_to_list[0], pair_to_list[1]):
                print(f'DEBUG, cannot link {pair}')