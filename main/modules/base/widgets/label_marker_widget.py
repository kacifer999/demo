from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class LabelMarkerWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.setFixedHeight(25)
        self.setStyleSheet("background-color: rgba(0, 255, 0, 100);")
        self.init_ui()


    def init_ui(self):
        layout = QHBoxLayout(self)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        font = QFont()
        font.setBold(True)
        font.setPointSize(20)
        self.left_label = QLabel('标注')
        self.left_label.setFont(font)
        self.left_label.setStyleSheet("border: none;")
        self.left_label.setContentsMargins(5, 0, 0, 0)
        self.left_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.left_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        layout.addWidget(self.left_label)
        self.right_label = QLabel('预测')
        self.right_label.setFont(font)
        self.right_label.setStyleSheet("border: none;")
        self.right_label.setContentsMargins(0, 0, 5, 0)
        self.right_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.right_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(self.right_label)


    def set_color(self, color):
        self.setStyleSheet(f"background-color: {color};")


    def set_left_text(self, text):
        self.left_label.setText(text)


    def set_right_text(self, text):
        self.right_label.setText(text)

