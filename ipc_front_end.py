import ipc
import time
import queue
from collections import deque
import threading
import json


class IpcFrontEnd:
    def __init__(self):
        self.ipc = ipc.IPCClient("Front end")
        self.ipc.register_callback(self.on_message)
        self.data_queue = queue.Queue()
        self.th = threading.Thread(target=self.ipc.listen)
        self.th.start()

    def on_message(self, message):
        # print("Client received a response:", message)
        self.data_queue.put(message)

    def get_buckets(self):
        self.ipc.send_message(json.dumps({"cmd": "get_buckets"}))
        try:
            data = self.data_queue.get(block=True, timeout=3)
            data = json.loads(data)
        except queue.Empty:
            print("Did not get a response from back end!")
            raise ConnectionError("No response from back end") from None
        except json.JSONDecodeError:
            print("Got bad message:", data)
            raise ValueError("Request could not be processed") from None
        return data

    def get_tasks(self, bucket_id):
        self.ipc.send_message(json.dumps({"cmd": "get_tasks", "bucket_id": bucket_id}))
        data = self.data_queue.get(block=True, timeout=3)
        data = json.loads(data)
        return data

    def get_task_details(self, task_id):
        return {}


if __name__ == "__main__":
    client = IpcFrontEnd()
    print(client.get_buckets())

    # while True:
    #     time.sleep(3)
    #     client.send_message("current time "+ str(time.time()))