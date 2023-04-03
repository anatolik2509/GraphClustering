import pathlib
import shutil
from typing import Dict, List

import networkx as nx

from code_generation.code_generator import CodeGenerator
from crawler.ssh_remote_executor import SshRemoteExecutor, SshConfig
from graphs.weighted_fluid_clustering_algorithm import WeightedFluidClusteringAlgorithm

NUCLEUS_NAME_LABEL = 'nucleus_name'
NEURONS_COUNT_LABEL = 'nucleus_count_name'
NUCLEUS_TYPE_LABEL = 'nucleus_type'

SYNAPSE_DELAY_LABEL = 'delay'
SYNAPSE_OUTDEGREE_LABEL = 'outdegree'
SYNAPSE_WEIGHT_LABEL = 'syn_weight'


class EsrnCodeGenerator(CodeGenerator):

    def generate_script(self, topology: nx.Graph, clustering_info: Dict[int, int],
                        node_configs: List[SshConfig]) -> (str, List[pathlib.Path]):
        with open('out/rank_file.txt', 'w') as rank_file:
            for i, node_info in enumerate(node_configs):
                rank_file.write(f'rank {i}={node_info.host} slots=2\n')
        with open('out/topology.txt', 'w') as topology_file:
            topology_file.write(f'{len(node_configs)}\n')
            topology_file.write(f'{len(topology.nodes)}\n')
            for node in topology.nodes:
                params = topology.nodes[node]
                topology_file.write(f'{params[NUCLEUS_NAME_LABEL]} {params[NEURONS_COUNT_LABEL]} '
                                    f'{params[NUCLEUS_TYPE_LABEL]}\n')
            topology_file.write(f'{len(topology.edges)}\n')
            topology_file.write('4\n')
            for edge in topology.edges:
                params = topology.edges[edge]
                topology_file.write(f'{edge[0]} {edge[1]} {params[SYNAPSE_OUTDEGREE_LABEL]} '
                                    f'{params[SYNAPSE_DELAY_LABEL]} {params[SYNAPSE_WEIGHT_LABEL]}\n')
            hosts_list = []
            for node in range(len(topology.nodes)):
                hosts_list.append(str(clustering_info[node]))
            topology_file.write(' '.join(hosts_list) + '\n')
        shutil.copy(pathlib.Path(__file__).parent.joinpath('bin/mini_gras'), pathlib.Path('out/mini_gras'))
        return f'mpirun -rf rank_file.txt -np {len(node_configs)} ./mini_gras topology.txt', \
            [pathlib.Path('out/mini_gras'), pathlib.Path('out/topology.txt')]


if __name__ == '__main__':
    topology = nx.DiGraph()
    topology.add_node(0, nucleus_name='1', nucleus_count_name=4, nucleus_type=1, weight=4)
    topology.add_node(1, nucleus_name='2', nucleus_count_name=4, nucleus_type=1, weight=4)
    topology.add_node(2, nucleus_name='g', nucleus_count_name=1, nucleus_type=0, weight=1)
    topology.add_edge(0, 1, delay=10, outdegree=4, syn_weight=10000, weight=16)
    topology.add_edge(1, 0, delay=10, outdegree=4, syn_weight=10000, weight=16)
    topology.add_edge(2, 1, delay=10, outdegree=4, syn_weight=10000, weight=4)
    generator = EsrnCodeGenerator()
    clustering_info = {0: 0, 1: 1, 2: 0}
    generator.generate_script(topology, clustering_info, [SshConfig('host'), SshConfig('host2')])
    alg = WeightedFluidClusteringAlgorithm()
    print(alg.clustering(topology, [1, 1]))
