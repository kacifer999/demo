import sys

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from qt_material import apply_stylesheet


from main.modules.base.widgets.main_window import MainWindow

def start():
    app = QApplication(sys.argv)
    window = MainWindow()
    apply_stylesheet(app, theme='dark_teal.xml')
    window.show()
    window.raise_()
    sys.exit(app.exec())