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
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(self.ssh_config.host, self.ssh_config.port, self.ssh_config.user, self.ssh_config.password,
                       key_filename=self.ssh_config.private_key_file)
        return client

    def send_file(self, local_path, remote_path):
        key = paramiko.PKey.from_private_key_file(filename=self.ssh_config.private_key_file)
        with Transport((self.ssh_config.host, self.ssh_config.port)) as transport:
            transport.connect(username=self.ssh_config.user, password=self.ssh_config.password, pkey=key)
            with paramiko.SFTPClient.from_transport(transport) as sftp:
                sftp.put(local_path, remote_path)

    def execute_bash(self, command):
        return self.ssh_client.exec_command(command)

    def close(self):
        self.ssh_client.close()