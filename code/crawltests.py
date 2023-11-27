import unittest
from main import crawl, generate_graph

class TestCrawl(unittest.TestCase):

    def setUp(self):
        data = '../cs5800-project/data/Data.xlsx'
        self.graph, self.vertices = generate_graph(data)
        self.start_vertex_name = "Roux Institute"

    def test_setup(self):
        # Check if graph and vertices are not None
        self.assertIsNotNone(self.graph, "Graph is not initialized")
        self.assertIsNotNone(self.vertices, "Vertices are not initialized")
        
        # Check if the graph has the expected number of vertices
        expected_vertex_count = 16 
        self.assertEqual(len(self.graph.vertices), expected_vertex_count, "Graph does not have the expected number of vertices")

    def test_max_breweries_constraint(self):
        # Test maximum number of breweries constraint
        max_breweries = 5
        path, _, _ = crawl(self.graph, self.start_vertex_name, max_breweries=max_breweries)
        brewery_count = sum(1 for vertex in path if vertex.name != "Roux Institute")
        path_str = ' -> '.join(vertex.name for vertex in path)
        self.assertEqual(brewery_count, max_breweries, f"Brewery count {brewery_count} does not match max breweries {max_breweries}. Path: {path_str}")
        print(f"Test Max Breweries Path: {path_str}")

    def test_max_walking_time_constraint(self):
        # Test the constraint of maximum walking time
        max_walking_time = 30
        path, _, total_walk_time = crawl(self.graph, self.start_vertex_name, max_walking_time=max_walking_time)
        path_str = ' -> '.join(vertex.name for vertex in path)
        self.assertLessEqual(total_walk_time, max_walking_time, f"Total walk time {total_walk_time} exceeds max walking time {max_walking_time}. Path: {path_str}")
        print(f"Test Max Walking Time Path: {path_str}")
        print(f"Total Walk Time: {total_walk_time} minutes")

    def test_time_limit_constraint(self):
        # Test the constraint of overall time limit
        time_limit = 60 
        path, total_time_spent, _ = crawl(self.graph, self.start_vertex_name, time_limit=time_limit)
        path_str = ' -> '.join(vertex.name for vertex in path)
        print(f"Test Time Limit Path: {path_str}")
        print(f"Total Time Spent: {total_time_spent} minutes")
        self.assertLessEqual(total_time_spent, time_limit, f"Total time spent {total_time_spent} exceeds time limit {time_limit}. Path: {path_str}")
    
    def test_combined_max_breweries_and_walking_time(self):
        # Test the constraint of maximum number of breweries and maximum walking time
        max_breweries = 5
        max_walking_time = 30
        path, _, total_walk_time = crawl(self.graph, self.start_vertex_name, max_breweries=max_breweries, max_walking_time=max_walking_time)
        brewery_count = sum(1 for vertex in path if vertex.name != "Roux Institute")
        path_str = ' -> '.join(vertex.name for vertex in path)
        self.assertLessEqual(brewery_count, max_breweries, f"Visited {brewery_count} breweries, which exceeds the max limit of {max_breweries}. Path: {path_str}")
        self.assertLessEqual(total_walk_time, max_walking_time, f"Total walk time {total_walk_time} minutes exceeds max walking time {max_walking_time} minutes. Path: {path_str}")
        print(f"Test Combined Max Breweries and Walking Time Path: {path_str}, Walk Time: {total_walk_time} minutes")

    def test_combined_total_time_and_max_breweries(self):
        # Test that the crawl adheres to both maximum number of breweries and maximum walking time constraints
        max_breweries = 5
        time_limit = 60
        path, total_time_spent, _ = crawl(self.graph, self.start_vertex_name, max_breweries=max_breweries, time_limit=time_limit)
        brewery_count = sum(1 for vertex in path if vertex.name != "Roux Institute")
        path_str = ' -> '.join(vertex.name for vertex in path)
        self.assertLessEqual(brewery_count, max_breweries, f"Visited {brewery_count} breweries, which exceeds the max limit of {max_breweries}. Path: {path_str}")
        self.assertLessEqual(total_time_spent, time_limit, f"Total time spent {total_time_spent} exceeds time limit {time_limit}. Path: {path_str}")
        print(f"Test Combined Total Time and Max Breweries Path: {path_str}, Total Time Spent: {total_time_spent} minutes")

    def test_combined_all_constraints(self):
        # Test that the crawl adheres to both overall time limit and maximum number of breweries constraints
        max_breweries = 5
        max_walking_time = 30
        time_limit = 60
        path, total_time_spent, total_walk_time = crawl(self.graph, self.start_vertex_name, max_breweries=max_breweries, max_walking_time=max_walking_time, time_limit=time_limit)
        brewery_count = sum(1 for vertex in path if vertex.name != "Roux Institute")
        path_str = ' -> '.join(vertex.name for vertex in path)
        self.assertLessEqual(brewery_count, max_breweries, f"Visited {brewery_count} breweries, which exceeds the max limit of {max_breweries}. Path: {path_str}")
        self.assertLessEqual(total_walk_time, max_walking_time, f"Total walk time {total_walk_time} exceeds max walking time {max_walking_time}. Path: {path_str}")
        self.assertLessEqual(total_time_spent, time_limit, f"Total time spent {total_time_spent} exceeds time limit {time_limit}. Path: {path_str}")
        print(f"Test Combined All Constraints Path: {path_str}, Walk Time: {total_walk_time} minutes, Total Time Spent: {total_time_spent} minutes")

if __name__ == '__main__':
    unittest.main()