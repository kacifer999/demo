import sys
import numpy as np

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class LabelTool(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.image = None
        self.scaled_image = None
        self.scale = 1.0
        self.offset = QPoint(0, 0) # 图像对于窗口的偏移量
        self.is_dragging = False
        self.last_drag_pos = None
        self.mouse_pos = None
        self.pen_size = 20
        self.is_showing_pen = True
        self.setMouseTracking(True)
        self.image_layer = None
        self.pen_layer = None
        self.init_layers()
    

    def init_layers(self):
        self.image_layer = QImage(self.size(), QImage.Format_ARGB32)
        self.pen_layer = QImage(self.size(), QImage.Format_ARGB32)
        self.image_layer.fill(Qt.transparent)
        self.pen_layer.fill(Qt.transparent)


    def load_image(self, image_path=None, qimage=None):
        if qimage:
            self.image = qimage
        elif image_path:
            self.image = QImage(image_path)
        else:
            return False

        if self.image.isNull():
            return False
        self.scale = 1.0
        self.offset = QPoint(0, 0)
        self.init_layers()
        self.fit_image()
        return True


    def update_image_layer(self):
        self.image_layer.fill(Qt.transparent)
        if not self.image or self.image.isNull(): return
        painter = QPainter(self.image_layer)
        painter.setRenderHints(QPainter.Antialiasing | QPainter.SmoothPixmapTransform)
        rect = QRect(self.offset.x(), self.offset.y(), self.scaled_image.width(), self.scaled_image.height())
        painter.drawPixmap(rect, QPixmap.fromImage(self.scaled_image))
        painter.end()
        self.update_pen_layer()


    def update_pen_layer(self):
        self.pen_layer.fill(Qt.transparent)
        if not self.is_showing_pen or self.mouse_pos is None: return
        painter = QPainter(self.pen_layer)
        painter.setRenderHints(QPainter.Antialiasing | QPainter.SmoothPixmapTransform)
        radius = round(self.pen_size / 2)
        # 绘制黑色画笔
        painter.setPen(QPen(QColor(0, 0, 0, 100), 2, Qt.SolidLine, Qt.RoundCap))
        painter.drawEllipse(self.mouse_pos, radius - 1, radius - 1)
        # 绘制白色画笔
        painter.setPen(QPen(QColor(255, 255, 255, 200), 2, Qt.SolidLine, Qt.RoundCap))
        painter.drawEllipse(self.mouse_pos, radius - 2, radius - 2)
        painter.end()


    def paintEvent(self, event):
        if not self.image or self.image.isNull(): return
        painter = QPainter(self)
        painter.drawImage(0, 0, self.image_layer)
        painter.drawImage(0, 0, self.pen_layer)
        painter.end()


    def wheelEvent(self, event):
        if not self.image or self.image.isNull(): return
        self.set_mouse_pos(event.pos())
        # 计算新缩放比例
        factor = 1.25 if event.angleDelta().y() > 0 else 0.8
        old_scale = self.scale
        self.scale = np.clip(old_scale * factor, 0.1, 10)
        self.update_image(self.scale)
        # 计算新的偏移量
        x = round((self.mouse_pos.x() - self.offset.x()) / old_scale * self.scale)
        y = round((self.mouse_pos.y() - self.offset.y()) / old_scale * self.scale)
        self.offset = QPoint(self.mouse_pos.x() - x, self.mouse_pos.y() - y)
        # 更新图像图层
        self.update_image_layer()
        self.update()


    def mousePressEvent(self, event):
        if not self.image or self.image.isNull():return
        self.set_mouse_pos(event.pos())
        if event.button() == Qt.RightButton and self.mouse_pos == event.pos():
            self.is_dragging = True
            self.last_drag_pos = self.mouse_pos
            self.setCursor(Qt.ClosedHandCursor)


    def mouseMoveEvent(self, event):
        if not self.image or self.image.isNull(): return
        self.set_mouse_pos(event.pos())
        # 拖动图像
        if self.is_dragging:
            self.offset += self.mouse_pos - self.last_drag_pos
            self.last_drag_pos = self.mouse_pos
            self.update_image_layer()
            self.update()
            return
        
        self.update_pen_layer()
        self.update()


    def mouseReleaseEvent(self, event):
        if not self.image or self.image.isNull(): return
        self.set_mouse_pos(event.pos())
        if event.button() == Qt.RightButton and self.is_dragging:
            self.is_dragging = False
            self.setCursor(Qt.ArrowCursor)
        
        # 更新画笔
        self.update_pen_layer()
        self.update()


    def set_mouse_pos(self, pos):
        rect = QRect(self.offset.x(), self.offset.y(),
                           self.scaled_image.width(), self.scaled_image.height())
        self.mouse_pos = QPoint(np.clip(pos.x(), rect.left(), rect.right()),
                                    np.clip(pos.y(), rect.top(), rect.bottom()))


    def set_pen_size(self, size):
        self.pen_size = max(1, min(200, size))
        self.update_pen_layer()
        self.update()


    def update_image(self, scale):
        if not self.image or self.image.isNull(): return
        self.scaled_image = self.image.scaled(round(self.image.size().width() * scale),
                                              round(self.image.size().height() * scale),
                                              Qt.KeepAspectRatio, Qt.SmoothTransformation)


    def fit_image(self):
        if not self.image or self.image.isNull(): return
        self.scale = min(self.width() / self.image.size().width(), 
                         self.height() / self.image.size().height())
        self.update_image(self.scale)
        # 计算偏移量
        self.offset = QPoint(round((self.width() - self.scaled_image.width()) / 2),
                             round((self.height() - self.scaled_image.height()) / 2))
        self.update_image_layer()
        self.update()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    # 创建主窗口和布局
    main_widget = QWidget()
    main_widget.resize(800, 600)
    main_layout = QVBoxLayout(main_widget)
    # 创建LabelTool实例
    label_tool = LabelTool(main_widget)
    label_tool.setMinimumSize(800, 550)
    # 创建按钮和滑块
    fit_button = QPushButton('适应窗口')
    fit_button.clicked.connect(label_tool.fit_image)
    # 画笔大小调节滑块
    pen_size_label = QLabel('画笔大小:')
    pen_size_slider = QSlider(Qt.Horizontal)
    pen_size_slider.setRange(5, 100)
    pen_size_slider.setValue(label_tool.pen_size)
    pen_size_slider.valueChanged.connect(label_tool.set_pen_size)
    # 创建滑块布局
    slider_layout = QHBoxLayout()
    slider_layout.addWidget(pen_size_label)
    slider_layout.addWidget(pen_size_slider)
    # 添加到布局并显示
    main_layout.addWidget(label_tool)
    main_layout.addWidget(fit_button)
    main_layout.addLayout(slider_layout)
    main_widget.show()
    # 加载示例图片
    label_tool.load_image(r'C:\Users\kacif\Downloads\键盘工程测试图片\CLS\OK\00_02_20_727_HXMH1GL3AV3000068L_NUM1.png')

    sys.exit(app.exec_())