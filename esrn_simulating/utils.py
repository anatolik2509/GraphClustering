from typing import List, Dict

import networkx as nx
import matplotlib.pyplot as plt


def to_data_set(lines: List[str], topology: nx.Graph, clustering_info: Dict[int, int]):
    result = {}
    for node in topology.nodes:
        result[topology.nodes[node]['nucleus_name']] = []
    for line in lines:
        host, step, nucleus_id, v = line.split()
        name = topology.nodes[int(nucleus_id)]['nucleus_name']
        result[name].insert(int(step), int(v))
    return result


def draw_nuclei(voltages, name):
    plt.plot(voltages)
    plt.title(name)
    plt.ylabel('V')
    plt.xlabel('steps')
    plt.show()


if __name__ == '__main__':
    test_lines = ["0 0 0 100", "0 0 1 101", "1 0 0 102", "1 0 1 103",
                  "0 1 0 200", "0 1 1 201", "1 1 0 202", "1 1 1 203"]
    g = nx.generators.complete_graph(4)
    g.nodes[0]['nucleus_name'] = "1"
    g.nodes[1]['nucleus_name'] = "2"
    g.nodes[2]['nucleus_name'] = "3"
    g.nodes[3]['nucleus_name'] = "4"
    to_data_set(test_lines, g, {0: 0, 1: 1, 2: 0, 3: 1})
