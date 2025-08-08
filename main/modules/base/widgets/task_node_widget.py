import json
import logging
import os
import shutil
from pathlib import Path
import types
from mmengine import ConfigDict

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

from main.settings.path import *
from main.modules.base.widgets.messagge_box import MessageBox
from main.modules.base.ui.ui_task_node import UiTaskNodeWidget



class TaskNodeWidget(UiTaskNodeWidget):

    # task_selected = pyqtSignal(str)
    # set_to_task = pyqtSignal(str)

    def __init__(self, task_panel):

        super(TaskNodeWidget, self).__init__()
        self.task_panel = task_panel
        self.task = None

        self.next_task_nodes = []

        self.row = 0
        self.col = 0




    def set_location(self, row, col):
        self.row = row
        self.col = col

    

    def disconnect(self):
        self.menu.triggered.disconnect()


