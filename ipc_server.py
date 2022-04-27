import ipc

HOST = "127.0.0.1"
PORT = 62227


class IPCServer:
    def __init__(self):
        self.ipc = ipc.IPCServer()

    def run_server(self):
        self.ipc.run_server()


if __name__ == "__main__":
    server = IPCServer()
    server.run_server()
