# -*- coding: utf-8 -*-
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class UiViewListPanel(QFrame):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setFrameShape(QFrame.NoFrame)
        self.setFrameShadow(QFrame.Plain)
        self.setStyleSheet("background-color: rgb(127, 127, 127); border: 1px solid rgb(150, 150, 150); border-radius: 0px;")
        self.init_ui()

    def init_ui(self):
        self.view_list_layout = QVBoxLayout(self)
        self.view_list_layout.setSpacing(0)
        self.view_list_layout.setContentsMargins(0, 0, 0, 0)