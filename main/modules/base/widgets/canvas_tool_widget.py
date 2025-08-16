
from pathlib import Path

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from main.settings.path import ICONS_DIR

class CanvasToolWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedWidth(40)
        self.buttons_dict = {
            'pen':('button_pen', 'pen.png', '画笔'),
            'eraser':('button_eraser', 'eraser.png', '橡皮'),
            'rectangle':('button_rectangle', 'rectangle.png', '矩形'),
            'square':('button_circle', 'circle.png', '圆形'),
            'bbox':('button_bbox', 'bbox.png', '检测框'),
            'delete_bbox':('button_delete_bbox', 'delete_bbox.png', '删除标注'),
            'delete':('button_delete', 'delete.png', '清空标注')}
        self.active_button = None
        self.init_ui()
        self.hide()

    def init_ui(self):
        # 创建垂直布局
        layout = QVBoxLayout(self)
        layout.setSpacing(6)
        layout.setContentsMargins(5, 10, 5, 0)
        slider_layout = QHBoxLayout()
        slider_layout.setAlignment(Qt.AlignHCenter)
        slider_layout.setContentsMargins(0, 0, 0, 0)
        layout.addLayout(slider_layout)
        self.bar_pen_size = QSlider(Qt.Vertical)
        self.bar_pen_size.setRange(1, 20)
        self.bar_pen_size.setInvertedAppearance(True)
        self.bar_pen_size.setValue(5)
        self.bar_pen_size.setFixedHeight(200)
        self.bar_pen_size.setStyleSheet("""
            QSlider::groove:vertical { margin: 9px 1px; }
            QSlider::handle:vertical { width: 20px; height: 20px; }
        """)
        self.bar_pen_size.valueChanged.connect(self.on_pen_size_changed)
        slider_layout.addWidget(self.bar_pen_size)
        self.add_line()
        self.add_button('pen')
        self.add_button('eraser')
        self.add_button('rectangle')
        self.add_button('square')
        self.add_button('bbox')
        self.add_line()
        self.add_button('delete_bbox')
        self.add_button('delete')
        # 添加伸缩项，使按钮靠上显示
        layout.addStretch()
    

    def get_button(self, button_name):
        return getattr(self, self.buttons_dict[button_name][0])


    def enable_buttons(self):
        for button_name in self.buttons_dict.keys():
            button = self.get_button(button_name)
            button.setEnabled(True)

    
    def on_pen_size_changed(self, value):
        print(f"画笔大小: {value}")
    

    def on_button_clicked(self, button_name):
        self.enable_buttons()
        if button_name not in ['delete_bbox', 'delete']: self.active_button = button_name
        if not self.active_button: return
        button = self.get_button(self.active_button)
        button.setEnabled(False)


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
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        line.setFixedSize(30, 1)
        self.layout().addWidget(line)
