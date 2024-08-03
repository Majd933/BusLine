import random

import networkx as nx
import matplotlib.pyplot as plt
import ExcelClass as ex
import numpy as np
from heapq import heappop, heappush

# Get the distance matrix
distance_matrix, labels = ex.getDistanceMatrix()
def creating_road_graph():

    # Step 3: Create an undirected graph
    G = nx.DiGraph()

    # Step 4: Add edges with weights to the graph
    for i in range(len(distance_matrix)):  ##len(distance_matrix)
        for j in range(len(distance_matrix)):
            if distance_matrix[i][j] > 0:  # assuming 0 means no connection
                G.add_edge(labels[i], labels[j], weight=distance_matrix[i][j])

    #print(np.array(G.edges()))


    #pos = nx.spring_layout(G, seed=82)
    #pos = nx.circular_layout(G)
    #pos = nx.spring_layout(G)

    ##plt.figure(figsize=(12, 8))
    #nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=500, font_size=10, edge_color='gray')

    # Add edge labels
    edge_labels = nx.get_edge_attributes(G, 'weight')
    #nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

    # Display the graph
    #plt.show()

    return G


# other option:
## 1. get al nodes
## 2. get al eadges between nodes
## 3. create new graph using nearest Nodes to get the complate graph

#creating_road_graph()

## Gready Algrothim to get MST


## Prim's Algorithm
def creating_busline_Prim_graph():
    graph = creating_road_graph()

    """
    Create an MST from the graph using Prim's Algorithm and return the MST.

    Parameters:
    graph (networkx.Graph): The input graph with nodes and weighted edges.

    Returns:
    networkx.Graph: The MST as a new graph.
    """
    mst_edges = []
    visited = set()
    #start_node = list(graph.nodes)[0]
    start_node = random.choice(list(graph.nodes))

    min_heap = [(0, start_node, start_node)]  # (weight, from_node, to_node)

    while min_heap and len(visited) < len(graph.nodes):
        weight, from_node, to_node = heappop(min_heap)

        if to_node in visited:
            continue

        visited.add(to_node)
        if from_node != to_node:  # Avoid the initial dummy edge
            mst_edges.append((from_node, to_node, weight))

        for neighbor, attributes in graph[to_node].items():
            if neighbor not in visited:
                heappush(min_heap, (attributes['weight'], to_node, neighbor))

    # Create the MST graph from the collected edges
    mst_graph = nx.Graph()
    mst_graph.add_weighted_edges_from(mst_edges)

    return mst_graph

##Kruskal Minimum Spanning Tree
def kruskal_mst():
    graph = creating_road_graph()
    """
    Find the Minimum Spanning Tree (MST) using Kruskal's Algorithm.

    Parameters:
    graph (networkx.Graph): The input graph with nodes and weighted edges.

    Returns:
    networkx.Graph: The MST as a new graph.
    """

    def find(parent, i):
        if parent[i] == i:
            return i
        else:
            return find(parent, parent[i])

    def union(parent, rank, x, y):
        xroot = find(parent, x)
        yroot = find(parent, y)

        if rank[xroot] < rank[yroot]:
            parent[xroot] = yroot
        elif rank[xroot] > rank[yroot]:
            parent[yroot] = xroot
        else:
            parent[yroot] = xroot
            rank[xroot] += 1

    mst = nx.Graph()
    edges = sorted(graph.edges(data=True), key=lambda e: e[2]['weight'])

    parent = {}
    rank = {}
    for node in graph.nodes():
        parent[node] = node
        rank[node] = 0

    for u, v, data in edges:
        x = find(parent, u)
        y = find(parent, v)

        if x != y:
            mst.add_edge(u, v, weight=data['weight'])
            union(parent, rank, x, y)

    return mst



##Floyd-Warshall Algorithm:
def optimize_Floyd_Warshall_graph():
    """
    Optimize the graph by minimizing the total distance for travel between any pair of nodes using the Floyd-Warshall Algorithm.

    Parameters:
    graph (networkx.Graph): The input graph with nodes and weighted edges.

    Returns:
    networkx.Graph: The optimized graph with shortest path distances as edge weights.
    """
    graph = creating_road_graph()
    nodes = list(graph.nodes)
    num_nodes = len(nodes)

    # Initialize distance dictionary
    dist = {node: {node: float('inf') for node in nodes} for node in nodes}

    for node in nodes:
        dist[node][node] = 0

    for u, v, data in graph.edges(data=True):
        dist[u][v] = data['weight']
        dist[v][u] = data['weight']

    for k in nodes:
        for i in nodes:
            for j in nodes:
                if dist[i][j] > dist[i][k] + dist[k][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]

    optimized_graph = nx.Graph()

    for u in dist:
        for v in dist[u]:
            if u != v:
                optimized_graph.add_edge(u, v, weight=dist[u][v])

    return optimized_graph



## totacl distance to a graph
def calculate_total_distance(graph):
    """
    Calculate the total distance of all edges in a graph.

    Parameters:
    graph (networkx.Graph): The input graph with nodes and weighted edges.

    Returns:
    float: The total distance of all edges in the graph.
    """
    total_distance = 0
    for u, v, data in graph.edges(data=True):
        total_distance += data.get('weight', 0)
    return total_distance , graph.number_of_edges()


## Results
#total_distance_road_graph , number_of_edges_road = calculate_total_distance(creating_road_graph())
#total_distance_bus_Prim_graph, number_of_edges = calculate_total_distance(creating_busline_Prim_graph())
#total_distance_bus_kruskal_graph, number_of_edges_kruskal = calculate_total_distance(kruskal_mst())
#total_distance_bus_saving_graph = calculate_total_distance(savings_algorithm())
#total_distance_bus_Floyd_Warshall_graph , number_of_edges_Warshall = calculate_total_distance(optimize_Floyd_Warshall_graph())


#print(f'total_distance_road_graph = {total_distance_road_graph}  with Edges : {number_of_edges_road}')
#print(f'total_distance_bus_graph Prims Algorithm = {total_distance_bus_Prim_graph} with Edges : {number_of_edges}')   #total_Prims Algorithm = 70798.13000000002 /70961.45000000001 /69979.70999999999 / 69451.67999999998
#print(f'total_distance_bus_graph kruskal Algorithm = {total_distance_bus_kruskal_graph}  with Edges : {number_of_edges_kruskal}')
#print(f'total_distance_bus_graph Floyd_Warshall Algorithm = {total_distance_bus_Floyd_Warshall_graph}  with Edges : {number_of_edges_Warshall}') #40588833.64999996

#creating_busline_graph()


def creating_tour(graph, tours):

    """
    Create and visualize manual tours on the given graph and calculate their lengths.

    Parameters:
    graph (networkx.Graph): The input graph with nodes and weighted edges.
    tours (list of list of int): A list of four tours, where each tour is a list of node indices.

    Returns:
    list: A list of total distances for the four tours.
    """

    distances = []
    for tour in tours:
        total_distance = 0
        for i in range(len(tour) - 1):
            node1 = tour[i]
            node2 = tour[i + 1]
            if graph.has_edge(node1, node2):
                total_distance += graph[node1][node2]['weight']
            else:
                print(f"Warning: Edge ({node1}, {node2}) does not exist in the graph.")
                total_distance += float('inf')  # Assign a large distance if the edge does not exist
        distances.append(total_distance)
    return distances


    # Ensure we have exactly four tours
    if len(tours) != 4:
        raise ValueError("You must provide exactly four tours.")

    # Calculate distances for the tours
    distances = [calculate_tour_distance(graph, tour) for tour in tours]

    # Print the lengths of the tours
    for i, distance in enumerate(distances):
        print(f"Total distance of tour {i + 1}: {distance}")

    # Visualize the tours
    #pos = nx.spring_layout(graph, seed=42)
    #colors = ['red', 'blue', 'green', 'orange']
    #plt.figure(figsize=(12, 12))

    # Draw the original graph in the background
    #nx.draw(graph, pos, with_labels=False, node_size=50, edge_color='gray')

    #for i, tour in enumerate(tours):
    #    tour_edges = [(tour[j], tour[j + 1]) for j in range(len(tour) - 1)]
    #    nx.draw_networkx_edges(graph, pos, edgelist=tour_edges, edge_color=colors[i], width=2,
     #                           label=f'Tour {i + 1}')
     #   nx.draw_networkx_nodes(graph, pos, nodelist=tour, node_color=colors[i], node_size=100)

    #plt.legend()
    #plt.title("Manual Tours on Graph")
    #plt.show()

    return distances


def calculate_tour_distance(graph, tour):
    """
    Calculate the total distance of a single tour in the graph.

    Parameters:
    graph (networkx.Graph): The input graph with nodes and weighted edges.
    tour (list): A list of nodes representing the tour.

    Returns:
    float: The total distance of the tour.
    """
    total_distance = 0
    for i in range(len(tour) - 1):
        node1 = tour[i]
        node2 = tour[i + 1]
        if graph.has_edge(node1, node2):
            total_distance += graph[node1][node2]['weight']
        else:
            print(f"Warning: Edge ({node1}, {node2}) does not exist in the graph.")
            total_distance += float('inf')  # Assign a large distance if the edge does not exist
    return total_distance
# Example usage:
# Create a sample graph with 150 nodes and random weights
#G = creating_busline_graph()

def print_graph_with_highlighted_nodes(graph, start_node, end_node):
    """
    Visualize the graph using matplotlib and print the edges in the console.

    Parameters:
    graph (networkx.Graph): The input graph.
    """
    # Choose a layout
    pos = nx.spring_layout(graph, seed=42)  # Spring layout for better distribution


    # Draw the graph
    plt.figure(figsize=(12, 12))  # Adjust the figure size for better clarity
    nx.draw(graph, pos, with_labels=True, node_color='lightblue', node_size=300, font_size=8, edge_color='gray',
            linewidths=0.5, font_weight='bold')

    # Highlight the start and end nodes
    nx.draw_networkx_nodes(graph, pos, nodelist=[start_node], node_color='green', node_size=300, label='Start Node')
    nx.draw_networkx_nodes(graph, pos, nodelist=[end_node], node_color='red', node_size=300, label='End Node')


    # Add edge labels
    edge_labels = nx.get_edge_attributes(graph, 'weight')
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels, font_size=6)

    # Highlight and draw edges between the start and end nodes
    path = nx.shortest_path(graph, source=start_node, target=end_node, weight='weight')
    path_edges = list(zip(path, path[1:]))
    nx.draw_networkx_edges(graph, pos, edgelist=path_edges, edge_color='blue', width=2, label='Path')


    # Display the graph
    plt.title("Graph Visualization")
    plt.show()

   # Print the edges in the console
   # print(f"the number of edges are: {graph.number_of_edges()}  they are :")
   # for u, v, data in graph.edges(data=True):
    #    print(f"({u}, {v}, {data['weight']})")

        # Print the edges between the start and end nodes
    print(f"Edges in the path from {start_node} to {end_node}:")
    for u, v in path_edges:
        weight = graph[u][v]['weight']
        print(f"({u}, {v}, {weight})")

##
def get_shortest_path_distance(graph, source, target):
    """
    Get the shortest path distance between two nodes in the graph.

    Parameters:
    graph (networkx.Graph): The input graph with nodes and weighted edges.
    source (node): The starting node.
    target (node): The ending node.

    Returns:
    float: The shortest path distance between the source and target nodes.
    """
    try:
        shortest_path_length = nx.shortest_path_length(graph, source=source, target=target, weight='weight')
        return shortest_path_length
    except nx.NetworkXNoPath:
        return float('inf')  # Return infinity if no path exists between source and target


# Define four manual tours
# Define four manual tours
tours = [
    ['Himmelsthür', 'Linnenkamp', 'Elzer Straße', 'Hauptbahnhof-ZOB', 'Immengarten', 'Breslauer Straße'],
    ['Marienfriedhof', 'Moltkestraße', 'Ostbahnhof', 'Immengarten', 'Hauptbahnhof-ZOB', 'Ostbahnhof'],
    ['Linnenkamp', 'Moltkestraße', 'Breslauer Straße', 'Immengarten', 'Hauptbahnhof-ZOB', 'Ostbahnhof'],
    ['Marienfriedhof', 'Hauptbahnhof-ZOB', 'Elzer Straße', 'Moltkestraße', 'Immengarten', 'Ostbahnhof']
]

one_tour = [ 'Immengarten', 'Moltkestraße']

"""""
resut from first graph
Total distance of tour 1: 11883.64
Total distance of tour 2: 7515.469999999999
Total distance of tour 3: 19344.42
Total distance of tour 4: 8540.35
"""""
# Create and visualize the manual tours, and get their lengths creating_busline_Prim_graph
distances_road_graph = get_shortest_path_distance(creating_road_graph(), one_tour[0],one_tour[1])
distances_kruskal = get_shortest_path_distance(kruskal_mst(),  one_tour[0],one_tour[1])
distances_Prim = get_shortest_path_distance(creating_busline_Prim_graph(),  one_tour[0],one_tour[1])
distances_Floyd_Warshall_graph = get_shortest_path_distance(optimize_Floyd_Warshall_graph(), one_tour[0],one_tour[1])

print(f' distances road_graph : {distances_road_graph}')
print(f' distances kruskal_graph : {distances_kruskal}')
print(f' distances _Prim_graph : {distances_Prim}')
print(f' distances Floyd_Warshall_graph : {distances_Floyd_Warshall_graph}')

print_graph_with_highlighted_nodes(kruskal_mst(), one_tour[0], one_tour[1])
