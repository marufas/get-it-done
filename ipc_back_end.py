import ipc
import json


class IpcBackEnd:
    def __init__(self):
        self.ipc = ipc.IPCClient("Back end")
        self.ipc.register_callback(self.on_message)

    def on_message(self, message):
        data = json.loads(message)
        self.ipc.send_message("Responding to command: %s" % data['cmd'])


if __name__ == "__main__":
    client = IpcBackEnd()
    client.ipc.listen()