import os
import pathlib
from typing import Dict, List

import networkx as nx

from graphs import fluid_clustering
from graphs import graph_generator
from graphs import graph_utils
from code_generation.code_generator import CodeGenerator
from crawler.ssh_remote_executor import SshConfig, SshRemoteExecutor

start = """
from mpi4py import MPI
import time

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
"""
if_rank = """if rank == {rank}:
{body}"""
for_iter = """for i in range({iters}):
{body}"""
sync_if = """if i % {iter_sync} == 0:
            print("Hit barrier, rank = " + str(rank) + ", iter = " + str(i))
            comm.barrier()"""
send_command = "for _ in range({neighbor_weight}): comm.send({message}, {target})"
recv_command = "comm.recv(source = {source})"

"""a = 31
for _ in range({iters}):
    a = (a ** 2) % (10 ** 100000)"""


class FakeCodeGenerator(CodeGenerator):

    def __init__(self, computes_divider=1, sending_divider=1):
        self.computing_divider = computes_divider
        self.sending_divider = sending_divider

    def generate_script(self, topology: nx.Graph, clustering_info: Dict[int, int],
                        node_configs: List[SshConfig]) -> (str, List[pathlib.Path]):
        program = start
        nodes_count = len(node_configs)
        nodes_sim_time = [0.0 for _ in range(nodes_count)]
        for neuron, node in clustering_info.items():
            nodes_sim_time[node] += topology.nodes[neuron][graph_utils.WEIGHT_LABEL]
        node_to_node = [[0.0 for _ in range(nodes_count)] for _ in range(nodes_count)]
        for i, j in topology.edges:
            node_i = clustering_info[i]
            node_j = clustering_info[j]
            if node_i == node_j:
                continue
            node_to_node[node_i][node_j] += topology.get_edge_data(i, j)[graph_utils.WEIGHT_LABEL]
            node_to_node[node_j][node_i] += topology.get_edge_data(i, j)[graph_utils.WEIGHT_LABEL]
        for node in range(nodes_count):
            sim_time = nodes_sim_time[node] / self.computing_divider
            for i, j in topology.edges:
                node_i = clustering_info[i]
                node_j = clustering_info[j]
                if node_i == node and node_j == node:
                    sim_time += topology.get_edge_data(i, j)[graph_utils.WEIGHT_LABEL] / self.computing_divider
            rank_body = (" " * 4 * 2) + "a = 31" + "\n"
            rank_body += (" " * 4 * 2) + f"for _ in range({int(sim_time)}):" + "\n"
            rank_body += (" " * 4 * 3) + "a = (a ** 2) % (10 ** 2000)" + "\n"
            rank_body += (" " * 4 * 2) + sync_if.format(iter_sync=10) + "\n"
            for i, neighbor in enumerate(node_to_node[node]):
                if neighbor < 0.001:
                    continue
                message = "'" + "A" * 1000 + "'"
                rank_body += (" " * 4 * 3) + f"message = {message}" + "\n"
                rank_body += (" " * 4 * 3) + send_command.format(message='message', target=i, neighbor_weight=int(neighbor / self.sending_divider + 1)) + "\n"
            for i, neighbor in enumerate(node_to_node[node]):
                if neighbor < 0.001:
                    continue
                rank_body += (" " * 4 * 3) + recv_command.format(source=i) + "\n"
            rank_body = (" " * 4) + for_iter.format(iters=100, body=rank_body)
            program += if_rank.format(rank=node, body=rank_body)
        with open('out/script.py', 'w') as output_file:
            output_file.write(program)
        with open('out/rank_file.txt', 'w') as rank_file:
            for i, node_info in enumerate(node_configs):
                rank_file.write(f'rank {i}={node_info.host} slots=2\n')
        return f'mpirun -rf rank_file.txt -np {nodes_count} python3 script.py', [pathlib.Path('out/script.py')]


if __name__ == '__main__':
    nodes = [10, 10]
    gen = FakeCodeGenerator()
    g = graph_generator.generate()
    g = graph_utils.add_random_weights_to_nodes(g, 50, 100)
    g = graph_utils.add_random_weights_to_edges(g, 50, 100)
    clusters = fluid_clustering.fluid_communities(g, nodes)
    cluster_info = {}
    for node, neurons in enumerate(clusters):
        for neuron in neurons:
            cluster_info[neuron] = node
    gen.generate_script(g, cluster_info,
                        list(map(lambda config: SshRemoteExecutor(config),
                                 [SshConfig('172.17.0.2'), SshConfig('172.17.0.3')]))
                        )
