from PyQt5 import QtCore, QtGui, QtWidgets
import sys

from gui import Ui_MainWindow


class GuiController:
    def __init__(self):
        app = QtWidgets.QApplication(sys.argv)
        self.main_window = QtWidgets.QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.main_window)
        self.main_window.show()
        self.connect_buttons()
        self.update_buckets()
        app.exec_()
        # sys.exit(app.exec_())

    def connect_buttons(self):
        pass
        # self.ui.run.clicked.connect(lambda: self.button_run())
        # self.ui.reset.clicked.connect(self.button_reset)
        # self.ui.read.clicked.connect(self.button_read)
        # self.ui.execute.clicked.connect(lambda: self.button_execute())

    def update_buckets(self):
        in_basket = self._add_tree_item("In basket", 0)
        to_do = self._add_tree_item("ToDo", 1)
        waiting = self._add_tree_item("Waiting for someone", 2)
        scheduled = self._add_tree_item("Scheduled", 3)
        reference = self._add_tree_item("Reference", 4)
        someday = self._add_tree_item("Someday/Maybe", 5)
        todo_generic = self._add_tree_item("Generic", 6, parent=to_do)

        self.ui.bucketTree.itemClicked.connect(self._item_selected)

    def update_projects(self):
        pass

    def update_tasks(self, tag=None):
        # TODO: delete all tasks
        if tag is None:
            return
        # TODO: add items according to tag

    def _add_tree_item(self, name, id, description="", parent=None):
        if parent is None:
            parent = self.ui.bucketTree
        item = QtWidgets.QTreeWidgetItem(parent)
        item.setText(0, name)
        item.setText(1, description)
        item.setText(2, str(id))
        return item

    def _item_selected(self, item):
        print(item.text(2))


if __name__ == "__main__":
    GuiController()