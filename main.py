import clustering
import graph_generator
import graph_utils
import networkx as nx


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
    partition_old_loses = []
    partition_new_loses = []
    for _ in range(1):
        clusters_weights = [0.1, 0.4, 0.2, 0.3]
        partitions_old = nx.community.asyn_fluidc(g, 4)
        partitions_old = [part for part in partitions_old]
        partition_old_loses.append(graph_utils.clustering_loss(g, partitions_old, clusters_weights))
        graph_utils.draw_graph(g, partitions_old)
        partitions_new = clustering.fluid_communities(g, clusters_weights)
        partition_new_loses.append(graph_utils.clustering_loss(g, partitions_new, clusters_weights))
        graph_utils.draw_graph(g, partitions_new)
    print(mean_loss(partition_old_loses))
    print(mean_loss(partition_new_loses))

