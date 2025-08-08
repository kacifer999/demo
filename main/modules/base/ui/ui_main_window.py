from PySide6.QtGui import *
from PySide6.QtCore import *
from PySide6.QtWidgets import *

from .ui_menubar import UiMenuBar
from .ui_project_panel import UiProjectPanel
from .ui_center_frame import UiCenterFrame
from .ui_view_list import UiViewListPanel

class UiMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # 设置窗口标题和基本属性
        self.setMinimumSize(QSize(1200, 800))
        self.resize(1200, 800)
        
        # 创建中心部件和主布局
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QHBoxLayout(self.central_widget)
        self.main_layout.setSpacing(0)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        
        # 创建菜单栏和状态栏
        self.create_menubar()
        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)

        # 创建所有widget
        self.create_project_panel()
        self.list_project_panel = self.ui_project_panel.list_project_panel
        self.create_center_content()
        self.widget_task_panel = self.ui_center_frame.widget_task_panel
        self.create_view_list_panel()
        
        # 统一设置尺寸
        self.setup_widget_sizes()
        
        
    def create_menubar(self):
        # 创建菜单栏
        self.menubar = UiMenuBar(self)

        self.setMenuBar(self.menubar)
        
    def create_project_panel(self):
        # 创建项目面板
        self.ui_project_panel = UiProjectPanel(self)
        # 添加到主布局
        self.main_layout.addWidget(self.ui_project_panel)
        
        
    def create_center_content(self):
        # 创建中心内容区域
        self.ui_center_frame = UiCenterFrame(self)
        # 添加到主布局
        self.main_layout.addWidget(self.ui_center_frame)

        
    def create_view_list_panel(self):
        # 创建视图列表面板
        self.frame_view_list = UiViewListPanel(self)
        # 添加到主布局
        self.main_layout.addWidget(self.frame_view_list)
        
    def setup_widget_sizes(self):
        # 设置主布局拉伸系数 (10%: 80%: 10%)
        self.main_layout.setStretch(0, 1)  # 项目面板
        self.main_layout.setStretch(1, 8)  # 中心面板
        self.main_layout.setStretch(2, 1)  # 视图列表面板
        
        # 设置中心内容区域尺寸策略和拉伸系数
        self.ui_center_frame.setup_sizes()
        
        # 设置视图列表面板尺寸策略
        self.frame_view_list.setup_size()

