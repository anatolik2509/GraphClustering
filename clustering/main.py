import numpy as np

import clustering
import graph_generator
import graph_utils
import networkx as nx
import kmedoids


def mean_loss(losses: list):
    node_sum = 0
    edge_sum = 0
    for loss in losses:
        node_sum += loss[0]
        edge_sum += loss[1]
    return node_sum / len(losses), edge_sum / len(losses)


if __name__ == '__main__':
    g = graph_generator.generate()
    while not nx.is_connected(g):
        g = graph_generator.generate()
    g = graph_utils.add_random_weights_to_nodes(g, 50, 100)
    g = graph_utils.add_random_weights_to_edges(g, 50, 100)
    partition_fluidc_loses = []
    partition_new_fluidc_loses = []
    partition_pam_loses = []
    for _ in range(1000):
        clusters_weights = [0.25, 0.25, 0.25, 0.25]
        partitions_fluidc = nx.community.asyn_fluidc(g, 4)
        partitions_fluidc = list(partitions_fluidc)
        partition_fluidc_loses.append(graph_utils.clustering_loss(g, partitions_fluidc, clusters_weights))
        # graph_utils.draw_graph(g, partitions_fluidc)
        partitions_new_fluidc = clustering.fluid_communities(g, clusters_weights)
        partition_new_fluidc_loses.append(graph_utils.clustering_loss(g, partitions_new_fluidc, clusters_weights))
        # graph_utils.draw_graph(g, partitions_new_fluidc)
        matrix = nx.to_numpy_matrix(g)
        matrix[matrix == 0] = 10000
        partitions_pam = [[] for _ in range(4)]
        for i, l in enumerate(kmedoids.pam(matrix, 4).labels):
            partitions_pam[l].append(i)
        # graph_utils.draw_graph(g, partitions_pam)
        partition_pam_loses.append(graph_utils.clustering_loss(g, partitions_pam, clusters_weights))

    print(mean_loss(partition_fluidc_loses))
    print(mean_loss(partition_new_fluidc_loses))
    print(mean_loss(partition_pam_loses))
