import time
from typing import List

from core.core import Core
from graphs import graph_generator, graph_utils


def run_test(core: Core, graph_nodes: int, graph_edges: int, tries: int) -> (List[float], List[float]):
    elapsed_times = []
    sim_elapsed_times = []
    for _ in range(tries):
        g = graph_generator.generate(graph_nodes, graph_edges)
        g = graph_utils.add_random_weights_to_nodes(g, 50, 100)
        g = graph_utils.add_random_weights_to_edges(g, 50, 100)
        start_time = time.time()
        process = core.execute(g)
        sim_start_time = time.time()
        process.wait()
        finish_time = time.time()
        elapsed_time = finish_time - start_time
        sim_elapsed_time = finish_time - sim_start_time
        elapsed_times.append(elapsed_time)
        sim_elapsed_times.append(sim_elapsed_time)
    return elapsed_times, sim_elapsed_times
