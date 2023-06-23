import os
import pathlib
import shutil
from typing import Dict, List

import networkx as nx

from code_generation.code_generator import CodeGenerator
from crawler.ssh_remote_executor import SshRemoteExecutor, SshConfig
from esrn_simulating.esrn_topology_constructor import *
from graphs.weighted_fluid_clustering_algorithm import WeightedFluidClusteringAlgorithm


class EsrnCodeGenerator(CodeGenerator):

    def __init__(self, iterations=1000):
        self.iterations = iterations

    def generate_script(self, topology: nx.Graph, clustering_info: Dict[int, int],
                        node_configs: List[SshConfig]) -> (str, List[pathlib.Path]):
        os.makedirs(os.path.dirname('out/'), exist_ok=True)
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
        shutil.copy(pathlib.Path(__file__).parent.joinpath('bin/mini_gras_esrn'), pathlib.Path('out/mini_gras_esrn'))
        return f'mpirun -rf rank_file.txt -np {len(node_configs)} ./mini_gras_esrn topology.txt {self.iterations}', \
            [pathlib.Path('out/mini_gras_esrn'), pathlib.Path('out/topology.txt')]


def run_reflect_arc():
    add_nucleus('1', 10)
    add_nucleus('2', 10)
    add_nucleus('g', 1, 0)
    add_synapse('1', '2', 15, 5, 10000)
    add_synapse('2', '1', 15, 5, 10000)
    add_synapse('g', '2', 15, 5, 10000)
    topology = build()
    generator = EsrnCodeGenerator()
    clustering_info = {0: 0, 1: 1, 2: 0}
    generator.generate_script(topology, clustering_info, [SshConfig('host'), SshConfig('host2')])
    alg = WeightedFluidClusteringAlgorithm()
    print(alg.clustering(topology, [1, 1]))
