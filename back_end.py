from collections import OrderedDict


class BackEndLogic:
    def __init__(self, ipc_client, storage):
        self.ipc = ipc_client
        self.ipc.register_action("get_buckets", self.get_buckets)
        self.ipc.register_action("get_tasks", self.get_tasks)
        self.storage = storage

    def get_buckets(self, details):
        buckets = OrderedDict()
        for bucket in self.storage.get_all_buckets():
            buckets[bucket['bucket_id']] = bucket
        return buckets

    def get_tasks(self, details):
        tasks = OrderedDict()
        bucket_id = details.get("bucket_id", None)
        for task in self.storage.get_tasks(bucket_id):
            tasks[task['task_id']] = task
        return tasks
