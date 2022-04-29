from collections import OrderedDict


class BackEndLogic:
    def __init__(self, ipc_client):
        self.ipc = ipc_client
        self.ipc.register_action("get_buckets", self.get_buckets)

    def get_buckets(self, details):
        buckets = OrderedDict({"0": {"name": "In basket", "parent": ""},
                               "1": {"name": "ToDo", "parent": ""},
                               "2": {"name": "Waiting for someone", "parent": ""},
                               "3": {"name": "Scheduled", "parent": ""},
                               "4": {"name": "Reference", "parent": ""},
                               "5": {"name": "Someday/Maybe", "parent": ""},
                               "6": {"name": "Generic", "parent": "1"}})
        return buckets
