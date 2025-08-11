from pathlib import Path

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from main.modules.base.service.thread_load_images import LoadImagesThread
from main.modules.base.widgets.messagge_box import MessageBox


class ButtonPanel(object):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.panel = main_window.widget_button_panel
        self.connect_signals()
    
    def connect_signals(self):
        self.panel.button_load_images.clicked.connect(self.on_load_images)
        self.panel.button_rescale.clicked.connect(self.on_rescale)
        self.panel.button_train.clicked.connect(self.on_train)
        self.panel.button_test.clicked.connect(self.on_test)
        self.panel.button_export.clicked.connect(self.on_export)


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




    def on_rescale(self):
        pass


    def on_train(self):
        pass
    

    def on_test(self):
        pass


    def on_export(self):
        pass




