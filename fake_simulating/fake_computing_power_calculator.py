from typing import List, Union

from crawler.computing_power_calculator import ComputingPowerCalculator
from crawler.ssh_remote_executor import SshRemoteExecutor


class FakeComputingPowerCalculator(ComputingPowerCalculator):
    def __init__(self, weights_list: List[float]):
        self.weights_list = weights_list

    def calculate(self, ssh_remote_executors: List[SshRemoteExecutor]) -> List[Union[int, float]]:
        return self.weights_list
