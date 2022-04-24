from unittest import TestCase
from unittest.mock import MagicMock
from collections import OrderedDict
from time import sleep
import sys
from PyQt5 import QtWidgets

from front_end import GuiController


class TestGuiController(GuiController):
    def connect_to_back_end(self):
        self.ipc = MagicMock()
        self.ipc.get_buckets.return_value = {}


class TestCases(TestCase):
    def setUp(self) -> None:
        self.app = QtWidgets.QApplication(sys.argv)
        self.test_gui = TestGuiController()

    def tearDown(self) -> None:
        pass
        self.app.exec_()

    def test_buckets_are_loaded(self):
        buckets = OrderedDict({"0": {"name": "root", "parent": ""},
                               "1": {"name": "subbucket", "parent": "0"},
                               "2": {"name": "secondBucket", "parent": ""}})
        self.test_gui.ipc.get_buckets.return_value = buckets
        self.test_gui.update_buckets()

        self.assertEqual(2, self.test_gui.ui.bucketTree.topLevelItemCount())
        top_level_item = self.test_gui.ui.bucketTree.topLevelItem(0)
        self.assertEqual(1, top_level_item.childCount())

    def test_tasks_are_loaded(self):
        tasks = OrderedDict({"10": {"name": "Test 1", "priority": "50"},
                             "11": {"name": "Task 2", "priority": "51"}})
        self.test_gui.ipc.get_tasks.return_value = tasks

        self.test_gui.update_tasks("0")

        r1c1 = self.test_gui.ui.taskTable.item(1, 1)
        self.assertEqual("51", r1c1.text())

        # , "tags": "0,2", "complete": "0", "next_action": "Fill in", "comments": "Test test\nMore test"}})

    def test_task_details_are_loaded(self):
        details = {}