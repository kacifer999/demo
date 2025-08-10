# -*- coding: utf-8 -*-
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class UiCenterFrame(QFrame):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setFrameShape(QFrame.NoFrame)
        self.setFrameShadow(QFrame.Plain)
        self.setStyleSheet("border: none; border-radius: 0px;")
        self.init_layout()
        self.init_widgets()

    def init_layout(self):
        self.layout_center = QVBoxLayout(self)
        self.layout_center.setSpacing(0)
        self.layout_center.setContentsMargins(0, 0, 0, 0)

    def init_widgets(self):
        # 创建任务面板
        self.create_task_panel()

        # 创建按钮面板
        self.create_button_panel()

        # 创建垂直中心面板
        self.create_v_center_panel()

    def create_task_panel(self):
        # 创建任务面板框架
        self.frame_task_panel = QFrame()
        self.frame_task_panel.setFrameShape(QFrame.NoFrame)
        self.frame_task_panel.setFrameShadow(QFrame.Plain)
        self.frame_task_panel.setStyleSheet("border: 1px solid rgb(150, 150, 150); border-radius: 0px;")
        # 创建布局
        self.task_layout = QVBoxLayout(self.frame_task_panel)
        self.task_layout.setSpacing(0)
        self.task_layout.setContentsMargins(0, 0, 0, 0)
        # 创建任务面板部件
        self.widget_task_panel = QWidget()
        self.widget_task_panel.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        # self.widget_task_panel.setStyleSheet("background-color: rgb(127, 127, 127);")
        self.task_layout.addWidget(self.widget_task_panel)
        # 添加到中心布局
        self.layout_center.addWidget(self.frame_task_panel)

    def create_button_panel(self):
        # 创建按钮面板框架
        self.frame_button_panel = QFrame()
        self.frame_button_panel.setFrameShape(QFrame.NoFrame)
        self.frame_button_panel.setFrameShadow(QFrame.Plain)
        self.frame_button_panel.setStyleSheet("border: 1px solid rgb(150, 150, 150); border-radius: 0px;")
        # 添加到中心布局
        self.layout_center.addWidget(self.frame_button_panel)

    def create_v_center_panel(self):
        # 创建垂直中心面板框架
        self.frame_center = QFrame()
        self.frame_center.setFrameShape(QFrame.NoFrame)
        self.frame_center.setFrameShadow(QFrame.Plain)

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
        self.frame_label_tool.setStyleSheet("border: 1px solid rgb(150, 150, 150); border-radius: 0px;")

        # 添加到布局
        self.layout_label_train.addWidget(self.frame_label_tool)

    def create_config_panel(self):
        # 创建配置面板框架
        self.frame_config_panel = QFrame()
        self.frame_config_panel.setFrameShape(QFrame.NoFrame)
        self.frame_config_panel.setFrameShadow(QFrame.Plain)
        self.frame_config_panel.setStyleSheet("border: 1px solid rgb(150, 150, 150); border-radius: 0px;")

        # 添加到布局
        self.layout_label_train.addWidget(self.frame_config_panel)

    def setup_sizes(self):
        # 设置中心布局拉伸系数
        self.layout_center.setStretch(0, 2)  # 任务面板
        self.layout_center.setStretch(1, 0)  # 按钮面板
        self.layout_center.setStretch(2, 8)  # 垂直中心面板

        # 设置任务面板尺寸策略
        self.frame_task_panel.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding))

        # 设置按钮面板尺寸策略和固定高度
        self.frame_button_panel.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed))
        self.frame_button_panel.setFixedHeight(40)

        # 设置垂直中心面板尺寸策略
        self.frame_center.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding))

        # 设置水平布局拉伸系数
        self.layout_label_train.setStretch(0, 7)  # 标签工具面板
        self.layout_label_train.setStretch(1, 3)  # 配置面板

        # 设置标签工具面板尺寸策略
        self.frame_label_tool.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding))

        # 设置配置面板尺寸策略
        self.frame_config_panel.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding))