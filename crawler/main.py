from SshRemoteExecutor import SshConfig, SshRemoteExecutor

config = SshConfig(host='localhost', port=1234, user="admin", password="1234")
executor = SshRemoteExecutor(config)
