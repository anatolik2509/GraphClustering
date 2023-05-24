import pathlib
from typing import List

import networkx as nx
import subprocess

import graphs.graph_utils
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
        self.cluster_info = None

    def _send_scripts_to_nodes(self, path: pathlib.Path):
        for executor in self.ssh_executors:
            executor.send_file(path, path.name)

    def execute(self, topology: nx.Graph):
        node_weights = self.computing_power_calculator.calculate(self.ssh_executors)
        clusters = self.clustering_algorithm.clustering(topology, node_weights)
        # print(graphs.graph_utils.clustering_loss(topology, clusters, node_weights))
        # graphs.graph_utils.draw_graph(topology, clusters)
        self.cluster_info = {}
        for node, neurons in enumerate(clusters):
            for neuron in neurons:
                self.cluster_info[neuron] = node
        start_command, file_paths = self.code_generator.generate_script(topology, self.cluster_info, self.nodes_configs)
        for file_path in file_paths:
            self._send_scripts_to_nodes(file_path)
        process = subprocess.Popen(start_command.split(' '),
                                   cwd=str(file_paths[0].parent),
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        return process
