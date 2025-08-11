from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class UiProjectPanel(QFrame):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setFrameShape(QFrame.NoFrame)
        self.setFrameShadow(QFrame.Plain)
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
        self.setFixedWidth(200)
        self.setStyleSheet("background-color: rgb(127, 127, 127); border: 1px solid rgb(150, 150, 150); border-radius: 0px;")
        self.project_layout = QVBoxLayout(self)
        self.project_layout.setSpacing(0)
        self.project_layout.setContentsMargins(0, 0, 0, 0)
        self.list_project_panel = QListWidget()
        font = QFont()
        font.setPointSize(12)
        self.list_project_panel.setFont(font)
        self.list_project_panel.setContextMenuPolicy(Qt.CustomContextMenu)
        self.list_project_panel.setStyleSheet("background-color: rgb(127, 127, 127)")
        self.list_project_panel.setFrameShape(QFrame.NoFrame)
        self.list_project_panel.setFrameShadow(QFrame.Plain)
        self.list_project_panel.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.list_project_panel.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.list_project_panel.setSpacing(1)

        # 添加到布局
        self.project_layout.addWidget(self.list_project_panel)