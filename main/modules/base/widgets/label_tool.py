from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QPixmap, QImage
from PyQt5.QtCore import Qt, QPoint, QRect
import sys

class LabelTool(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.image = None
        self.scaled_image = None
        self.scale = 1.0
        self.offset = QPoint(0, 0)
        self.dragging = False
        self.last_pos = QPoint(0, 0)

    def load_image(self, image_path=None, qimage=None):
        if qimage:
            self.image = qimage
        elif image_path:
            self.image = QImage(image_path)
        else:
            return False
        if self.image.isNull():
            return False
        self.reset()
        return True

    def paintEvent(self, event):
        if not self.image or self.image.isNull():
            return

        painter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing | QPainter.SmoothPixmapTransform)

        # 绘制图片
        rect = QRect(int(self.offset.x()), int(self.offset.y()), 
                     self.scaled_image.width(), self.scaled_image.height())
        painter.drawPixmap(rect, QPixmap.fromImage(self.scaled_image))
    

    def wheelEvent(self, event):
        if not self.image or self.image.isNull(): return

        # 计算缩放因子
        factor = 1.1 if event.angleDelta().y() > 0 else 0.9
        new_scale = max(0.1, min(10, self.scale * factor))

        # 计算鼠标在图片上的位置
        mouse_pos = event.pos()
        image_pos = QPoint(round((mouse_pos.x() - self.offset.x()) / self.scale),
                           round((mouse_pos.y() - self.offset.y()) / self.scale))

        # 更新缩放比例和图片
        self.scale = new_scale
        self.update_image()

        # 调整偏移量，使鼠标指向的点保持不变
        self.offset = QPoint(round(mouse_pos.x() - image_pos.x() * self.scale),
                             round(mouse_pos.y() - image_pos.y() * self.scale))
        
        self.update()

    def mousePressEvent(self, event):
        if not self.image or self.image.isNull(): return
        if event.button() == Qt.RightButton:
            self.dragging = True
            self.last_pos = event.pos()
            self.setCursor(Qt.ClosedHandCursor)


    def mouseMoveEvent(self, event):
        if not self.dragging or not self.image or self.image.isNull():
            return

        # 计算偏移量
        delta = event.pos() - self.last_pos
        self.offset += delta
        self.last_pos = event.pos()
        self.update()


    def mouseReleaseEvent(self, event):
        if event.button() == Qt.RightButton and self.dragging:
            self.dragging = False
            self.setCursor(Qt.ArrowCursor)


    def resizeEvent(self, event):
        # 只有在初始状态下才自动调整图片大小
        if self.image and not self.image.isNull():
            if self.scale == 1.0 and self.offset == QPoint(0, 0):
                self.fit_image_to_widget()
        super().resizeEvent(event)


    def update_image(self):
        if not self.image or self.image.isNull():return

        # 缩放图片
        self.scaled_image = self.image.scaled(round(self.image.size().width() * self.scale),
                                              round(self.image.size().height() * self.scale),
                                              Qt.KeepAspectRatio, Qt.SmoothTransformation)

    def fit_image_to_widget(self):
        if not self.image or self.image.isNull(): return

        # 计算缩放比例
        widget_w, widget_h = self.width(), self.height()
        image_w, image_h = self.image.size().width(), self.image.size().height()

        self.scale = min(widget_w / image_w, widget_h / image_h)
        self.update_image()

        # 居中显示
        self.offset = QPoint((widget_w - self.scaled_image.width()) // 2,
                             (widget_h - self.scaled_image.height()) // 2)

        self.update()

    def reset(self):
        if not self.image or self.image.isNull(): return
        # 重置缩放和偏移
        self.scale = 1.0
        self.offset = QPoint(0, 0)
        self.fit_image_to_widget()

if __name__ == '__main__':
    from PyQt5.QtWidgets import QApplication, QPushButton, QVBoxLayout, QWidget
    app = QApplication(sys.argv)
    
    # 创建主窗口和布局
    main_widget = QWidget()
    main_widget.resize(800, 600)
    main_layout = QVBoxLayout(main_widget)
    
    # 创建LabelTool实例和按钮
    label_tool = LabelTool(main_widget)
    label_tool.setMinimumSize(800, 550)
    
    fit_button = QPushButton('适应窗口')
    fit_button.clicked.connect(label_tool.fit_image_to_widget)
    
    # 添加到布局并显示
    main_layout.addWidget(label_tool)
    main_layout.addWidget(fit_button)
    main_widget.show()
    
    # 加载图片
    label_tool.load_image(r'C:\Users\kacif\Downloads\键盘工程测试图片\CLS\OK\00_02_20_727_HXMH1GL3AV3000068L_NUM1.png')

    sys.exit(app.exec_())