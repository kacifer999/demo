from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

class UiTaskNodeWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        # 设置窗口属性
        self.setObjectName("TaskNodeWidget")
        self.setGeometry(QRect(0, 0, 150, 35))
        self.setMinimumSize(QSize(15, 15))
        self.setStyleSheet("background-color: rgb(100, 100, 100);")

        # 创建水平框架
        self.h_frame = QFrame(self)
        self.h_frame.setObjectName("h_frame")
        self.h_frame.setGeometry(QRect(-1, -1, 150, 35))
        size_policy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.h_frame.setSizePolicy(size_policy)
        self.h_frame.setStyleSheet("QFrame { border: none; }")
        self.h_frame.setFrameShape(QFrame.NoFrame)
        self.h_frame.setFrameShadow(QFrame.Plain)
        self.h_frame.setLineWidth(0)

        # 创建水平布局
        self.h_layout = QHBoxLayout(self.h_frame)
        self.h_layout.setObjectName("h_layout")
        self.h_layout.setSpacing(0)
        self.h_layout.setContentsMargins(2, 2, 2, 2)

        # 创建任务名称标签
        self.label_task_name = QLabel(self.h_frame)
        self.label_task_name.setObjectName("label_task_name")
        size_policy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        size_policy1.setHorizontalStretch(9)
        self.label_task_name.setSizePolicy(size_policy1)
        self.label_task_name.setLocale(QLocale(QLocale.Chinese, QLocale.China))
        self.label_task_name.setLineWidth(0)
        self.label_task_name.setText("图像分类")
        self.label_task_name.setTextFormat(Qt.AutoText)
        self.label_task_name.setAlignment(Qt.AlignCenter)

        self.h_layout.addWidget(self.label_task_name)

        # 创建垂直框架
        self.v_frame = QFrame(self.h_frame)
        self.v_frame.setObjectName("v_frame")
        size_policy2 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        size_policy2.setHorizontalStretch(1)
        self.v_frame.setSizePolicy(size_policy2)
        self.v_frame.setLayoutDirection(Qt.RightToLeft)
        self.v_frame.setStyleSheet("QFrame { border: none; }")
        self.v_frame.setFrameShape(QFrame.NoFrame)
        self.v_frame.setFrameShadow(QFrame.Plain)
        self.v_frame.setLineWidth(0)

        # 创建垂直布局
        self.verticalLayout = QVBoxLayout(self.v_frame)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)

        # 创建添加按钮
        self.button_add = QPushButton(self.v_frame)
        self.button_add.setObjectName("button_add")
        size_policy3 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.button_add.setSizePolicy(size_policy3)
        self.button_add.setMinimumSize(QSize(15, 15))
        self.button_add.setMaximumSize(QSize(15, 15))
        self.button_add.setLocale(QLocale(QLocale.Chinese, QLocale.China))
        self.button_add.setText("+")

        self.verticalLayout.addWidget(self.button_add)

        # 创建垂直间隔
        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.verticalLayout.addItem(self.verticalSpacer)

        # 创建删除按钮
        self.button_delete = QPushButton(self.v_frame)
        self.button_delete.setObjectName("button_delete")
        size_policy4 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.button_delete.setSizePolicy(size_policy4)
        self.button_delete.setMinimumSize(QSize(15, 15))
        self.button_delete.setMaximumSize(QSize(15, 16777215))
        self.button_delete.setLocale(QLocale(QLocale.Chinese, QLocale.China))
        self.button_delete.setText("-")
        self.button_delete.setIconSize(QSize(15, 15))

        self.verticalLayout.addWidget(self.button_delete)

        self.h_layout.addWidget(self.v_frame)

        # 连接信号槽
        QMetaObject.connectSlotsByName(self)