import pandas as pd
from graph import Graph
from vertex import Vertex

def generate_graph(path, max_weight_threshold=None):
    """
    Generates the graph data from the excel file with breweries and walking distances.

    args: 
        path (str): Path to the excel file with the data.
        max_weight_threshold (int, optional): Threshold for maximum edge weight.

    returns:
    graph: A graph where vertices are locations and edges represent walking distances.
    vertices: A dictionary of vertices.
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
                # Add edge only if weight is below the threshold (if specified)
                if max_weight_threshold is None or weight <= max_weight_threshold:
                    graph.add_edge(vertices[i], vertices[j], weight)


    return graph, vertices

def find_nearest_unvisited(graph, start_vertex, visited):
    '''
    Uses Dijkstra's algorithm to find the nearest unvisited vertex. 

    Parameters: a graph, a starting vertex, and a list of visited vertices
    
    Return: The nearest unvisited vertex and its distance from the start_vertex
    '''

    distances, predecessors = graph.dijkstra(start_vertex)  # Extract only the distances

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
    graph (Graph): The graph representing breweries and walking times.
    start_vertex_name (str): The name of the starting brewery.
    max_breweries (int, optional): Max number of breweries to visit.
    max_walking_time (int, optional): Max total walking time (in minutes).
    time_limit (int, optional): Max total time for the crawl (in minutes).
    time_at_each (int): Time spent at each brewery (default 10 minutes).

    returns:
    tuple: Path of vertices visited, total time, and total walk time.
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

def print_crawl_info(graph, start_vertex_name, max_breweries=None, max_walking_time=None, time_limit=None, time_at_each=10):
    """
    Prints information about the path generated by the crawl function, and calls the crawl function.

    args:
    graph (Graph): The graph representing breweries and walking times.
    start_vertex_name (str): The name of the starting brewery.
    max_breweries, max_walking_time, time_limit, time_at_each: Constraints for the crawl function.
    """
    path, total_time_spent, total_walk_time = crawl(graph, start_vertex_name, max_breweries, max_walking_time, time_limit, time_at_each)

    print("\nWalking tour path via Traveling Salesman/neighbor: ", " --> ".join(vertex.name for vertex in path))
    print("Total time spent: ", total_time_spent)
    print("Total travel time:", total_walk_time, "minutes")
    print("\n")


def print_shortest_path_info(graph, start_vertex, destination_vertex):
    """
    Prints the shortest path and total travel time between two vertices using Dijkstra's algorithm.

    args:
    graph (Graph): The graph representing breweries and walking times.
    start_vertex (Vertex): The starting vertex.
    destination_vertex (Vertex): The destination vertex.
    """
    distances, predecessors = graph.dijkstra(start_vertex)

    total_distance = distances[destination_vertex]

    if total_distance == float('inf'):
        print(f"No path from {start_vertex.name} to {destination_vertex.name}")
        return

    # Construct the shortest path
    path = []
    current_vertex = destination_vertex
    while current_vertex is not None:
        path.insert(0, current_vertex.name)
        current_vertex = predecessors[current_vertex]

    # Print the shortest path and travel time.
    print(f"Shortest path from {start_vertex.name} to {destination_vertex.name}: {' --> '.join(path)}")
    print(f"Total travel time: {total_distance} minutes")    


def main():
    
    # This is the path to the vanilla spreadsheet of our walking times. 
    # The only thing different about this one is there are no edges directed toward the Roux Institute.
    path = '../cs5800-project/data/Data.xlsx'

    # Demonstrates a more simple approach to our problem, using Dijkstra's algorithm purely. 
    # Currently the only constraint added here is setting a weight threshold in graph generation.
    # This is akin to saying we don't want to walk more than the specificed minutes between breweries.
    graph1, vertices1 = generate_graph(path, max_weight_threshold=10)
    print_shortest_path_info(graph1, vertices1["Roux Institute"], vertices1["Belleflower"])

    print("\n ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ \n")

    # Demonstrates the heuristic/traveling salesman approach to our problem.
    # Currently, this offers more constraints than the purely Dijkstra approach, 
    # including a max number of breweries, max walking time, and overall time limit.
    graph2, vertices2 = generate_graph(path)
    print_crawl_info(graph2, "Roux Institute", max_breweries=5, max_walking_time=60, time_limit=120, time_at_each=10)

if __name__ == '__main__':
    main()