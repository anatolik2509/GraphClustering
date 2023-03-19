import pathlib
from typing import List, Union

from crawler.computing_power_calculator import ComputingPowerCalculator
from crawler.ssh_remote_executor import SshRemoteExecutor
from crawler.ssh_remote_executor import SshConfig


class DockerPowerCalculator(ComputingPowerCalculator):
    def calculate(self, ssh_remote_executors: List[SshRemoteExecutor]) -> List[Union[int, float]]:
        result = []
        script_path = pathlib.Path(__file__).parent.joinpath('scripts/docker_power.py')
        for executor in ssh_remote_executors:
            stdout, stderr = executor.execute_script("python3 docker_power.py", script_path)
            result.append(float(stdout[0]))
        return result


if __name__ == '__main__':
    calculator = DockerPowerCalculator()
    executors = [SshRemoteExecutor(SshConfig('172.17.0.2', user='root', password='')),
                 SshRemoteExecutor(SshConfig('172.17.0.3', user='root', password=''))]
    powers = calculator.calculate(executors)
    print(powers)
