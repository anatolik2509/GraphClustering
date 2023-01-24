class SshConfig:
    def __init__(self, host: str, user: str = None, password: str = None, private_key_file: str = None, port: int = 22):
        self.host = host
        self.user = user
        self.password = password
        self.private_key_file = private_key_file
        self.port = port
