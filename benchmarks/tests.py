from benchmarks.benchmark_test import run_test
from benchmarks.utils import write_time_to_file
from core.core import Core
from crawler.docker_power_calculator import DockerPowerCalculator
from crawler.ssh_remote_executor import SshConfig
from fake_simulating.fake_code_generator import FakeCodeGenerator
from graphs.fast_greedy_algorithm import FastGreedyClusteringAlgorithm
from graphs.fluid_clustering_algorithm import FluidClusteringAlgorithm
from graphs.spin_glass_clustering_algorithm import SpinGlassClusteringAlgorithm
from graphs.walktrap_clustering_algorithm import WalktrapClusteringAlgorithm
from graphs.weighted_fluid_clustering_algorithm import WeightedFluidClusteringAlgorithm


def test_algorithm(algorithm, nodes, edges, compute_divider, send_divider, file_name):
    print(f'Running test for {algorithm.__class__.__name__}, nodes={nodes}, edges={edges}, '
          f'compute_divider={compute_divider}, send_divider={send_divider}')
    tries = 200
    configs = [SshConfig('172.17.0.2', user='anatoly', password=''),
               SshConfig('172.17.0.3', user='anatoly', password=''),
               SshConfig('172.17.0.4', user='anatoly', password='')]

    computing_power_calculator = DockerPowerCalculator()
    code_generator = FakeCodeGenerator(computes_divider=compute_divider, sending_divider=send_divider)
    core = Core(configs, algorithm, code_generator, computing_power_calculator)
    elapsed_time, sim_elapsed_time = run_test(core, nodes, edges, tries)
    print(f'Saving results to {file_name}')
    write_time_to_file(elapsed_time, sim_elapsed_time, file_name)


if __name__ == '__main__':
    config_set = [[20, 30, 10, 50],
                  [50, 80, 20, 100],
                  [100, 200, 40, 200],
                  [300, 900, 80, 500]]
    algorithm_names = ['weighted_fluid', 'fluid', 'fast_greedy', 'walktrap', 'spin_glass']
    algorithm_objects = [WeightedFluidClusteringAlgorithm(), FluidClusteringAlgorithm(), FastGreedyClusteringAlgorithm(),
                         WalktrapClusteringAlgorithm(), SpinGlassClusteringAlgorithm()]
    for algorithm_object, algorithm_name in zip(algorithm_objects, algorithm_names):
        for config in config_set:
            file = f'res/1_1_1/{algorithm_name}_{config[0]}_{config[1]}.csv'
            test_algorithm(algorithm_object, config[0], config[1], config[2], config[3], file)
