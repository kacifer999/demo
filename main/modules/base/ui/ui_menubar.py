from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class UiMenuBar(QMenuBar):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.init_ui()


    def init_ui(self):
        self.menu_views = QMenu("视图")
        self.addAction(self.menu_views.menuAction())
        self.init_menu_views()
        self.menu_tools = QMenu("工具")
        self.addAction(self.menu_tools.menuAction())
        

    def init_menu_views(self):
        self.main_window.action_project_panel = QAction("工程管理")
        self.main_window.action_project_panel.setCheckable(True)
        self.main_window.action_project_panel.setChecked(True)
        self.main_window.action_project_panel.setShortcut("Ctrl+P")
        self.menu_views.addAction(self.main_window.action_project_panel)
        self.main_window.action_task_panel = QAction("任务管理")
        self.main_window.action_task_panel.setCheckable(True)
        self.main_window.action_task_panel.setChecked(True)
        self.main_window.action_task_panel.setShortcut("Ctrl+T")
        self.menu_views.addAction(self.main_window.action_task_panel)

    
    def init_menu_tools(self):
        pass
    