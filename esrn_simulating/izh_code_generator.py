import pathlib
import shutil
from typing import Dict, List

import networkx as nx

from code_generation.code_generator import CodeGenerator
from crawler.ssh_remote_executor import SshRemoteExecutor, SshConfig
from esrn_simulating.esrn_topology_constructor import *
from graphs.weighted_fluid_clustering_algorithm import WeightedFluidClusteringAlgorithm


class IzhCodeGenerator(CodeGenerator):

    def __init__(self, iterations=1000):
        self.iterations = iterations

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
        shutil.copy(pathlib.Path(__file__).parent.joinpath('bin/mini_gras_izh'), pathlib.Path('out/mini_gras_izh'))
        return f'mpirun -rf rank_file.txt -np {len(node_configs)} ./mini_gras_izh topology.txt {self.iterations}', \
            [pathlib.Path('out/mini_gras_izh'), pathlib.Path('out/topology.txt')]
