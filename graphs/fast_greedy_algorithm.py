from graphs.clustering_algorithm import ClusteringAlgorithm

from igraph import Graph
from graphs import graph_utils
from graphs import graph_generator


class FastGreedyClusteringAlgorithm(ClusteringAlgorithm):

    def clustering(self, topology, node_weights):
        if topology.is_directed():
            ig: Graph = Graph.from_networkx(topology.to_undirected())
        else:
            ig: Graph = Graph.from_networkx(topology)
        edge_weights = []
        for u, v in ig.get_edgelist():
            in_edge = topology.edges.get((u, v), None)
            out_edge = topology.edges.get((v, u), None)
            in_edge_weight = in_edge[graph_utils.WEIGHT_LABEL] if in_edge is not None else 0
            out_edge_weight = out_edge[graph_utils.WEIGHT_LABEL] if out_edge is not None else 0
            edge_weights.append(in_edge_weight + out_edge_weight)
        clusters = [[] for _ in range(len(node_weights))]
        res = ig.community_fastgreedy(edge_weights).as_clustering(len(node_weights))
        for i, cluster in enumerate(res.membership):
            clusters[cluster].append(i)
        return clusters


if __name__ == '__main__':
    g = graph_generator.generate(20, 40)
    g = graph_utils.add_random_weights_to_edges(g, 50, 100)
    g = graph_utils.add_random_weights_to_nodes(g, 50, 100)
    alg = FastGreedyClusteringAlgorithm()
    res = alg.clustering(g, [1, 1, 1])
    print(res)

