import time

from ssh_remote_executor import SshConfig, SshRemoteExecutor

config = SshConfig(host='172.17.0.3', port=22, user="anatoly", password="")
executor = SshRemoteExecutor(config)
executor.send_file("./hello_world.py", "./hello_world.py")
start = time.time()
lines = executor.execute_bash("python3 hello_world.py")
for i, line in enumerate(lines):
    print(f'{i}: {line}')
executor.close()
finish = time.time()
print(finish - start)
