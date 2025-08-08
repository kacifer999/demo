from pathlib import Path


from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

from main.settings.path import *



class MessageBox(QMessageBox):
    def __init__(self, parent, inform_type, title, text, buttons):
        super().__init__(parent)
        grid_layout = self.layout()
        msg_lab = self.findChild(QLabel, "qt_msgbox_label")
        msg_lab.setAlignment(Qt.AlignCenter)
        msg_btn_box = self.findChild(QDialogButtonBox, "qt_msgbox_buttonbox")
        grid_layout.removeWidget(msg_lab)
        grid_layout.removeWidget(msg_btn_box)
        grid_layout.addWidget(msg_lab, 0, 0, alignment=Qt.AlignCenter)
        grid_layout.addWidget(msg_btn_box, 1, 0, alignment=Qt.AlignCenter)
        self.clicked_button = QMessageBox.Ok
        self.setWindowTitle(title)
        match(inform_type):
            case 'information':
                self.setWindowIcon(QIcon(Path(ICONS_DIR, 'information.png').as_posix()))
            case 'warning':
                self.setWindowIcon(QIcon(Path(ICONS_DIR, 'warning.png').as_posix()))
            case _:
                pass

        self.setText(text)
        self.setStandardButtons(buttons)
        self.button(QMessageBox.Ok).setText("确定")
        self.button(QMessageBox.Ok).clicked.connect(self.set_ok)
        if len(self.buttons()) == 2:
            self.button(QMessageBox.Cancel).setText("取消")
            self.button(QMessageBox.Cancel).clicked.connect(self.set_cancel)
        
        self.setStyleSheet("QLabel{min-width: 360px; min-height: 60px; font: 14px;}")
        self.setDefaultButton(QMessageBox.Ok)
        

    def run(self):
        if self.exec():
            return self.clicked_button





    # def popup_information(self, inform_type, title, text, buttons, default=QMessageBox.Ok):
    #     if inform_type == 'information':
    #         self.setWindowTitle(title)
    #         self.setWindowIcon(QIcon(Path(ICONS_DIR, 'information.png').as_posix()))
    #     if inform_type == 'warning':
            
    #     self.setText(text)
    #     self.setStandardButtons(buttons)
    #     if len(self.buttons()) == 1:
    #         self.button(QMessageBox.Ok).setText("确定")
    #         self.button(QMessageBox.Ok).clicked.connect(self.set_ok)
    #     if len(self.buttons()) == 2:
    #         self.button(QMessageBox.Ok).setText("确定")
    #         self.button(QMessageBox.Ok).clicked.connect(self.set_ok)
    #         self.button(QMessageBox.Cancel).setText("取消")
    #         self.button(QMessageBox.Cancel).clicked.connect(self.set_cancel)
    #     self.setStyleSheet("QLabel{min-width: 360px; min-height: 60px; font: 14px;}")
    #     self.setDefaultButton(default)
    #     if self.exec():
    #         return self.clicked_button

    def set_ok(self):
        self.clicked_button = QMessageBox.Ok

    def set_cancel(self):
        self.clicked_button = QMessageBox.Cancel