from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class UiTaskConfigWidget(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.init_ui()
    
    def init_ui(self):
        # 创建主布局
        layout_main = QVBoxLayout(self)
        layout_main.setSpacing(5)
        layout_main.setContentsMargins(5, 5, 5, 5)
        self.setLayout(layout_main)
        self.init_toolchain_config()
        self.init_model_config()
        layout_main.addStretch(1)
    
    def init_toolchain_config(self):
        # 创建工具链配置GroupBox
        group_box_toolchain = QGroupBox('工具链配置')
        self.main_window.group_box_toolchain = group_box_toolchain
        layout_toolchain = QGridLayout()
        layout_toolchain.setContentsMargins(0, 0, 0, 0)
        layout_toolchain.setVerticalSpacing(5)
        layout_toolchain.setHorizontalSpacing(10)
        group_box_toolchain.setLayout(layout_toolchain)
        self.layout().addWidget(group_box_toolchain)
        # 过滤标签
        label_filter_tag = QLabel('过滤标签:')
        self.main_window.label_filter_tag = label_filter_tag
        layout_toolchain.addWidget(label_filter_tag, 0, 0)
        combo_box_filter_tag = QComboBox()
        self.main_window.combo_box_filter_tag = combo_box_filter_tag
        self.main_window.setStyleSheet('color: white;')
        layout_toolchain.addWidget(combo_box_filter_tag, 0, 1)
        # 过滤分数
        label_filter_score = QLabel('过滤分数:')
        self.main_window.label_filter_score = label_filter_score
        layout_toolchain.addWidget(label_filter_score, 0, 2)
        combo_box_filter_score = QDoubleSpinBox()
        self.main_window.combo_box_filter_score = combo_box_filter_score
        combo_box_filter_score.setValue(0.5)
        combo_box_filter_score.setSingleStep(0.05)
        combo_box_filter_score.setRange(0.05, 0.95)
        combo_box_filter_score.setStyleSheet('color: white;')
        layout_toolchain.addWidget(combo_box_filter_score, 0, 3)
        # 应用过滤
        button_apply_filter = QPushButton('应用过滤')
        self.main_window.button_apply_filter = button_apply_filter
        button_apply_filter.setFocusPolicy(Qt.NoFocus)
        layout_toolchain.addWidget(button_apply_filter, 1, 2, 1, 2)
        

    def init_model_config(self):
        group_box_model_config = QGroupBox('模型配置')
        layout_model_config = QGridLayout()
        layout_model_config.setContentsMargins(5, 5, 5, 5)
        layout_model_config.setVerticalSpacing(5)
        layout_model_config.setHorizontalSpacing(20)
        group_box_model_config.setLayout(layout_model_config)
        self.layout().addWidget(group_box_model_config)
        # 模型大小
        label_model_size = QLabel('模型大小:')
        self.main_window.label_model_size = label_model_size
        layout_model_config.addWidget(label_model_size, 0, 0)
        combo_box_model_size = QComboBox()
        combo_box_model_size.addItems(['小', '中', '大'])
        self.main_window.combo_box_model_size = combo_box_model_size
        self.main_window.setStyleSheet("color: white;")
        layout_model_config.addWidget(combo_box_model_size, 0, 1)
        # 模型精度
        label_model_precision = QLabel('模型精度:')
        self.main_window.label_model_precision = label_model_precision
        layout_model_config.addWidget(label_model_precision, 0, 2)
        combo_box_model_precision = QComboBox()
        combo_box_model_precision.addItems(['FP16', 'INT8'])
        self.main_window.combo_box_model_precision = combo_box_model_precision
        self.main_window.setStyleSheet("color: white;")
        layout_model_config.addWidget(combo_box_model_precision, 0, 3)


