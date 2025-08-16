from pathlib import Path

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from main.settings.path import ICONS_DIR

class ViewListPanel(QFrame):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setFrameShape(QFrame.NoFrame)
        self.setFrameShadow(QFrame.Plain)
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
        self.setFixedWidth(100)
        self.setStyleSheet("""QFrame {background-color: rgb(127, 127, 127);
                           border: 1px solid rgb(150, 150, 150);
                           border-radius: 0px;}""")
        self.buttons_dict = dict()
        self.batch_size = 10
        self.selected_button = None
        self.init_ui()
        view_name_list = list()
        for image_dir in Path(r'C:\Codes\GitHub\demo\projects\1\icons').glob('*.png'):
            view_name = image_dir.stem
            view_name_list.append(view_name)
        self.add_images(r'C:\Codes\GitHub\demo\projects\1', view_name_list)
        
        
    def init_ui(self):
        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        
        button_up_layout = QHBoxLayout()
        self.button_up = QPushButton()
        self.button_up.setFixedSize(99, 20)
        self.button_up.setIcon(QIcon(Path(ICONS_DIR, 'up.png').as_posix()))
        self.button_up.setIconSize(QSize(20, 20))
        self.button_up.setFocusPolicy(Qt.NoFocus)
        self.button_up.setCursor(Qt.PointingHandCursor)
        self.button_up.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        button_up_layout.addWidget(self.button_up, alignment=Qt.AlignCenter)
        self.layout.addLayout(button_up_layout)

        self.image_area = QWidget()
        self.image_area.setStyleSheet('border: none; background-color: rgb(127, 127, 127);')
        self.image_area_layout = QVBoxLayout(self.image_area)
        self.image_area_layout.setAlignment(Qt.AlignCenter)
        self.image_area_layout.setSpacing(0)
        self.image_area_layout.setContentsMargins(0, 0, 0, 0)
        self.image_area.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.layout.addWidget(self.image_area)

        button_down_layout = QHBoxLayout()
        self.button_down = QPushButton()
        self.button_down.setFixedSize(99, 20)
        self.button_down.setIcon(QIcon(Path(ICONS_DIR, 'down.png').as_posix()))
        self.button_down.setIconSize(QSize(20, 20))
        self.button_down.setFocusPolicy(Qt.NoFocus)
        self.button_down.setCursor(Qt.PointingHandCursor)
        self.button_down.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        button_down_layout.addWidget(self.button_down, alignment=Qt.AlignCenter)
        self.layout.addLayout(button_down_layout)

        
    def add_images(self, project_dir, view_name_list):
        self.clear_images()
        for view_name in view_name_list:
            icon = QIcon(Path(project_dir, 'icons', f'{view_name}.png').as_posix())
            button = QPushButton()
            button.setIcon(icon)
            button.setIconSize(QSize(80, 80))
            button.setFixedSize(90, 90)
            button.setStyleSheet('border: none;')
            button.clicked.connect(lambda _, name=view_name: self.on_image_clicked(name))
            if len(self.buttons_dict) == 0:
                QTimer.singleShot(0, button.click)
            self.buttons_dict[view_name] = button
            self.image_area_layout.addWidget(button)
    

    def clear_images(self):
        for button in self.buttons_dict.values():
            self.image_area_layout.removeWidget(button)
            button.disconnect()
            button.deleteLater()
        self.buttons_dict.clear()



    def on_image_clicked(self, view_name):
        print(f"图片被点击: {view_name}")
        # 获取当前点击的按钮
        clicked_button = self.buttons_dict[view_name]
        if self.selected_button == clicked_button: return
        if self.selected_button:
            self.selected_button.setStyleSheet('border: none;')

        self.selected_button = clicked_button
        self.selected_button.setStyleSheet('border: 5px solid rgb(29, 233, 182);')

