import paramiko

from crawler.SshConfig import SshConfig
from paramiko import SSHClient, Transport


class SshRemoteExecutor:
    def __init__(self, ssh_config: SshConfig):
        self.ssh_config = ssh_config

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

    def execute_bash(self):
        pass

