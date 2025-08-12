import sys

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
        self.last_pos = QPoint(0, 0)
        self.mouse_pos = QPoint(-1, -1)
        self.pen_size = 20
        self.is_showing_pen = True
        self.setMouseTracking(True)

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
        self.fit_image_to_widget()
        return True

    

    def paintEvent(self, event):
        if not self.image or self.image.isNull(): return
        # 绘制图片
        painter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing | QPainter.SmoothPixmapTransform)
        image_rect = QRect(self.offset.x(), self.offset.y(), self.scaled_image.width(), self.scaled_image.height())
        painter.drawPixmap(image_rect, QPixmap.fromImage(self.scaled_image))
        # 绘制画笔
        self.paint_pen()
    
    
    def paint_pen(self):
        if not self.is_showing_pen: return
        painter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing | QPainter.SmoothPixmapTransform)
        # 计算圆环半径
        radius = round(self.pen_size / 2)
        # 绘制白色画笔
        painter.setPen(QPen(QColor(255, 255, 255, 200), 1, Qt.SolidLine, Qt.RoundCap))
        painter.drawEllipse(self.mouse_pos, radius, radius)
        # 绘制黑色画笔
        painter.setPen(QPen(QColor(0, 0, 0, 100), 1, Qt.SolidLine, Qt.RoundCap))
        painter.drawEllipse(self.mouse_pos, radius + 1, radius + 1)


    def wheelEvent(self, event):
        if not self.image or self.image.isNull(): return
        # 计算新缩放比例
        factor = 1.1 if event.angleDelta().y() > 0 else 0.9
        old_scale = self.scale
        self.scale = max(0.1, min(10, old_scale * factor))
        # 计算鼠标在图片上的位置
        pos = event.pos()
        image_x = round((pos.x() - self.offset.x()) / old_scale)
        image_y = round((pos.y() - self.offset.y()) / old_scale)
        self.update_image()
        # 确保鼠标指向点不变
        self.offset = QPoint(round(pos.x() - image_x * self.scale), 
                             round(pos.y() - image_y * self.scale))
        self.update()

    def mousePressEvent(self, event):
        if not self.image or self.image.isNull():return
        if event.button() == Qt.RightButton:
            self.is_dragging = True
            self.last_pos = event.pos()
            self.setCursor(Qt.ClosedHandCursor)

    def mouseMoveEvent(self, event):
        if not self.image or self.image.isNull(): return
        old_pos = self.mouse_pos
        self.mouse_pos = event.pos()
        
        if self.is_dragging:
            delta = self.mouse_pos - self.last_pos
            self.offset += delta
            self.last_pos = event.pos()
            self.update()
            return
        
        pen_radius = self.pen_size // 2 + 10
        x1, y1 = old_pos.x() - pen_radius, old_pos.y() - pen_radius
        x2, y2 = self.mouse_pos.x() - pen_radius, self.mouse_pos.y() - pen_radius
        pen_area = QRect(min(x1, x2), min(y1, y2),
                        abs(x1 - x2) + 2 * pen_radius,
                        abs(y1 - y2) + 2 * pen_radius)
        self.update(pen_area)


    def mouseReleaseEvent(self, event):
        if event.button() == Qt.RightButton and self.is_dragging:
            self.is_dragging = False
            self.setCursor(Qt.ArrowCursor)
            
        # 鼠标释放后，显示画笔
        self.is_showing_pen = True
        self.mouse_pos = event.pos()
        
        # 更新画笔区域
        pen_area = QRect(
            self.mouse_pos.x() - self.pen_size//2 - 10,
            self.mouse_pos.y() - self.pen_size//2 - 10,
            self.pen_size + 20,
            self.pen_size + 20
        )
        self.update(pen_area)


    def set_pen_size(self, size):
        self.pen_size = max(1, min(200, size))


    def update_image(self):
        if not self.image or self.image.isNull(): return
        self.scaled_image = self.image.scaled(round(self.image.size().width() * self.scale),
                                              round(self.image.size().height() * self.scale),
                                              Qt.KeepAspectRatio, Qt.SmoothTransformation)

    def fit_image_to_widget(self):
        if not self.image or self.image.isNull(): return
        widget_w, widget_h = self.width(), self.height()
        image_w, image_h = self.image.size().width(), self.image.size().height()
        self.scale = min(widget_w / image_w, widget_h / image_h)
        self.update_image()
        # 居中显示
        self.offset = QPoint(round((widget_w - self.scaled_image.width()) / 2),
                             round((widget_h - self.scaled_image.height()) // 2))
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
    fit_button.clicked.connect(label_tool.fit_image_to_widget)
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