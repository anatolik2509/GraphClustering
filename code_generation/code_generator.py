from typing import Dict, List
from pathlib import Path

import networkx as nx


class CodeGenerator:
    def generate_scripts(self, topology: nx.Graph, clustering_info: Dict[int, List[int]]) -> Dict[int, (str, Path)]:
        raise Exception('Not implemented')
