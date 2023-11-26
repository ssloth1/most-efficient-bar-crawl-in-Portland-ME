import pandas as pd
from graph import Graph
from vertex import Vertex

def generate_graph(path):
    """
    Generates the graph data from the excel file with our breweries and walking distances.

    args: 
    path: Path to the excel file with the data.

    returns:
    graph (Graph): a dictionary representing the graph. Each key is a location, 
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

    return graph, vertices


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


def crawl(graph, start_vertex_name, max_breweries=None, max_walking_time=None, time_limit=None, time_at_each=10):
    """
    Constructs a path through the graph using the nearest neighbor approach, starting from the given vertex.
    The path may be constrained by the minimum and maximum number of breweries to visit, the maximum walking time, or the overall time limit.

    args:
    graph (Graph): the graph representing the network of breweries and the walking times between them.
    start_vertex_name (string): the name of the starting vertex (brewery) for the crawl.
    max_breweries (integer, optional): maximum number of breweries to include in the crawl.
    max_walking_time (int, optional): maximum total walking time desired for the crawl (in minutes).
    time_limit (int, optional): maximum total time for the crawl (in minutes), including time spent at each brewery.

    returns:
    tuple: A list representing the path of vertices visited and the total time of the crawl.
    """
    start_vertex = graph.vertices_dict[start_vertex_name] 
    visited = set() # need to track visited vertices to avoid revisits
    path = [start_vertex] # initialize path with the start vertex
    total_time_spent = 0 # time spent in total (including time at each brewery and walking time)
    total_walk_time = 0 # time spent walking (not including time at each brewery)
    brewery_count = 0 # number of breweries visited

    while True:
        current_vertex = path[-1] # current position in the crawl
        visited.add(current_vertex) # count it as visited

        # find the nearest unvisited vertex
        nearest, distance = find_nearest_unvisited(graph, current_vertex, visited)

        # if there are no more unvisited vertices, or if the nearest vertex is already visited, stop
        if nearest is None or nearest in visited:
            break
        
        # if the nearest vertex is not the Roux Institute, add the time spent at each brewery to the total time spent
        # we don't add time spent at the Roux Institute because in this context as it isn't a brewery. 
        next_vertex_time = total_time_spent + distance + (time_at_each if nearest.name != "Roux Institute" else 0)

        # if the next vertex would violate any of the constraints, stop
        if (max_walking_time is not None and total_walk_time + distance > max_walking_time) or \
           (max_breweries is not None and brewery_count >= max_breweries) or \
           (time_limit is not None and next_vertex_time > time_limit):
            break
        
        # add the nearest vertex to the path and update the total time spent and total walk time
        path.append(nearest)
        total_walk_time += distance
        total_time_spent += distance

        # increment brewery count and add time at the brewery if it's not the Roux Institute
        if nearest.name != "Roux Institute":
            brewery_count += 1
            total_time_spent += time_at_each

    return path, total_time_spent, total_walk_time

def main():
   
    path = '../cs5800-project/data/Data.xlsx'
    graph, vertices = generate_graph(path) 
    start_vertex_name = "Roux Institute"

    #Get a route following a nearest neighbor solution.
    path, total_time_spent, total_walk_time = crawl(graph, start_vertex_name)
    print("\nWalking tour path via Traveling Salesman/neighbor: ", " -> ".join(vertex.name for vertex in path))
    print("Total time spent: ", total_time_spent)
    print("Total travel time:", total_walk_time, "minutes")
    print("\n")

if __name__ == '__main__':
    main()