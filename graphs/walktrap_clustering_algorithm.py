import networkx as nx
from igraph import Graph

from graphs import graph_generator, graph_utils
from graphs.clustering_algorithm import ClusteringAlgorithm


class WalktrapClusteringAlgorithm(ClusteringAlgorithm):

    def clustering(self, topology, node_weights):
        ig: Graph = Graph.from_networkx(topology)
        edge_weights = [topology.edges[e][graph_utils.WEIGHT_LABEL] for e in ig.get_edgelist()]
        clusters = [[] for _ in range(len(node_weights))]
        res = ig.community_walktrap(weights=edge_weights).as_clustering(len(node_weights))
        for i, cluster in enumerate(res.membership):
            clusters[cluster].append(i)
        return clusters


if __name__ == '__main__':
    g = graph_generator.generate(20, 40)
    g = graph_utils.add_random_weights_to_edges(g, 50, 100)
    g = graph_utils.add_random_weights_to_nodes(g, 50, 100)
    alg = WalktrapClusteringAlgorithm()
    res = alg.clustering(g, [1, 1, 1])
    print(res)
