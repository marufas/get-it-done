from unittest import TestCase
from unittest.mock import MagicMock
from collections import OrderedDict
from time import sleep
import sys
from PyQt5 import QtWidgets

from front_end import GuiController


class TestCases(TestCase):
    def setUp(self) -> None:
        self.app = QtWidgets.QApplication(sys.argv)
        self.test_gui = GuiController(MagicMock())

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



    def test_task_details_are_loaded(self):
        buckets = OrderedDict({"0": {"name": "root", "parent": ""},
                               "1": {"name": "subbucket", "parent": "0"},
                               "2": {"name": "secondBucket", "parent": ""}})
        details = {"name": "Detailed task", "priority": "53" , "bucket": "0", "project": "1", "complete": "0", "comments": "Test test\nMore test"}
        self.test_gui.ipc.get_task_details.return_value = details
        self.test_gui.ipc.get_buckets.return_value = buckets
        self.test_gui.update_buckets()
        self.test_gui.update_task_details("0")

        self.assertEqual("subbucket", self.test_gui.ui.detailProject.text())
