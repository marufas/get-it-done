from collections import OrderedDict


class BackEndLogic:
    def __init__(self, ipc_client, storage):
        self.ipc = ipc_client
        self.ipc.register_action("get_buckets", self.get_buckets)
        self.storage = storage

    def get_buckets(self, details):
        buckets = OrderedDict()
        for id, name, parent in self.storage.get_all_buckets():
            buckets[id] = {"name": name,
                           "parent": parent}
        return buckets
