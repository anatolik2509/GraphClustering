from graphs import graph_generator, graph_utils
from graphs.fluid_clustering import fluid_communities
from graphs.clustering_algorithm import ClusteringAlgorithm


class WeightedFluidClusteringAlgorithm(ClusteringAlgorithm):

    def clustering(self, topology, node_weights):
        return fluid_communities(topology, node_weights)


if __name__ == '__main__':
    g = graph_generator.generate(20, 40)
    g = graph_utils.add_random_weights_to_edges(g, 50, 100)
    g = graph_utils.add_random_weights_to_nodes(g, 50, 100)
    alg = WeightedFluidClusteringAlgorithm()
    res = alg.clustering(g, [1, 1, 1])
    print(res)
