from clustering.clustering import fluid_communities
from clustering.clustering_algorithm import ClusteringAlgorithm


class WeightedFluidClusteringAlgorithm(ClusteringAlgorithm):

    def clustering(self, topology, node_weights):
        return fluid_communities(topology, node_weights)
