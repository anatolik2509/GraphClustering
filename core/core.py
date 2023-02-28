from typing import List

import networkx as nx
import subprocess

from graphs.clustering_algorithm import ClusteringAlgorithm
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
        clusters = self.clustering_algorithm.clustering(topology, node_weights)
        cluster_info = {}
        for node, neurons in enumerate(clusters):
            for neuron in neurons:
                cluster_info[neuron] = node
        start_command = self.code_generator.generate_script(topology, cluster_info, self.nodes_configs)
        process = subprocess.Popen(start_command.split(' '),
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        return process
