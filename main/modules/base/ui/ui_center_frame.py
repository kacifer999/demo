from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from main.modules.base.widgets.button_panel import ButtonPanel
from main.modules.base.widgets.canvas_tool_widget import CanvasToolWidget
from main.modules.base.widgets.label_marker_widget import LabelMarkerWidget
from main.modules.base.widgets.canvas import Canvas
from main.modules.base.ui.ui_config_frame import UiConfigFrame


class UiCenterFrame(QFrame):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setFrameShape(QFrame.NoFrame)
        self.setFrameShadow(QFrame.Plain)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.setStyleSheet("QFrame {border: none; border-radius: 0px;}")
        self.init_ui()

    def init_ui(self):
        self.layout_center = QVBoxLayout(self)
        self.layout_center.setSpacing(0)
        self.layout_center.setContentsMargins(0, 0, 0, 0)
        # 创建任务面板
        self.create_task_panel()

        # 创建按钮面板
        self.create_button_panel()

        # 创建垂直中心面板
        self.create_center_panel()

    def create_task_panel(self):
        self.frame_task_panel = QFrame()
        self.frame_task_panel.setFrameShape(QFrame.NoFrame)
        self.frame_task_panel.setFrameShadow(QFrame.Plain)
        self.frame_task_panel.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding))
        self.frame_task_panel.setStyleSheet("QFrame {border: 1px solid rgb(150, 150, 150); border-radius: 0px;}")
        # 创建布局
        self.layout_task_panel = QVBoxLayout(self.frame_task_panel)
        self.layout_task_panel.setSpacing(0)
        self.layout_task_panel.setContentsMargins(0, 0, 0, 0)
        # 创建任务面板
        self.widget_task_panel = QWidget()
        self.widget_task_panel.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.layout_task_panel.addWidget(self.widget_task_panel)
        # 添加到中心布局
        self.layout_center.addWidget(self.frame_task_panel)

    def create_button_panel(self):
        self.frame_button_panel= QFrame()
        self.frame_button_panel.setFrameShape(QFrame.NoFrame)
        self.frame_button_panel.setFrameShadow(QFrame.Plain)
        self.frame_button_panel.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed))
        self.frame_button_panel.setFixedHeight(40)
        self.frame_button_panel.setStyleSheet("QFrame {border: 1px solid rgb(150, 150, 150); border-radius: 0px;}")
        # 创建布局
        self.layout_button_panel = QVBoxLayout(self.frame_button_panel)
        self.layout_button_panel.setSpacing(0)
        self.layout_button_panel.setContentsMargins(0, 0, 0, 0)
        # 创建按钮面板
        self.widget_button_panel = ButtonPanel(self.main_window)
        self.layout_button_panel.addWidget(self.widget_button_panel)
        # 添加到中心布局
        self.layout_center.addWidget(self.frame_button_panel)

    def create_center_panel(self):
        # 创建垂直中心面板框架
        self.frame_center = QFrame()
        self.frame_center.setFrameShape(QFrame.NoFrame)
        self.frame_center.setFrameShadow(QFrame.Plain)
        self.frame_center.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding))

        # 创建水平布局
        self.layout_label_train = QHBoxLayout(self.frame_center)
        self.layout_label_train.setSpacing(0)
        self.layout_label_train.setContentsMargins(0, 0, 0, 0)
        # 创建标签工具面板
        self.create_label_tool_panel()
        # 创建配置面板
        self.create_config_panel()

        # 添加到中心布局
        self.layout_center.addWidget(self.frame_center)

    def create_label_tool_panel(self):
        # 创建标签工具面板框架
        self.frame_label_tool = QFrame()
        self.frame_label_tool.setFrameShape(QFrame.NoFrame)
        self.frame_label_tool.setFrameShadow(QFrame.Plain)
        self.frame_label_tool.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding))
        self.frame_label_tool.setStyleSheet("QFrame {border: 1px solid rgb(150, 150, 150); border-radius: 0px;}")
        # 创建水平布局
        self.layout_h_label = QHBoxLayout(self.frame_label_tool)
        self.layout_h_label.setSpacing(0)
        self.layout_h_label.setContentsMargins(0, 0, 0, 0)
        # 创建Canvas工具栏
        self.canvas_tool = CanvasToolWidget()
        self.layout_h_label.addWidget(self.canvas_tool)
        # 创建垂直布局
        self.layout_v_label = QVBoxLayout()
        self.layout_v_label.setSpacing(0)
        self.layout_v_label.setContentsMargins(0, 0, 0, 0)
        self.layout_h_label.addLayout(self.layout_v_label)
        # 标注标记控件
        self.label_marker = LabelMarkerWidget()
        self.layout_v_label.addWidget(self.label_marker)
        # 创建Canvas
        self.canvas = Canvas(self)
        self.layout_v_label.addWidget(self.canvas)
        # 创建信息显示区域
        self.view_info = QLabel()
        self.view_info.setFixedHeight(35)
        self.view_info.setStyleSheet("background-color: black; color: white; border: none;")
        self.view_info.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        self.view_info.setText("视图信息")
        self.layout_v_label.addWidget(self.view_info)
        self.layout_label_train.addWidget(self.frame_label_tool)

    def create_config_panel(self):
        self.frame_config_panel = UiConfigFrame(self)
        self.layout_label_train.addWidget(self.frame_config_panel)

    def setup_sizes(self):
        # 设置中心布局拉伸系数
        self.layout_center.setStretch(0, 20)  # 任务面板
        self.layout_center.setStretch(1, 0)  # 按钮面板
        self.layout_center.setStretch(2, 80)  # 垂直中心面板
