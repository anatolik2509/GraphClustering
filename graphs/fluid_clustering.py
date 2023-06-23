import random
from random import Random

import networkx as nx
from networkx import all_neighbors

from graphs.graph_utils import WEIGHT_LABEL


def fluid_communities(graph: nx.Graph, weights: list, max_iter=100):
    random = Random()
    k = len(weights)
    total_weight = 0
    for node in graph.nodes:
        total_weight += graph.nodes[node][WEIGHT_LABEL]
    node_to_partitions = {}
    partitions = [[] for _ in range(k)]
    volumes = [w * total_weight for w in weights]
    start_nodes = random.sample(list(graph.nodes), k)
    for i, node in enumerate(start_nodes):
        node_to_partitions[node] = i
    density = __calculate_density(graph, node_to_partitions, volumes)
    old_partitions = {}
    while not __equals_partitions(old_partitions, node_to_partitions) and max_iter > 0:
        old_partitions = node_to_partitions
        node_to_partitions = __fluid_iter(graph, density, node_to_partitions, k)
        density = __calculate_density(graph, node_to_partitions, volumes)
        max_iter -= 1
    for node, part in node_to_partitions.items():
        partitions[part].append(node)
    return partitions


def __equals_partitions(old_partitions: dict, new_partitions: dict):
    for key in new_partitions.keys():
        if key not in old_partitions or old_partitions[key] != new_partitions[key]:
            return False
    return True


def __fluid_iter(graph: nx.Graph, density: list, node_to_partitions: dict, k):
    nodes = [node for node in graph.nodes]
    new_partitions = {}
    random.shuffle(nodes)
    for node in nodes:
        part = __find_closest_partition(graph, node, density, node_to_partitions, k)
        if part == -1:
            continue
        new_partitions[node] = part
    __fix_destroyed_partition(new_partitions, node_to_partitions, k)
    return new_partitions


def __find_closest_partition(graph: nx.Graph, node, density: list, node_to_partitions: dict, k):
    neighbors = set(all_neighbors(graph, node))
    edges_weights = get_neighbors_edges_weights(graph, node, neighbors)
    neighbors.add(node)
    partitions_pressure = {part: 0 for part in range(k)}
    at_least_one_partition_found = False
    for neighbor in neighbors:
        if neighbor not in node_to_partitions:
            continue
        at_least_one_partition_found = True
        partitions_pressure[node_to_partitions[neighbor]] += density[node_to_partitions[neighbor]] * edges_weights[(node, neighbor)]
    if not at_least_one_partition_found:
        return -1
    max_partition = max(partitions_pressure.keys(), key=lambda key: partitions_pressure[key])
    return max_partition


def get_neighbors_edges_weights(graph: nx.Graph, node, neighbors):
    edge_to_weights = {}
    for neighbor in neighbors:
        edge_from = graph.get_edge_data(node, neighbor)
        edge_in = graph.get_edge_data(neighbor, node)
        edge_from_weight = edge_from[WEIGHT_LABEL] if edge_from is not None else 0
        edge_in_weight = edge_in[WEIGHT_LABEL] if edge_in is not None else 0
        edge_to_weights[(node, neighbor)] = edge_from_weight + edge_in_weight
    edge_to_weights[(node, node)] = max(edge_to_weights.values())
    return edge_to_weights


def __fix_destroyed_partition(new_partitions, old_partitions, k):
    partition_to_count = {part: 0 for part in range(k)}
    for node, part in new_partitions.items():
        partition_to_count[part] += 1
    for part, count in partition_to_count.items():
        if count == 0:
            for node, old_part in old_partitions.items():
                if part == old_part:
                    new_partitions[node] = old_part
                    __fix_destroyed_partition(new_partitions, old_partitions, k)
                    break


def __calculate_density(graph: nx.Graph, node_to_partitions: dict, volumes):
    density = [0] * len(volumes)
    partitions_to_weight = {part: 0 for part in range(len(volumes))}
    for node, part in node_to_partitions.items():
        partitions_to_weight[part] += graph.nodes[node][WEIGHT_LABEL]
    for edge in graph.edges:
        if edge[0] in node_to_partitions and edge[1] in node_to_partitions:
            if node_to_partitions[edge[0]] == node_to_partitions[edge[1]]:
                partitions_to_weight[node_to_partitions[edge[0]]] += graph.edges[edge][WEIGHT_LABEL]
    for part, weight in partitions_to_weight.items():
        density[part] = volumes[part] / weight
    return density
