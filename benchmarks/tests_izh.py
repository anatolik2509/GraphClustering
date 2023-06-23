from benchmarks.benchmark_test import run_test
from benchmarks.utils import write_time_to_file, write_logs_to_file
from core.core import Core
from crawler.docker_power_calculator import DockerPowerCalculator
from crawler.ssh_remote_executor import SshConfig
from esrn_simulating.izh_code_generator import IzhCodeGenerator
from esrn_simulating.main import create_reflect_arc
from graphs.fast_greedy_algorithm import FastGreedyClusteringAlgorithm
from graphs.fluid_clustering_algorithm import FluidClusteringAlgorithm
from graphs.spin_glass_clustering_algorithm import SpinGlassClusteringAlgorithm
from graphs.walktrap_clustering_algorithm import WalktrapClusteringAlgorithm
from graphs.weighted_fluid_clustering_algorithm import WeightedFluidClusteringAlgorithm


def run_algorithm(algorithm, topology, file_name, logs_file):
    print(f'Running test for {algorithm.__class__.__name__}')
    tries = 5
    configs = [SshConfig('172.17.0.2', user='anatoly', password=''),
               SshConfig('172.17.0.3', user='anatoly', password=''),
               SshConfig('172.17.0.4', user='anatoly', password='')]

    computing_power_calculator = DockerPowerCalculator()
    code_generator = IzhCodeGenerator()
    core = Core(configs, algorithm, code_generator, computing_power_calculator)
    elapsed_time, sim_elapsed_time, data = run_test(core, topology, tries)
    print(f'Saving results to {file_name}')
    write_time_to_file(elapsed_time, sim_elapsed_time, file_name)
    write_logs_to_file(data, logs_file)


if __name__ == '__main__':
    algorithm_names = ['weighted_fluid', 'fluid', 'spinglass', 'fast_greedy', 'walktrap']
    algorithm_objects = [WeightedFluidClusteringAlgorithm(), FluidClusteringAlgorithm(), SpinGlassClusteringAlgorithm(),
                         FastGreedyClusteringAlgorithm(), WalktrapClusteringAlgorithm()]
    for algorithm_object, algorithm_name in zip(algorithm_objects, algorithm_names):
        file = f'res/1_1_1/{algorithm_name}_izh_reflect_arc.csv'
        log_file = f'res/1_1_1/{algorithm_name}_izh_reflect_arc.txt'
        run_algorithm(algorithm_object, create_reflect_arc(), file, log_file)
