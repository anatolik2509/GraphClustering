import numpy as np

import graphs
import graph_generator
import graph_utils
import networkx as nx
import kmedoids

from graphs.fluid_clustering import fluid_communities
from graphs.spin_glass_clustering_algorithm import SpinGlassClusteringAlgorithm
from graphs.weighted_fluid_clustering_algorithm import WeightedFluidClusteringAlgorithm


def mean_loss(losses: list):
    node_sum = 0
    edge_sum = 0
    for loss in losses:
        node_sum += loss[0]
        edge_sum += loss[1]
    return node_sum / len(losses), edge_sum / len(losses)


if __name__ == '__main__':
    g = graph_generator.generate(20, 30)
    g = graph_utils.add_random_weights_to_nodes(g, 50, 100)
    g = graph_utils.add_random_weights_to_edges(g, 50, 100)
    partition_fluidc_loses = []
    partition_spin_glass_loses = []
    wf = WeightedFluidClusteringAlgorithm()
    sg = SpinGlassClusteringAlgorithm()
    for _ in range(1000):
        clusters_weights = [1.0, 0.5, 0.5]
        partitions_fluidc = wf.clustering(g, clusters_weights)
        partitions_fluidc = list(partitions_fluidc)
        partition_fluidc_loses.append(graph_utils.clustering_loss(g, partitions_fluidc, clusters_weights))
        # graph_utils.draw_graph(g, partitions_fluidc)
        partitions_spin_glass = sg.clustering(g, clusters_weights)
        partition_spin_glass_loses.append(graph_utils.clustering_loss(g, partitions_spin_glass, clusters_weights))
        # graph_utils.draw_graph(g, partitions_new_fluidc)
    print(mean_loss(partition_fluidc_loses))
    print(mean_loss(partition_spin_glass_loses))
