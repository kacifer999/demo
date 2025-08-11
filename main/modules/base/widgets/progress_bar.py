from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class ProgressBar(object):
    def __init__(self, main_window):
        super().__init__()
        self.progress_bar_dict = dict()
        self.main_window = main_window
        self.progress_bar = None
        self.percentage_text = None
        self.progressing = False
    

    def add_bar(self, bar_name, message):
        self.progressing = True
        # if bar_name == 'main_bar':
        #     self.disable_buttons()
        progress_bar = QProgressBar(self.main_window, minimum=0, maximum=100)
        progress_bar.setMaximumWidth(self.main_window.width())
        percentage_text = QLabel(self.main_window)
        percentage_text.setAlignment(Qt.AlignCenter)
        percentage_text.setMaximumWidth(200)
        self.main_window.status_bar.addWidget(progress_bar, 9)
        self.main_window.status_bar.addWidget(percentage_text, 1)
        self.progress_bar_dict[bar_name] = (progress_bar, percentage_text, message)
        self.update_bar(bar_name, 0)


    def update_bar(self, bar_name, value):
        if bar_name not in self.progress_bar_dict: return
        value = min(max(value, 0), 100)
        progress_bar, percentage_text, message = self.progress_bar_dict[bar_name]
        percentage_text.setText(f'{message}已完成: {value} %')
        progress_bar.setValue(value)
    

    def remove_bar(self, bar_name):
        progress_bar, percentage_text, message = self.progress_bar_dict[bar_name]
        self.main_window.status_bar.removeWidget(progress_bar)
        self.main_window.status_bar.removeWidget(percentage_text)
        progress_bar.deleteLater()
        percentage_text.deleteLater()
        del self.progress_bar_dict[bar_name]
        if len(self.progress_bar_dict) == 0:
            self.progressing = False
            # self.enable_buttons()