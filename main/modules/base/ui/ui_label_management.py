from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class UiLabelManagementWidget(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.init_ui()
    
    def init_ui(self):
        # 创建主布局
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(10, 10, 10, 10)
        
        # 创建滚动区域
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setStyleSheet("QScrollArea {border: none;}")
        
        # 创建滚动区域内容widget
        scroll_content = QWidget()
        scroll_content.setStyleSheet("background-color: transparent;")
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_layout.setSpacing(15)
        scroll_layout.setContentsMargins(0, 0, 0, 0)
        
        # 添加视图筛选GroupBox
        groupbox_view_filter = QGroupBox("视图筛选")
        groupbox_view_filter_layout = QVBoxLayout(groupbox_view_filter)
        groupbox_view_filter_layout.setSpacing(10)
        groupbox_view_filter_layout.setContentsMargins(10, 20, 10, 10)
        
        # 添加示例控件到视图筛选
        filter_label = QLabel("筛选条件")
        groupbox_view_filter_layout.addWidget(filter_label)
        
        # 添加数据集统计GroupBox
        groupbox_data_stats = QGroupBox("数据集统计")
        groupbox_data_stats_layout = QVBoxLayout(groupbox_data_stats)
        groupbox_data_stats_layout.setSpacing(10)
        groupbox_data_stats_layout.setContentsMargins(10, 20, 10, 10)
        
        # 添加示例控件到数据集统计
        data_label = QLabel("数据集统计信息")
        groupbox_data_stats_layout.addWidget(data_label)
        
        # 添加标注统计GroupBox
        groupbox_label_stats = QGroupBox("标注统计")
        groupbox_label_stats_layout = QVBoxLayout(groupbox_label_stats)
        groupbox_label_stats_layout.setSpacing(10)
        groupbox_label_stats_layout.setContentsMargins(10, 20, 10, 10)
        
        # 添加示例控件到标注统计
        label_stats_label = QLabel("标注统计信息")
        groupbox_label_stats_layout.addWidget(label_stats_label)
        
        # 将三个GroupBox添加到滚动布局
        scroll_layout.addWidget(groupbox_view_filter)
        scroll_layout.addWidget(groupbox_data_stats)
        scroll_layout.addWidget(groupbox_label_stats)
        scroll_layout.addStretch(1)  # 添加拉伸因子确保底部空间
        
        # 设置滚动区域内容
        scroll_area.setWidget(scroll_content)
        
        # 将滚动区域添加到主布局
        main_layout.addWidget(scroll_area)
        main_layout.addStretch(1)
        