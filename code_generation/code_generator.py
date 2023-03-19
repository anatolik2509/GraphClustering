import pathlib
from typing import Dict, List
from pathlib import Path

import networkx as nx

from crawler.ssh_remote_executor import SshConfig


class CodeGenerator:
    def generate_script(self, topology: nx.Graph, clustering_info: Dict[int, int],
                        node_configs: List[SshConfig]) -> (str, pathlib.Path):
        raise Exception('Not implemented')
