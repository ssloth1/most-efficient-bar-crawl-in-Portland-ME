import pandas as pd
import heapq
import os
from dotenv import load_dotenv

class Vertex:
    """
    A class that represents a vertex in a graph. 
    Each vertex really just represents the name of the breweries we are interested in.
    """

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name
    
    def __repr__(self):
        return self.name

class Graph:
    """
    A class to represent a graph, or in the context of the project, our cluster of breweries.
    Each brewery is a vertex and the edges are the walking distances between them. 
    """

    def __init__(self):
        self.vertices = set()
        self.edges =  {}

    # Method to add a vertex to the graph.
    def add_vertex(self, vertex):
        self.vertices.add(vertex)
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
        Return: Dictionary of shortest distances from start to all other vertices
        '''
        # Set all distances to positive infinity 
        distances = {}
        for vertex in self.vertices:
            distances[vertex] = float('inf')
        distances[start_vertex] = 0

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

                # If new distance is less than the previous
                if new_distance < distances[neighbor]:
                    # Update the distance to this neighbor
                    distances[neighbor] = new_distance
                    # Add neighbor to priority queue
                    heapq.heappush(priority_queue, (new_distance, neighbor.name))

        return distances

def find_nearest_unvisited(graph, start_vertex, visited):
    '''
    Uses Dijkstra's algorithm to find the nearest unvisited vertex. 
    Parameters: a graph, a starting vertex, and a list of visited vertices
    Return: The nearest unvisited vertex and its distance from the start_vertex
    '''

    distances = graph.dijkstra(start_vertex)

    nearest = None
    min_distance = float('inf')
    
    # Loop through distance dictionary
    for vertex, distance in distances.items():
        # If the vertex has not been visited and its distance is less than the current minimum
        if vertex not in visited and distance < min_distance:
            # Update nearest vertex and minimum distance
            nearest = vertex
            min_distance = distance

    return nearest, min_distance

def generate_graph(path):
    """
    Generates the graph data from the excel file with our breweries and walking distances.

    args: 
    path: Path to the excel file with the data.

    returns:
    graph: a dictionary representing the graph. Each key is a location, 
    and its value is a dictionary of neighboring locations and their corresponding walk distance values.
    """
    graph = Graph()
    graph_data = pd.read_excel(path, index_col=0)

    # Add the vertices
    vertices = {name: Vertex(name) for name in graph_data.columns}
    for vertex in vertices.values():
        graph.add_vertex(vertex)
        # print(f"Added vertex: {vertex}")  # To help with debugging

    # Add the edges
    for i in graph_data.index:
        for j in graph_data.columns:
            i = i.strip() # Removes any extra spaces in the spreadsheet.
            j = j.strip()
            if i != j and pd.notna(graph_data.at[i, j]):
                weight = graph_data.at[i, j]
                graph.add_edge(vertices[i], vertices[j], weight)

    return graph, vertices

def main():
    load_dotenv()
    path = os.getenv('DATA_PATH')
    graph, vertices = generate_graph(path) 

    start_vertex_name = "Roux Institute"

    # Get start vertex object from dictionary of vertices
    start_vertex = vertices[start_vertex_name]

    visited = set()
    current_vertex = start_vertex
    walking_path = [current_vertex]
    total_time = 0

    # Loop until all vertices in the graph have been visited
    while len(visited) < len(graph.vertices):
        visited.add(current_vertex)
        # Get the nearest unvisited vertex and the time to get there
        next_vertex, minutes = find_nearest_unvisited(graph, current_vertex, visited)
        
        # End loop when there no more unvisited vertices
        if next_vertex is None:
            break
        
        walking_path.append(next_vertex)
        total_time += minutes
        current_vertex = next_vertex

    print("Walking tour path: ", end="")
    first_vertex = True
    for vertex in walking_path:
        if first_vertex == False:
            print(" -> ", end="")
        print(vertex.name, end="")
        first_vertex = False

    print("\n Total travel time:", total_time, "minutes") 

if __name__ == '__main__':
    main()