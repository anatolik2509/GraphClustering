from ssh_remote_executor import SshConfig, SshRemoteExecutor

config = SshConfig(host='172.17.0.2', port=22, user="root", password="123456")
executor = SshRemoteExecutor(config)
executor.send_file("./hello_world.py", "./hello_world.py")
lines = executor.execute_bash("python3 hello_world.py")
for i, line in enumerate(lines):
    print(f'{i}: {line}')
executor.close()
