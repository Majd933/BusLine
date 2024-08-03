import networkx as nx
import random
import math
import Graph as gr

def ant_colony_optimization(graph, demand, ants=50, iterations=100, evaporation_rate=0.5, alpha=1.0, beta=2.0):
    """
    Perform Ant Colony Optimization to minimize total travel distance in a bus network.

    Parameters:
    graph (networkx.Graph): The bus network graph.
    demand (dict): Demand between nodes.
    ants (int): Number of ants to simulate.
    iterations (int): Number of iterations to perform.
    evaporation_rate (float): Rate at which pheromones evaporate.
    alpha (float): Influence of pheromone on direction.
    beta (float): Influence of heuristic (inverse distance) on direction.

    Returns:
    networkx.Graph: Optimized graph with improved routes.
    """
    # Initialize pheromone levels for all edges in both directions
    pheromone_levels = {(u, v): 1.0 for u, v in graph.edges()}
    pheromone_levels.update({(v, u): 1.0 for u, v in graph.edges()})

    def update_pheromones(solutions, best_solution):
        for edge in pheromone_levels:
            pheromone_levels[edge] *= (1 - evaporation_rate)
        for solution in solutions:
            for u, v in solution.edges():
                # Ensure the pheromone levels dictionary is accessed correctly
                if (u, v) in pheromone_levels:
                    pheromone_levels[(u, v)] += 1.0 / calculate_total_distance(solution, demand)
                elif (v, u) in pheromone_levels:
                    pheromone_levels[(v, u)] += 1.0 / calculate_total_distance(solution, demand)

        # Increase pheromones on the best solution path to promote it
        for u, v in best_solution.edges():
            if (u, v) in pheromone_levels:
                pheromone_levels[(u, v)] += 2.0 / calculate_total_distance(best_solution, demand)
            elif (v, u) in pheromone_levels:
                pheromone_levels[(v, u)] += 2.0 / calculate_total_distance(best_solution, demand)

    def construct_solution():
        solution = nx.Graph()
        for (start, end) in demand.keys():
            path = [start]
            visited = set(path)
            while path[-1] != end:
                last_node = path[-1]
                candidates = [n for n in graph.neighbors(last_node) if n not in visited]
                probabilities = []
                for next_node in candidates:
                    pheromone = pheromone_levels.get((last_node, next_node), 1.0)
                    distance = graph[last_node][next_node]['weight']
                    probability = (pheromone ** alpha) * ((1.0 / distance) ** beta)
                    probabilities.append(probability)
                if not probabilities:
                    break  # Dead end
                probabilities_sum = sum(probabilities)
                probabilities = [p / probabilities_sum for p in probabilities]
                next_node = random.choices(candidates, probabilities)[0]
                path.append(next_node)
                visited.add(next_node)
                solution.add_edge(last_node, next_node, weight=graph[last_node][next_node]['weight'])
        return solution

    best_solution = None
    best_distance = float('inf')
    for iteration in range(iterations):
        solutions = [construct_solution() for _ in range(ants)]
        for solution in solutions:
            distance = calculate_total_distance(solution, demand)
            if distance < best_distance:
                best_solution = solution
                best_distance = distance
        update_pheromones(solutions, best_solution)
        print(f"Iteration {iteration + 1}/{iterations}, Best Distance: {best_distance}")

    return best_solution


def calculate_total_distance(graph, demand):
    total_distance = 0
    for (u, v), num_travelers in demand.items():
        if graph.has_edge(u, v):
            distance = graph[u][v]['weight']
            total_distance += distance * num_travelers
    return total_distance


# Example usage:

def run_simulation():
    # Create the initial bus network graph (could be an MST)

    G = nx.Graph()
    G.add_edge('Stop1', 'Stop2', weight=5)
    G.add_edge('Stop2', 'Stop3', weight=7)
    G.add_edge('Stop3', 'Stop4', weight=3)
    G.add_edge('Stop4', 'Stop1', weight=6)
    G.add_edge('Stop1', 'Stop3', weight=10)
    G.add_edge('Stop2', 'Stop4', weight=8)

    # Define demand between nodes
    demand = {
        ('Stop1', 'Stop3'): 100,
        ('Stop2', 'Stop4'): 150,
        ('Stop1', 'Stop4'): 50,
        ('Stop2', 'Stop3'): 120,
    }

    # Optimize the network using ACO
    optimized_network = ant_colony_optimization(G, demand)

    # Calculate optimized total distance
    optimized_distance = calculate_total_distance(optimized_network, demand)
    print(f"Optimized Total Distance: {optimized_distance}")


# Run the simulation
run_simulation()
