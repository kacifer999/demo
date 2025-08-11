from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class UiMenuBar(QMenuBar):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setMinimumHeight(25)
        self.menu_font = QFont()
        self.menu_font.setPointSize(12)
        self.menu_font.setBold(True)
        self.action_font = QFont()
        self.action_font.setPointSize(10)
        self.action_font.setBold(False)
        self.init_ui()


    def init_ui(self):
        # 设置字体
        self.setFont(self.menu_font)
        # 创建菜单
        self.menu_views = QMenu("视图")
        self.init_menu_views()
        self.menu_tools = QMenu("工具")
        # 添加菜单到菜单栏
        self.addAction(self.menu_views.menuAction())
        self.addAction(self.menu_tools.menuAction())
        

    def init_menu_views(self):
        # 创建动作
        self.main_window.action_project_panel = QAction("工程管理")
        self.main_window.action_project_panel.setCheckable(True)
        self.main_window.action_project_panel.setChecked(True)
        self.main_window.action_project_panel.setFont(self.action_font)
        self.main_window.action_project_panel.setShortcut("Ctrl+P")
        self.menu_views.addAction(self.main_window.action_project_panel)
        self.main_window.action_task_panel = QAction("任务管理")
        self.main_window.action_task_panel.setCheckable(True)
        self.main_window.action_task_panel.setChecked(True)
        self.main_window.action_task_panel.setFont(self.action_font)
        self.main_window.action_task_panel.setShortcut("Ctrl+T")
        self.menu_views.addAction(self.main_window.action_task_panel)

    
    def init_menu_tools(self):
        pass
    