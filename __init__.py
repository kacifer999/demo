import os
import sys
# import psutil
import signal
import subprocess
import warnings
from pathlib import Path

# third packages
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

# from cyai.modules.base.widgets.tool_chain_widget import ToolChainWidget

sys.path.append(str(Path(__file__)))

# self packages

# from cyai.modules.base.widgets.main_window import AiMainWindow
# from cyai.modules.base.service.logger import get_root_logger
# from cyai.modules.base.service.migration import Migration
# from cyai.settings.paths import BASE_DIR
# from cyai.modules.base.service.stylesheet import apply_stylesheet

def start():
    app = QApplication(sys.argv)
    window = QWidget()
    window.show()
    sys.exit(app.exec())



if __name__ == "__main__":
    """Load the Core module and trigger the execution."""
    
    # app.exec()

    # if not os.path.exists(f'{BASE_DIR}/projects/'):
    #     os.mkdir(f'{BASE_DIR}/projects/')
    # main = AiMainWindow()
    # main_icon = QIcon(Path(THEME_DIR, 'icons', 'cylogo.png').as_posix())
    # main.setWindowIcon(main_icon)
    # apply_stylesheet(app, theme='dark_teal.xml')
    # screen = QApplication.primaryScreen()
    # if screen:
    #     screen_rect = screen.geometry()
    #     max_width = screen_rect.width()
    #     max_height = screen_rect.height()
        # main.setMaximumSize(max_width, max_height - 65)
    # main.setWindowState(Qt.WindowMaximized)
    # main.show()
    # if main.label_tab is not None:
    #     main.label_tab.set_fit_window()
    # sys.exit(app.exec_())
