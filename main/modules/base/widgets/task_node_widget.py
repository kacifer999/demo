import json
import logging
import os
import shutil
from pathlib import Path
import types

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from main.settings.path import *
from main.modules.base.ui.ui_task_node import UiTaskNodeWidget


class TaskNodeWidget(UiTaskNodeWidget):
    signal_create_task = pyqtSignal(str, str)
    signal_delete_task = pyqtSignal(str)
    signal_select_task = pyqtSignal(str)

    def __init__(self, task_panel, task):
        super().__init__()
        self.task_panel = task_panel
        self.main_window = task_panel.main_window
        self.task_name = task.task_name
        self.prev_task = task.toolchain_config.get('prev_task')
        self.next_tasks = task.toolchain_config.get('next_tasks')
        self.row = 0
        self.col = 0
        self.update_ui()
        self.button_add.clicked.connect(self.create_task)
        self.button_delete.clicked.connect(self.delete_task)

    
    def update_ui(self):
        self.label_task_name.setText(self.task_name)
        if len(self.next_tasks) == 0 and self.prev_task!='input':
            self.button_delete.show()
        else:
            self.button_delete.hide()


    def set_location(self, row, col):
        self.row = row
        self.col = col
    

    def create_task(self):
        self.signal_create_task.emit(self.main_window.project_name, self.task_name)

    
    def delete_task(self):
        self.signal_delete_task.emit(self.task_name)
    
    def mouseDoubleClickEvent(self, a0):
        self.signal_select_task.emit(self.task_name)

        
        


    


        
    

    


