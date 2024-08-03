import networkx as nx
import matplotlib.pyplot as plt
import random


def generate_complate_graph(num_nodes, weight_range=(1, 100)):
    G = nx.complete_graph(num_nodes)
    for u, v in G.edges():
        G[u][v]['weight'] = random.randint(*weight_range)

    return G

#print(generate_complate_graph(5).edges())

#Info : tour = [1,2,3,4,5] --> zip(list(tour, tour[1:]) ---> [(1,2),(2,3),(3,4)(4,5)
def plot_graph_step(G, tour, current_node , pos):
    #plt.clf()
    nx.draw(G, pos, with_labels=True, node_color='lightblue',node_size=500)
    path_edges = list(zip(tour, tour[1:]))
    nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='red', width=20)
    nx.draw_networkx_nodes(G, pos, nodelist=[current_node], node_color='green', node_size=500)

    edge_labels = nx.get_edge_attributes(G,'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

    #plt.pause(1)


def calculate_tour_length(G, tour):
    return sum(G[tour[i]][tour[i+1]]['weight'] for i in range(len(tour)-1))


def nearest_neighbor_tsp(G,start_node=None):
    if start_node is None:
        start_node = random.choice(list(G.nodes))

    pos = nx.spring_layout(G)
    #plt.ion()
    #plt.show()

    unvisited_nodes = list(G.nodes)
    unvisited_nodes.remove(start_node)
    tour = [start_node]
    current_node = start_node

    plot_graph_step(G, tour, current_node, pos)
    while unvisited_nodes:
        next_node = min(unvisited_nodes, key=lambda node: G[current_node][node]['weight'])
        unvisited_nodes.remove(next_node)
        tour.append(next_node)
        current_node = next_node
        plot_graph_step(G, tour, current_node, pos)

    tour.append(start_node)
    plot_graph_step(G, tour, current_node, pos)

    print(tour)
    tour_length = calculate_tour_length(G, tour)
    print(f'Total tour length: {tour_length}')

  #  plt.ioff()
   # plt.show()



if __name__ == '__main__':
    G = generate_complate_graph(10)
    nearest_neighbor_tsp(G, 1)



