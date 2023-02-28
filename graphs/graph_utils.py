from random import Random

import networkx as nx
import matplotlib.pyplot as plt

WEIGHT_LABEL = 'weight'


def add_random_weights_to_nodes(graph: nx.Graph, min_weight, max_weight) -> nx.Graph:
    rand = Random()
    for node in graph.nodes:
        graph.nodes[node][WEIGHT_LABEL] = rand.randint(min_weight, max_weight)
    return graph


def add_random_weights_to_edges(graph: nx.Graph, min_weight, max_weight) -> nx.Graph:
    rand = Random()
    for edge in graph.edges:
        graph.edges[edge][WEIGHT_LABEL] = rand.randint(min_weight, max_weight)
    return graph


def draw_graph(graph: nx.Graph, partitions: list):
    pos = nx.kamada_kawai_layout(graph)
    node_weights = nx.get_node_attributes(graph, WEIGHT_LABEL)
    colors = ['green', 'blue', 'yellow', 'red']
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


def clustering_loss(graph: nx.Graph, clusters, cluster_target_weights):
    cluster_weights = list()
    weights_sum = 0
    node_to_clusters = {}
    for c, cluster in enumerate(clusters):
        cluster_weight = 0
        for node in cluster:
            w = graph.nodes[node][WEIGHT_LABEL]
            node_to_clusters[node] = c
            weights_sum += w
            cluster_weight += w
        cluster_weights.append(cluster_weight)

    node_weight_lose = 0
    for i, cluster_weight in enumerate(cluster_weights):
        node_weight_lose += abs(cluster_target_weights[i] - cluster_weight / weights_sum)

    edge_weights_loss = 0
    for edge in graph.edges:
        if node_to_clusters[edge[0]] != node_to_clusters[edge[1]]:
            edge_weights_loss += graph.edges[edge][WEIGHT_LABEL]

    return node_weight_lose, edge_weights_loss



