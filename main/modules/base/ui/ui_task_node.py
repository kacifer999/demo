from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class UiTaskNodeWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        # 设置窗口属性
        self.setObjectName("TaskNodeWidget")
        self.setGeometry(QRect(0, 0, 150, 40))
        # 创建主水平布局
        self.main_layout = QHBoxLayout(self)
        self.main_layout.setSpacing(0)
        self.main_layout.setContentsMargins(2, 0, 2, 0)
        # 创建任务名称标签
        self.label_task_name = QLabel()
        self.label_task_name.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding))
        self.label_task_name.setText("任务名称")
        # self.label_task_name.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.label_task_name.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.main_layout.addWidget(self.label_task_name)
        # 创建按钮布局
        self.layout_buttons = QVBoxLayout()
        self.layout_buttons.setSpacing(0)
        self.layout_buttons.setContentsMargins(0, 0, 0, 0)
        self.main_layout.addLayout(self.layout_buttons)
        # 新建按钮
        self.button_add = QPushButton()
        self.button_add.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))
        self.button_add.setFixedSize(QSize(18, 18))
        self.button_add.setText("+")
        self.layout_buttons.addWidget(self.button_add)
        # 删除按钮
        self.button_delete = QPushButton()
        self.button_delete.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))
        self.button_delete.setFixedSize(QSize(18, 18))
        self.button_delete.setText("-")
        self.layout_buttons.addWidget(self.button_delete)

        
