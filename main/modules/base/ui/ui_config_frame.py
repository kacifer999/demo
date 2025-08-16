from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class UiConfigFrame(QFrame):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setFrameShape(QFrame.NoFrame)
        self.setFrameShadow(QFrame.Plain)
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
        self.setFixedWidth(500)
        self.init_ui()
    
    def init_ui(self):
        # 创建主布局
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # 创建QTabWidget
        self.tab_widget = QTabWidget()
        
        # 设置TabBar显示在右侧
        self.tab_widget.setTabPosition(QTabWidget.TabPosition.East)
        
        # 创建页面内容
        self.task_config_tab = QWidget()
        self.annotation_management_tab = QWidget()
        self.params_settings_tab = QWidget()
        self.result_analysis_tab = QWidget()
        
        # 将页面添加到QTabWidget
        self.tab_widget.addTab(self.task_config_tab, "")
        self.tab_widget.addTab(self.annotation_management_tab, "")
        self.tab_widget.addTab(self.params_settings_tab, "")
        self.tab_widget.addTab(self.result_analysis_tab, "")
        
        # 获取TabBar
        tab_bar = self.tab_widget.tabBar()
        
        tab_bar.setStyleSheet("""
            QTabBar::tab {
                height: 120px;
                width: 35px;
                background-color: transparent;
                border: none;
                margin: 0px;
                padding: 2px;
            }
            QTabBar::tab:selected {
                background-color: #ffffff;
                border-right: 1px solid #ffffff;
            }
        """)
        
        # 按钮样式
        button_style = """
            QPushButton {
                height: 120px;
                width: 35px;
                font-family: 'Microsoft YaHei';
                font-size: 12px;
                color: #333333;
                background-color: transparent;
                border: none;
                padding: 2px;
                margin: 0px;
            }
            QPushButton:hover {
                color: #1a73e8;
            }
        """
        
        # 添加自定义Tab按钮
        tab_labels = ["任务配置", "标注管理", "参数设置", "结果分析"]
        for i, label in enumerate(tab_labels):
            button = QPushButton()
            button.setText(self.vertical_text(label))
            button.setStyleSheet(button_style)
            button.clicked.connect(lambda checked, idx=i: self.tab_widget.setCurrentIndex(idx))
            
            # 将按钮添加到TabBar
            tab_bar.setTabButton(i, QTabBar.ButtonPosition.RightSide, button)
            tab_bar.setTabText(i, "")  # 清空原有的tab文本
        
        # 将QTabWidget添加到主布局
        main_layout.addWidget(self.tab_widget)
        
        # 默认选中第一个标签页
        self.tab_widget.setCurrentIndex(0)


    def vertical_text(self, text):
        return '\n'.join(text)
