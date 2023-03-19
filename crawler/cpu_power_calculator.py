from typing import List, Union

from statistics import mean

from crawler.computing_power_calculator import ComputingPowerCalculator
from crawler.ssh_remote_executor import SshRemoteExecutor


class CpuPowerCalculator(ComputingPowerCalculator):
    def calculate(self, ssh_remote_executors: List[SshRemoteExecutor]) -> List[Union[int, float]]:
        results = []
        for executor in ssh_remote_executors:
            stdout, stderr = executor.execute_bash('lscpu -p=CPU,MAXMHZ')
            max_rate = mean(
                map(lambda line: int(str(line).split(',')[1]),
                    filter(lambda s: not s.startswith('#'), stdout))
            )
            results.append(max_rate)
        return results
