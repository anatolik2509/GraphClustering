from typing import List

import networkx as nx
import os

from clustering.clustering_algorithm import ClusteringAlgorithm
from code_generation.code_generator import CodeGenerator
from crawler.computing_power_calculator import ComputingPowerCalculator
from crawler.ssh_remote_executor import SshConfig, SshRemoteExecutor


class Core:

    def __init__(self, nodes_configs: List[SshConfig], clustering_algorithm: ClusteringAlgorithm,
                 code_generator: CodeGenerator, computing_power_calculator: ComputingPowerCalculator):
        self.nodes_configs = nodes_configs
        self.clustering_algorithm = clustering_algorithm
        self.code_generator = code_generator
        self.ssh_executors = [SshRemoteExecutor(config) for config in nodes_configs]
        self.computing_power_calculator = computing_power_calculator

    def execute(self, topology: nx.Graph):
        node_weights = self.computing_power_calculator.calculate(self.ssh_executors)
        cluster_info = self.clustering_algorithm.clustering(topology, node_weights)
        start_command = self.code_generator.generate_script(topology, cluster_info, self.nodes_configs)
        os.system(start_command)
