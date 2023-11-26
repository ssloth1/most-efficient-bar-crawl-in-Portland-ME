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