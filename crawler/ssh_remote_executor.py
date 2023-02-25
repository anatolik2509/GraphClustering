import paramiko

from paramiko import SSHClient, Transport


class SshConfig:
    def __init__(self, host: str, port: int = 22, user: str = None, password: str = None, private_key_file: str = None):
        self.host = host
        self.user = user
        self.password = password
        self.private_key_file = private_key_file
        self.port = port


class SshRemoteExecutor:
    def __init__(self, ssh_config: SshConfig):
        self.ssh_config = ssh_config
        self.ssh_client = self.get_client()

    def get_client(self):
        client = SSHClient()
        client.load_system_host_keys()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(self.ssh_config.host, self.ssh_config.port, self.ssh_config.user, self.ssh_config.password,
                       key_filename=self.ssh_config.private_key_file)
        return client

    def send_file(self, local_path, remote_path):
        with self.ssh_client.open_sftp() as sftp_client:
            sftp_client.put(local_path, remote_path)

    def execute_bash(self, command):
        stdin_raw, stdout_raw, stderr_raw = self.ssh_client.exec_command(command)

        stdout = []
        for line in stdout_raw:
            stdout.append(line.strip())

        stderr = []
        for line in stderr_raw:
            stderr.append(line.strip())

        del stdin_raw, stdout_raw, stderr_raw
        if stderr:
            print(stderr)
        return stdout

    def close(self):
        self.ssh_client.close()