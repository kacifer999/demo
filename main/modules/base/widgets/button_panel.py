from pathlib import Path

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from main.settings.path import ICONS_DIR
from main.modules.base.widgets.messagge_box import MessageBox
from main.modules.base.service.thread_load_images import LoadImagesThread


class ButtonPanel(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setStyleSheet("QPushButton { border: none; }")
        self.buttons_dict = {
            'load_images': ('button_load_images', 'image.png', '加载图像'),
            'left': ('button_prev_image', 'left.png', '上一张'),
            'right': ('button_next_image', 'right.png', '下一张'),
            'rescale': ('button_rescale', 'rescal.png', '缩放图像'),
            'train': ('button_train', 'train.png', '训练模型'),
            'test': ('button_test', 'test.png', '测试模型'),
            }
        self.init_ui()
    

    def init_ui(self):
        self.layout_buttons = QHBoxLayout(self)
        self.layout_buttons.setSpacing(20)
        self.layout_buttons.setContentsMargins(10, 0, 0, 0)
        self.add_button('load_images')
        self.add_button('left')
        self.add_button('right')
        self.add_button('rescale')
        self.add_line()
        self.add_button('train')
        self.add_button('test')
        self.layout_buttons.addStretch()
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("搜索图像名称...")
        self.search_box.setFixedWidth(400)
        self.search_box.setFixedHeight(30)
        self.search_box.setStyleSheet("QLineEdit {background: transparent; border: none;}")
        self.layout_buttons.addWidget(self.search_box)



    def on_load_images(self):
        selected_files, _ = QFileDialog.getOpenFileNames()
        if not selected_files: return
        image_dir_list = sorted([Path(file).as_posix() for file in selected_files
                                if Path(file).suffix.lower() in ['.jpg','.png','.bmp']])
        self.main_window.progress_bar.add_bar('main_bar', '加载图集')
        self.main_window.close_db()
        thread = LoadImagesThread(self.main_window.task, image_dir_list)
        thread.one_finished.connect(self.main_window.update_progress_bar)
        thread.thread_finished.connect(self.post_load_images)
        thread.start()
        thread.exec()
    
    def post_load_images(self):
        self.main_window.connect_db()
        # TODO
        # self.main_window.image_panel.load_view_list()
        msg = '图像加载完成！'
        MessageBox(self.main_window, 'information', '提示', msg, QMessageBox.Ok).run()
        self.main_window.progress_bar.remove_bar('main_bar')


    def on_prev_image(self):
        pass


    def on_next_image(self):
        pass


    def on_rescale(self):
        pass


    def on_train(self):
        pass
    

    def on_test(self):
        pass


    def on_export(self):
        pass


    def on_button_clicked(self, button_name):
        match button_name:
            case 'load_images':
                self.on_load_images()
            case 'left':
                self.on_prev_image()
            case 'right':
                self.on_next_image()
            case 'rescale':
                self.on_rescale()
            case 'train':
                self.on_train()
            case 'test':
                self.on_test()
    
    def add_button(self, button_name):
        name, icon_name, tooltip = self.buttons_dict[button_name]
        button = QPushButton()
        button.setFixedSize(30, 30)
        button.setIcon(QIcon(Path(ICONS_DIR, icon_name).as_posix()))
        button.setIconSize(QSize(20, 20))
        button.setFocusPolicy(Qt.NoFocus)
        button.setToolTip(tooltip)
        button.setCursor(Qt.PointingHandCursor)
        setattr(self, name, button)
        button.clicked.connect(lambda: self.on_button_clicked(button_name))
        self.layout().addWidget(button)

    
    def add_line(self):
        line = QFrame()
        line.setFrameShape(QFrame.VLine)
        line.setFrameShadow(QFrame.Sunken)
        line.setFixedSize(1, 30)
        self.layout_buttons.addWidget(line)



