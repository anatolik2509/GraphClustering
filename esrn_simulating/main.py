import time

import networkx as nx

from core.core import Core
from crawler.docker_power_calculator import DockerPowerCalculator
from crawler.ssh_remote_executor import SshConfig
from esrn_simulating.esrn_code_generator import EsrnCodeGenerator
from graphs.weighted_fluid_clustering_algorithm import WeightedFluidClusteringAlgorithm

if __name__ == '__main__':
    topology = nx.DiGraph()
    topology.add_node(0, nucleus_name='1', nucleus_count_name=4, nucleus_type=1, weight=4)
    topology.add_node(1, nucleus_name='2', nucleus_count_name=4, nucleus_type=1, weight=4)
    topology.add_node(2, nucleus_name='3', nucleus_count_name=4, nucleus_type=1, weight=4)
    topology.add_node(3, nucleus_name='g', nucleus_count_name=1, nucleus_type=0, weight=1)
    topology.add_edge(0, 1, delay=10, outdegree=4, syn_weight=10000, weight=16)
    topology.add_edge(1, 0, delay=10, outdegree=4, syn_weight=10000, weight=16)
    topology.add_edge(1, 2, delay=10, outdegree=4, syn_weight=10000, weight=16)
    topology.add_edge(2, 1, delay=10, outdegree=4, syn_weight=10000, weight=16)
    topology.add_edge(3, 1, delay=10, outdegree=4, syn_weight=10000, weight=4)

    configs = [SshConfig('172.17.0.2', user='anatoly', password=''),
               SshConfig('172.17.0.3', user='anatoly', password='')]

    clustering_algorithm = WeightedFluidClusteringAlgorithm()
    computing_power_calculator = DockerPowerCalculator()
    code_generator = EsrnCodeGenerator()
    core = Core(configs, clustering_algorithm, code_generator, computing_power_calculator)
    start = time.time()
    process = core.execute(topology)
    stdout = process.stdout
    while True:
        line = stdout.readline()
        if not line:
            break
        print("out: ", line.decode('utf-8').rstrip('\n'), sep='')
    finish = time.time()
    print(finish - start)

