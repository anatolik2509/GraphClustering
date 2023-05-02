import networkx as nx

from graphs import graph_generator, graph_utils
from graphs.clustering_algorithm import ClusteringAlgorithm


class FluidClusteringAlgorithm(ClusteringAlgorithm):

    def clustering(self, topology, node_weights):
        if not topology.is_directed():
            clusters = list(nx.community.asyn_fluidc(topology, len(node_weights)))
        else:
            clusters = list(nx.community.asyn_fluidc(topology.to_undirected(), len(node_weights)))
        clusters = [list(cluster) for cluster in clusters]
        return clusters


if __name__ == '__main__':
    g = graph_generator.generate(20, 40)
    g = graph_utils.add_random_weights_to_edges(g, 50, 100)
    g = graph_utils.add_random_weights_to_nodes(g, 50, 100)
    alg = FluidClusteringAlgorithm()
    res = alg.clustering(g, [1, 1, 1])
    print(res)
