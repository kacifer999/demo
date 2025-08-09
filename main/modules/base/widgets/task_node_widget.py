import json
import logging
import os
import shutil
from pathlib import Path
import types
from mmengine import ConfigDict

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from main.settings.path import *
from main.modules.base.widgets.messagge_box import MessageBox
from main.modules.base.ui.ui_task_node import UiTaskNodeWidget



class TaskNodeWidget(UiTaskNodeWidget):
    def __init__(self, task_panel, task):
        super().__init__()
        self.task_panel = task_panel
        self.task_name = task.task_name
        self.pre_task = task.toolchain_config.get('pre_task')
        self.next_tasks = task.toolchain_config.get('next_tasks')
        self.row = 0
        self.col = 0
        self.update_ui()

    
    def update_ui(self):
        self.label_task_name.setText(self.task_name)
        if len(self.next_tasks) == 0:
            self.button_delete.show()
        else:
            self.button_delete.hide()


    def set_location(self, row, col):
        self.row = row
        self.col = col
    

    def disconnect(self):
        self.menu.triggered.disconnect()


