from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from main.modules.base.widgets.messagge_box import MessageBox
from main.settings.settings import TASK_TYPE_LIST
from main.db.dao.service import *

class CreateTaskDialog(QDialog):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setWindowTitle('创建任务')
        self.setMinimumWidth(400)
        self.setWindowFlags(Qt.WindowTitleHint)
        self.task_types = list(TASK_TYPE_LIST)
        self.task_type = ''
        self.task_name = ''
        self.init_ui()
        
    def init_ui(self):
        # 创建布局
        layout = QVBoxLayout(self)
        # 任务类型选择部分
        label_task_type = QLabel('任务类型:')
        self.combo_box_task_type = QComboBox()
        self.combo_box_task_type.addItems(self.task_types)
        
        layout_task_type = QHBoxLayout()
        layout_task_type.addWidget(label_task_type)
        layout_task_type.addWidget(self.combo_box_task_type)
        
        # 任务名称输入部分
        label_task_name = QLabel('任务名称:')
        self.line_edit_task_name = QLineEdit()
        self.line_edit_task_name.setPlaceholderText('请输入任务名称')
        
        layout_task_name = QHBoxLayout()
        layout_task_name.addWidget(label_task_name)
        layout_task_name.addWidget(self.line_edit_task_name)
        
        ok_button = QPushButton('确认')
        
        # 添加到主布局
        layout.addLayout(layout_task_type)
        layout.addLayout(layout_task_name)
        layout.addWidget(ok_button)
        
        # 连接按钮信号
        ok_button.clicked.connect(self.on_ok_clicked)
        
    def on_ok_clicked(self):
        self.task_type = self.combo_box_task_type.currentText()
        self.task_name = self.line_edit_task_name.text().strip()
        
        if not self.task_name:
            MessageBox(self.main_window, 'warning', '警告', '任务名称不能为空！', QMessageBox.Ok).run()
            self.line_edit_task_name.clear()
            self.raise_()
            return
        if self.task_name in get_task_name_list():
            MessageBox(self.main_window, 'warning', '警告', '任务名称已存在！', QMessageBox.Ok).run()
            self.line_edit_task_name.clear()
            self.raise_()
            return
        
        self.accept()