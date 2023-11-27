import heapq
from vertex import Vertex

class Graph:
    """
    A class to represent a graph, or in the context of the project, our cluster of breweries.
    Each brewery is a vertex and the edges are the walking distances between them. 
    """

    def __init__(self):
        self.vertices = set()
        self.edges =  {}
        self.vertices_dict = {}

    # Method to add a vertex to the graph.
    def add_vertex(self, vertex):
        self.vertices.add(vertex)
        self.vertices_dict[vertex.name] = vertex
        if vertex not in self.edges:
            self.edges[vertex] = {}
    
    # Method to add an edge to the graph. 
    def add_edge(self, vertex_a, vertex_b, weight):
        if vertex_a != vertex_b: # we don't want to consider self loops
            self.edges[vertex_a][vertex_b] = weight
    
    # String representation of a graph as an adjacency list.
    def __str__(self):
        graph = "Graph:\n"
        for vertex in self.vertices:
            connections = [f"{str(neighbor)}({self.edges[vertex].get(neighbor, 'NA')})" for neighbor in self.vertices if neighbor != vertex]
            graph += f"{str(vertex)} -> {', '.join(connections)}\n"
        return graph

    def dijkstra(self, start_vertex):
        '''
        Implementation of Dijkstra's algorithm

        Parameters: Starting vertex

        Return: A tuple of two dictionaries - distances and predecessors

        distances: A dictionary of distances from the starting vertex to each vertex in the graph
        predecessors: A dictionary of predecessors for each vertex in the the shortest path from the starting vertex
        '''
        # Initialize distances dictionary, and set all distances to positive infinity 
        distances = {}
        for vertex in self.vertices:
            distances[vertex] = float('inf')
        distances[start_vertex] = 0

        # Initialize predecessors dictionary
        predecessors = {}
        for vertex in self.vertices:
            predecessors[vertex] = None

        # Create priority queue and add starting vertex with distance of 0
        priority_queue = []
        heapq.heappush(priority_queue, (0, start_vertex.name))

        # Keep track of visited vertices
        visited = set()

        # Loop until queue is empty
        while len(priority_queue) > 0:
            # Pop the vertex with the smallest distance
            current = heapq.heappop(priority_queue)
            current_distance = current[0]
            current_vertex_name = current[1]
            current_vertex = None
            
            # Find the vertex object based on the name
            for vertex in self.vertices:
                if vertex.name == current_vertex_name:
                    current_vertex = vertex
                    break

            # Check if vertex has been visited
            if current_vertex in visited:
                continue

            # Mark current vertex as visited
            visited.add(current_vertex)

            # Check all neighbors of current vertex
            for neighbor in self.edges[current_vertex]:
                weight = self.edges[current_vertex][neighbor]
                # Calculate the new potential distance to this neighbor
                new_distance = current_distance + weight

                # Update the distance and predecesseor if a shorter path is found
                if new_distance < distances[neighbor]:
                    distances[neighbor] = new_distance
                    predecessors[neighbor] = current_vertex
                    heapq.heappush(priority_queue, (new_distance, neighbor.name))

        return distances, predecessors