import time

from crawler.docker_power_calculator import DockerPowerCalculator
from crawler.ssh_remote_executor import SshRemoteExecutor, SshConfig
from graphs import graph_generator, graph_utils
from graphs.fluid_clustering_algorithm import FluidClusteringAlgorithm
from graphs.spin_glass_clustering_algorithm import SpinGlassClusteringAlgorithm
from graphs.weighted_fluid_clustering_algorithm import WeightedFluidClusteringAlgorithm
from core.core import Core
from fake_simulating.fake_code_generator import FakeCodeGenerator
from fake_simulating.fake_computing_power_calculator import FakeComputingPowerCalculator


g = graph_generator.generate(100, 400)
g = graph_utils.add_random_weights_to_nodes(g, 50, 100)
g = graph_utils.add_random_weights_to_edges(g, 50, 100)

configs = [SshConfig('172.17.0.2', user='anatoly', password=''),
           SshConfig('172.17.0.3', user='anatoly', password=''),
           SshConfig('172.17.0.4', user='anatoly', password='')]

clustering_algorithm = WeightedFluidClusteringAlgorithm()
computing_power_calculator = DockerPowerCalculator()
code_generator = FakeCodeGenerator(10, 1000)
core = Core(configs, clustering_algorithm, code_generator, computing_power_calculator)
start = time.time()
process = core.execute(g)
stdout = process.stdout
while True:
    line = stdout.readline()
    if not line:
        break
    print("out: ", line.decode('utf-8').rstrip('\n'), sep='')
finish = time.time()
print(finish - start)
