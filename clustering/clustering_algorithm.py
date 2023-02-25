from typing import List, Union, Dict

import networkx as nx


class ClusteringAlgorithm:

    def clustering(self, topology: nx.Graph, node_weights: List[Union[int, float]]) -> Dict[int, List[int]]:
        raise Exception('Not implemented')
