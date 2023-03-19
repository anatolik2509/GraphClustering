import pathlib
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

    def _send_scripts_to_nodes(self, path: pathlib.Path):
        for executor in self.ssh_executors:
            executor.send_file(path, path.name)

    def execute(self, topology: nx.Graph):
        node_weights = self.computing_power_calculator.calculate(self.ssh_executors)
        print(f"Node weights = {node_weights}")
        clusters = self.clustering_algorithm.clustering(topology, node_weights)
        cluster_info = {}
        for node, neurons in enumerate(clusters):
            for neuron in neurons:
                cluster_info[neuron] = node
        start_command, file_path = self.code_generator.generate_script(topology, cluster_info, self.nodes_configs)
        print(file_path)
        print(start_command)
        self._send_scripts_to_nodes(file_path)
        process = subprocess.Popen(start_command.split(' '),
                                   cwd=str(file_path.parent),
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        return process
