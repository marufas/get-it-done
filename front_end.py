from PyQt5 import QtCore, QtGui, QtWidgets
import sys

from gui import Ui_MainWindow


class GuiController():
    def __init__(self, client_ipc):
        self.main_window = QtWidgets.QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.main_window)
        self.main_window.show()
        self.ipc = client_ipc
        self.object_library = {}
        self.initialise_ui()

    def show_ui(self):
        app = QtWidgets.QApplication(sys.argv)
        sys.exit(app.exec_())

    def initialise_ui(self):
        self.connect_ui_elements()
        self.update_buckets()
        self.update_projects()

    def connect_ui_elements(self):
        # self.ui.run.clicked.connect(lambda: self.button_run())
        # self.ui.reset.clicked.connect(self.button_reset)
        # self.ui.read.clicked.connect(self.button_read)
        # self.ui.execute.clicked.connect(lambda: self.button_execute())
        self.ui.bucketTree.itemClicked.connect(self._item_selected)

    def update_buckets(self):
        buckets = self.ipc.get_buckets()
        for bucket_id in buckets:
            bucket = buckets[bucket_id]
            object = self._add_tree_item(self.ui.bucketTree, bucket_id, bucket["name"], parent=bucket["parent"])
            self.object_library[bucket_id] = object
        # in_basket = self._add_tree_item("In basket", 0)
        # to_do = self._add_tree_item("ToDo", 1)
        # waiting = self._add_tree_item("Waiting for someone", 2)
        # scheduled = self._add_tree_item("Scheduled", 3)
        # reference = self._add_tree_item("Reference", 4)
        # someday = self._add_tree_item("Someday/Maybe", 5)
        # todo_generic = self._add_tree_item("Generic", 6, parent=to_do)


    def update_projects(self):
        pass

    def update_tasks(self, bucket_id=None):
        # TODO: delete all tasks
        if bucket_id is None:
            return
        tasks = self.ipc.get_tasks(bucket_id)
        for task_id in tasks:
            task = tasks[task_id]
            self._add_table_item(self.ui.taskTable, task_id, task["name"], task["priority"])

        # TODO: add items according to tag

    def update_task_details(self, task_id=None):
        if task_id is None:
            return
        details = self.ipc.get_task_details(task_id)
        self.ui.detailName.setText(details["name"])
        self.ui.detailBucket.setText(self.object_library[details["bucket"]].text(0))
        self.ui.detailProject.setText(self.object_library[details["project"]].text(0))
        self.ui.detailPriority.setText(details["priority"])
        self.ui.detailComments.setText(details["comments"])


    def _add_tree_item(self, tree, id, name, description="", parent=""):
        if not parent:
            parent = tree
        else:
            parent = self.object_library[parent]
        item = QtWidgets.QTreeWidgetItem(parent)
        item.setText(0, name)
        item.setText(1, description)
        item.setText(2, str(id))
        return item

    def _add_table_item(self, table, id, name, priority):
        row = table.rowCount() + 1
        table.setRowCount(row)
        table.setItem(row - 1, 0, QtWidgets.QTableWidgetItem(name))
        table.setItem(row - 1, 1, QtWidgets.QTableWidgetItem(priority))

    def _item_selected(self, item):
        print(item.text(2))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    win = GuiController()
    sys.exit(app.exec_())