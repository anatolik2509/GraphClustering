from typing import List, Union

from crawler.ssh_remote_executor import SshRemoteExecutor


class ComputingPowerCalculator:
    def calculate(self, ssh_remote_executors: List[SshRemoteExecutor]) -> List[Union[int, float]]:
        raise Exception('Not implemented')
