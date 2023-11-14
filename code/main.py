import pandas as pd

def generate_graph(path):

    """
    Generates the graph data from the excel file with our breweries and walking distances.

    args: 
    path: Path to the excel file with the data.

    returns:
    graph: a dictionary representing the graph. Each key is a location, 
    and its value is a dictionary of neighboring locations and their corresponding walk distance values.
    """

    # First read in the data from the excel spreadsheet into a pandas dataframe.
    graph_data = pd.read_excel(path)

    # Now iterate through the dataframe and create a dictionary representing the graph.
    graph = {}
    for index, row in graph_data.iterrows():

        location = row[0] # the first element of the row is the location (vertex/node)

        # Create a dictionary representing edges/walking distances from the location.
        # the key is the neighbor of the location and the value is the edge weight. 
        edges = {graph_data.columns[i]: row[i] for i in range(1, len(graph_data.columns))}
        graph[location] = edges

    return graph

def main():
    path = '../cs5800-project/data/Data.xlsx'
    graph = generate_graph(path)
    #print(graph)
if __name__ == '__main__':
    main()





