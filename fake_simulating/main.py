from graphs import graph_generator, graph_utils
from graphs.weighted_fluid_clustering_algorithm import WeightedFluidClusteringAlgorithm
from core.core import Core
from fake_simulating.fake_code_generator import FakeCodeGenerator
from fake_simulating.fake_computing_power_calculator import FakeComputingPowerCalculator

computing_powers = [10, 10, 10, 10]

g = graph_generator.generate(100, 400)
g = graph_utils.add_random_weights_to_nodes(g, 50, 100)
g = graph_utils.add_random_weights_to_edges(g, 50, 100)

clustering_algorithm = WeightedFluidClusteringAlgorithm()
computing_power_calculator = FakeComputingPowerCalculator(computing_powers)
code_generator = FakeCodeGenerator(computing_powers)
core = Core([], clustering_algorithm, code_generator, computing_power_calculator)
process = core.execute(g)
stdout = process.stdout
while True:
    line = stdout.readline()
    if not line:
        break
    print("test:", line.decode('utf-8'), sep='')
