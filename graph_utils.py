from random import Random

import networkx as nx
import matplotlib.pyplot as plt

WEIGHT_LABEL = 'weight'


def add_random_weights_to_nodes(graph: nx.Graph, min_weight, max_weight) -> nx.Graph:
    rand = Random()
    for node in graph.nodes:
        graph.nodes[node][WEIGHT_LABEL] = rand.randint(min_weight, max_weight)
    return graph


def draw_graph(graph: nx.Graph, partitions: list):
    pos = nx.kamada_kawai_layout(graph)
    node_weights = nx.get_node_attributes(graph, WEIGHT_LABEL)
    colors = ['green', 'blue', 'yellow']
    node_colors = [''] * len(graph.nodes)
    for i, part in enumerate(partitions):
        for node in part:
            node_colors[node] = colors[i]
    for node in node_weights:
        node_weights[node] = f"{node} ({node_weights[node]})"
    edge_weights = nx.get_edge_attributes(graph, WEIGHT_LABEL)
    nx.draw_networkx_nodes(graph, pos, node_size=600, node_color=node_colors)
    nx.draw_networkx_labels(graph, pos, labels=node_weights, font_size=9)
    nx.draw_networkx_edges(graph, pos)
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_weights, font_size=7)
    plt.show()
