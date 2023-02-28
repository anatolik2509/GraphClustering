import os
from typing import Dict, List

import networkx as nx

from graphs import fluid_clustering
from graphs import graph_generator
from graphs import graph_utils
from code_generation.code_generator import CodeGenerator
from crawler.ssh_remote_executor import SshConfig


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
            print("Hit barrier" + str(rank) + " " + str(i))
            comm.barrier()"""
send_command = "comm.send({message}, {target})"
sleep_command = "time.sleep({secs})"
recv_command = "comm.recv(source = {source})"


class FakeCodeGenerator(CodeGenerator):
    def __init__(self, node_comp_powers):
        self.node_comp_powers = node_comp_powers

    def generate_script(self, topology: nx.Graph, clustering_info: Dict[int, int],
                        node_configs: List[SshConfig]) -> str:
        program = start
        nodes_count = len(self.node_comp_powers)
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
            sim_time = nodes_sim_time[node] / self.node_comp_powers[node] / 1000
            rank_body = (" " * 4 * 2) + sleep_command.format(secs=sim_time) + "\n"
            rank_body += (" " * 4 * 2) + sync_if.format(iter_sync=10) + "\n"
            for i, neighbor in enumerate(node_to_node[node]):
                if neighbor < 0.001:
                    continue
                message = "'" + "A" * int(neighbor) + "'"
                rank_body += (" " * 4 * 3) + f"message = {message}" + "\n"
                rank_body += (" " * 4 * 3) + send_command.format(message='message', target=i) + "\n"
            for i, neighbor in enumerate(node_to_node[node]):
                if neighbor < 0.001:
                    continue
                rank_body += (" " * 4 * 3) + recv_command.format(source=i) + "\n"
            rank_body = (" " * 4) + for_iter.format(iters=100, body=rank_body)
            program += if_rank.format(rank=node, body=rank_body)
        with open('out/script.py', 'w') as output_file:
            output_file.write(program)
        return f'mpirun -np {nodes_count} python3 ./out/script.py'


if __name__ == '__main__':
    nodes = [10, 10, 10, 10]
    gen = FakeCodeGenerator(nodes)
    g = graph_generator.generate()
    g = graph_utils.add_random_weights_to_nodes(g, 50, 100)
    g = graph_utils.add_random_weights_to_edges(g, 50, 100)
    clusters = fluid_clustering.fluid_communities(g, nodes)
    cluster_info = {}
    for node, neurons in enumerate(clusters):
        for neuron in neurons:
            cluster_info[neuron] = node
    gen.generate_script(g, cluster_info, None)
