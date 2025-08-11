from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap
from main.settings.path import ICONS_DIR
import os

class UiButtonPanel(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setStyleSheet("QPushButton { border: none; }")
        self.init_ui()

    def init_ui(self):
        self.layout_buttons = QHBoxLayout(self)
        self.layout_buttons.setSpacing(20)
        self.layout_buttons.setContentsMargins(10, 0, 0, 0)
        self.create_buttons()

    
    def create_buttons(self):
        # 加载图像按钮
        self.button_load_images = QPushButton()
        self.button_load_images.setIcon(QIcon(QPixmap(os.path.join(ICONS_DIR, 'image.png'))))
        self.button_load_images.setToolTip("加载图像")
        self.add_button(self.button_load_images)
        # 缩放按钮
        self.button_rescale = QPushButton()
        self.button_rescale.setIcon(QIcon(QPixmap(os.path.join(ICONS_DIR, 'rescal.png'))))
        self.button_rescale.setToolTip("缩放图像")
        self.add_button(self.button_rescale)
        # 添加分割线
        self.add_line()
        # 训练按钮
        self.button_train = QPushButton()
        self.button_train.setIcon(QIcon(QPixmap(os.path.join(ICONS_DIR, 'train.png'))))
        self.button_train.setToolTip("训练模型")
        self.add_button(self.button_train)
        # 测试按钮
        self.button_test = QPushButton()
        self.button_test.setIcon(QIcon(QPixmap(os.path.join(ICONS_DIR, 'test.png'))))
        self.button_test.setToolTip("测试模型")
        self.add_button(self.button_test)
        # 添加分割线
        self.add_line()
        # 导出按钮
        self.button_export = QPushButton()
        self.button_export.setIcon(QIcon(QPixmap(os.path.join(ICONS_DIR, 'export.png'))))
        self.button_export.setToolTip("导出模型")
        self.add_button(self.button_export)
        # 添加拉伸项，使按钮靠左侧对齐，搜索框靠右侧对齐
        self.layout_buttons.addStretch()
        # 创建搜索框
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("搜索...")
        self.search_box.setFixedWidth(400)
        self.search_box.setFixedHeight(30)
        self.search_box.setStyleSheet("QLineEdit {background: transparent; border: none;}")
        self.layout_buttons.addWidget(self.search_box)
    

    def add_button(self, button):
        button.setFixedSize(30, 30)
        button.setIconSize(QSize(26, 26))
        button.setFocusPolicy(Qt.NoFocus)
        self.layout_buttons.addWidget(button)
    

    def add_line(self):
        line = QFrame()
        line.setFrameShape(QFrame.VLine)
        line.setFrameShadow(QFrame.Sunken)
        line.setFixedSize(1, 30)
        self.layout_buttons.addWidget(line)