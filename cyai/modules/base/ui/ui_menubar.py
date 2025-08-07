from PySide6.QtGui import *
from PySide6.QtCore import *
from PySide6.QtWidgets import *

class UiMenuBar(QMenuBar):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setMinimumHeight(25)
        self.init_menu()

    def init_menu(self):
        # 设置字体
        self.menu_font = QFont()
        self.menu_font.setPointSize(12)
        self.menu_font.setBold(True)
        self.action_font = QFont()
        self.action_font.setPointSize(10)
        self.action_font.setBold(False)
        self.setFont(self.menu_font)

        # 创建菜单
        self.menu_project = QMenu("工程")
        self.init_menu_project()
        self.menu_tools = QMenu("工具")
        self.menu_views = QMenu("视图")

        # 添加菜单到菜单栏
        self.addAction(self.menu_project.menuAction())
        self.addAction(self.menu_tools.menuAction())
        self.addAction(self.menu_views.menuAction())

    def init_menu_project(self):
        # 创建动作
        self.main_window.action_project_panel = QAction("工程管理")
        self.main_window.action_project_panel.setCheckable(True)
        self.main_window.action_project_panel.setChecked(True)
        self.main_window.action_project_panel.setFont(self.action_font)
        self.main_window.action_project_panel.setShortcut("P")
        self.menu_project.addAction(self.main_window.action_project_panel)
    
    def init_menu_tools(self):
        pass
    
    def init_menu_views(self):
        pass