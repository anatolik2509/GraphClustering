import time
from typing import List

from core.core import Core
from graphs import graph_generator, graph_utils
from graphs.graph_utils import WEIGHT_LABEL


def run_test(core: Core, topology, tries: int) -> (List[float], List[float], List[str]):
    elapsed_times = []
    sim_elapsed_times = []
    data = []
    for i in range(tries):
        g = topology
        start_time = time.time()
        process = core.execute(g)
        sim_start_time = time.time()
        stdout = process.stdout
        while True:
            line = stdout.readline()
            if not line:
                break
            data.append(line.decode('utf-8').rstrip('\n'))
        finish_time = time.time()
        elapsed_time = round(finish_time - start_time, 5)
        sim_elapsed_time = round(finish_time - sim_start_time, 5)
        elapsed_times.append(elapsed_time)
        sim_elapsed_times.append(sim_elapsed_time)
        print(f"({i + 1}/{tries}) elapsed time {elapsed_time} sec, sim elapsed time {sim_elapsed_time}")
    return elapsed_times, sim_elapsed_times, data
