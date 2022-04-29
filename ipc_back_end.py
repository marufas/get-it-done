import ipc
import json


class IpcBackEnd:
    def __init__(self):
        self.ipc = ipc.IPCClient("Back end")
        self.ipc.register_callback(self.on_message)
        self.actions = {}

    def on_message(self, message):
        data = json.loads(message)
        try:
            command = data['cmd']
            callback = self.actions[command]
            response = callback(message)
            self.ipc.send_message(json.dumps(response))
        except Exception as err:
            print("Problem with message %s. Error: %r" % (message, err))
            self.ipc.send_message("error")

    def register_action(self, command, callback):
        self.actions[command] = callback

if __name__ == "__main__":
    client = IpcBackEnd()

    client.ipc.listen()