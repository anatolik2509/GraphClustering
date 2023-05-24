import random

import networkx as nx

from benchmarks.benchmark_test import run_test
from core.core import Core
from crawler.docker_power_calculator import DockerPowerCalculator
from crawler.ssh_remote_executor import SshConfig
from esrn_simulating.izh_code_generator import IzhCodeGenerator
from graphs import graph_generator, graph_utils
from esrn_simulating import esrn_topology_constructor
from graphs.weighted_fluid_clustering_algorithm import WeightedFluidClusteringAlgorithm
from statistics import mean


def graph_to_topology(g: nx.Graph):
    gen_poses = random.choices(g.nodes, k=2)
    for node in g.nodes():
        neuron_type = 0 if node in gen_poses else 1
        esrn_topology_constructor.add_nucleus(str(node), g.nodes[node][graph_utils.WEIGHT_LABEL], neuron_type)
    for edge in g.edges():
        if random.randint(0, 1) == 0:
            esrn_topology_constructor.add_synapse(str(edge[0]), str(edge[1]), 20,
                                                  g.edges[edge][graph_utils.WEIGHT_LABEL], 1000)
        else:
            esrn_topology_constructor.add_synapse(str(edge[1]), str(edge[0]), 20,
                                                  g.edges[edge][graph_utils.WEIGHT_LABEL], 1000)
    topology = esrn_topology_constructor.build()
    esrn_topology_constructor.clean()
    return topology


def write_3d_data_to_file(data, x_len, y_len, file_name):
    with open(file_name, 'w+') as file:
        file.write(f'{x_len} {y_len}' + '\n')
        for line in data:
            file.write(f'{line[0]},{line[1]},{line[2]}' + '\n')


def test(hosts, nodes, edges):
    configs = [SshConfig('172.17.0.2', user='anatoly', password=''),
               SshConfig('172.17.0.3', user='anatoly', password=''),
               SshConfig('172.17.0.4', user='anatoly', password=''),
               SshConfig('172.17.0.5', user='anatoly', password=''),
               SshConfig('172.17.0.6', user='anatoly', password=''),
               SshConfig('172.17.0.7', user='anatoly', password=''),
               SshConfig('172.17.0.8', user='anatoly', password=''),
               SshConfig('172.17.0.9', user='anatoly', password='')]
    configs = configs[:hosts]
    g = graph_generator.generate(nodes, edges)
    g = graph_utils.add_random_weights_to_nodes(g, 100, 200)
    g = graph_utils.add_random_weights_to_edges(g, 50, 100)
    topology = graph_to_topology(g)
    computing_power_calculator = DockerPowerCalculator()
    code_generator = IzhCodeGenerator()
    algorithm = WeightedFluidClusteringAlgorithm()
    core = Core(configs, algorithm, code_generator, computing_power_calculator)
    elapsed_time, sim_elapsed_time, data = run_test(core, topology, tries)
    return mean(sim_elapsed_time)


if __name__ == '__main__':
    tries = 50
    host_num = range(1, 9)
    node_num = range(10, 110, 10)
    edge_num = [int(n * 1.2) for n in node_num]
    file = "res/3d/data.csv"
    data = []
    for hosts in host_num:
        for nodes, edges in zip(node_num, edge_num):
            print(f"Running for {hosts} hosts, {nodes} nodes, {edges} edges")
            et = test(hosts, nodes, edges)
            data.append((hosts, nodes, et))
    write_3d_data_to_file(data, len(host_num), len(node_num), file)
