from typing import List

from clustering.clustering_algorithm import ClusteringAlgorithm
from code_generation.code_generator import CodeGenerator
from crawler.ssh_remote_executor import SshConfig, SshRemoteExecutor


class Core:

    def __init__(self, nodes_configs: List[SshConfig], clustering_algorithm: ClusteringAlgorithm,
                 code_generator: CodeGenerator):
        self.nodes_configs = nodes_configs
        self.clustering_algorithm = clustering_algorithm
        self.code_generator = code_generator
        self.ssh_executors = [SshRemoteExecutor(config) for config in nodes_configs]

