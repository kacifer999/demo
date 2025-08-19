from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from main.modules.base.ui.ui_task_config import UiTaskConfigWidget
from main.modules.base.ui.ui_label_management import UiLabelManagementWidget

class UiConfigFrame(QFrame):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setFrameShape(QFrame.NoFrame)
        self.setFrameShadow(QFrame.Plain)
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
        self.setFixedWidth(500)
        self.tab_dict = {'任务配置': (0, UiTaskConfigWidget(self.main_window)),
                         '标注管理': (1, UiLabelManagementWidget(self.main_window)),
                         '参数设置': (2, QWidget()),
                         '结果分析': (3, QWidget()),
                        }
        self.init_ui()
    
    def init_ui(self):
        # 创建主布局
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # 创建QTabWidget并设置右侧标签
        self.tab_widget = QTabWidget()
        self.tab_widget.setTabPosition(QTabWidget.TabPosition.East)
        # 设置TabBar样式
        tab_bar = self.tab_widget.tabBar()
        tab_bar.setStyleSheet("""
            QTabBar::tab {
                height: 100px; 
                width: 30px;
                background-color: 
                transparent;
                border: none; padding: 0px;
            }
            QTabBar::tab:selected { background-color: rgb(150, 150, 150); }
        """)

        for tab_name, (tab_index, tab_widget) in self.tab_dict.items():
            self.tab_widget.addTab(tab_widget, '')
            button = QPushButton(self.vertical_text(tab_name))
            button.setFixedSize(30, 100)
            button.setStyleSheet("""
                QPushButton {
                    color: #ffffff;
                    font-size: 13px;
                    background-color: transparent;
                    border: none;
                    padding: 0px;
                    margin: 0px;
                    text-align: center;}
            """)
            button.setCheckable(True)
            button.clicked.connect(lambda _, name=tab_name: self.select_tab(name))
            tab_bar.setTabButton(tab_index, QTabBar.ButtonPosition.RightSide, button)


        
        # 默认选中第一个标签页和按钮
        self.tab_widget.setCurrentIndex(0)
        # 添加TabWidget到主布局
        main_layout.addWidget(self.tab_widget)
    
    def select_tab(self, tab_name):
            tab_index, tab_widget = self.tab_dict[tab_name]
            self.tab_widget.setCurrentIndex(tab_index)

    def vertical_text(self, text):
        return '\n'.join(text)
        
    
