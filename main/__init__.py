import sys

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


from main.modules.base.widgets.main_window import MainWindow
from qt_material import apply_stylesheet

def start():
    app = QApplication(sys.argv)
    window = MainWindow()
    apply_stylesheet(app, theme='dark_teal.xml')
    window.show()
    window.raise_()
    sys.exit(app.exec())