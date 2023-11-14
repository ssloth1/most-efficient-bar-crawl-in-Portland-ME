import pandas as pd

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
        return  graph
    
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

    # Add the edges
    for i in graph_data.index:
        for j in graph_data.columns:
            i = i.strip() # Removes any extra spaces in the spreadsheet.
            j = j.strip()
            if i != j and pd.notna(graph_data.at[i, j]):
                weight = graph_data.at[i, j]
                graph.add_edge(vertices[i], vertices[j], weight)

    return graph

def main():

    path = '../cs5800-project/data/Data.xlsx'
    graph = generate_graph(path)
    print(graph)

if __name__ == '__main__':
    main()





