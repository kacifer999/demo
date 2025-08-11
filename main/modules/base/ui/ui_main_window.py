from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from .ui_view_list import UiViewListPanel
from main.modules.base.ui.ui_menubar import UiMenuBar
from main.modules.base.ui.ui_project_panel import UiProjectPanel
from main.modules.base.ui.ui_center_frame import UiCenterFrame
from main.modules.base.ui.ui_view_list import UiViewListPanel


class UiMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # 设置窗口标题和基本属性
        self.setMinimumSize(QSize(1200, 800))
        self.resize(1200, 800)
        # 设置窗口为无边框
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.init_ui()
    
    def init_ui(self):
        # 创建窗口控件和布局
        self.window_widget = QWidget()
        self.window_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.setCentralWidget(self.window_widget)
        self.window_layout = QVBoxLayout(self.window_widget)
        self.window_layout.setSpacing(0)
        self.window_layout.setContentsMargins(0, 0, 0, 0)
        # 创建标题栏
        self.create_title_bar()
        # 创建菜单栏
        self.create_menubar()
        # 创建所有widget
        self.main_layout = QHBoxLayout()
        self.main_layout.setSpacing(0)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.window_layout.addLayout(self.main_layout)
        self.create_project_panel()
        self.list_project_panel = self.ui_project_panel.list_project_panel
        self.create_center_content()
        self.ui_task_panel = self.ui_center_frame.frame_task_panel
        self.widget_task_panel = self.ui_center_frame.widget_task_panel
        self.widget_button_panel = self.ui_center_frame.widget_button_panel
        self.create_view_list_panel()
        # 创建状态栏
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        # 统一设置尺寸
        self.setup_widget_sizes()


    def create_title_bar(self):
        self.title_bar = QWidget()
        self.title_bar.setFixedHeight(25)
        self.window_layout.addWidget(self.title_bar)
        # 创建标题栏布局
        layout = QHBoxLayout(self.title_bar)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        # 创建标题标签
        self.label_title = QLabel()
        self.label_title.setText("Demo")
        self.label_title.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        layout.addWidget(self.label_title)
        # 创建最小化和关闭按钮
        self.button_minimize = QPushButton("-")
        self.button_minimize.setFixedSize(23, 23)
        self.button_minimize.clicked.connect(self.showMinimized)
        layout.addWidget(self.button_minimize)
        layout.addItem(QSpacerItem(5, 25, QSizePolicy.Fixed, QSizePolicy.Fixed))
        self.button_close = QPushButton("×")
        self.button_close.setFixedSize(23, 23)
        self.button_close.clicked.connect(self.close)
        layout.addWidget(self.button_close)

        
    def create_menubar(self):
        self.menu_bar = UiMenuBar(self)
        self.window_layout.addWidget(self.menu_bar)
        

    def create_project_panel(self):
        self.ui_project_panel = UiProjectPanel(self)
        self.main_layout.addWidget(self.ui_project_panel)
        
        
    def create_center_content(self):
        self.ui_center_frame = UiCenterFrame(self)
        self.main_layout.addWidget(self.ui_center_frame)

        
    def create_view_list_panel(self):
        self.ui_view_list = UiViewListPanel(self)
        self.main_layout.addWidget(self.ui_view_list)
    
    
    def setup_widget_sizes(self):
        self.ui_center_frame.setup_sizes()
    
