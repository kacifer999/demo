from pathlib import Path
from win32api import GetMonitorInfo, MonitorFromPoint

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from main.settings.path import *
from main.db.dao.service import *
from main.modules.base.widgets import *

from main.modules.base.ui.ui_main_window import UiMainWindow
from main.modules.base.widgets.project_panel import ProjectPanel
from main.modules.base.widgets.task_panel import TaskPanel
from main.modules.base.widgets.button_panel import ButtonPanel
from main.modules.base.widgets.progress_bar import ProgressBar


# logger = get_root_logger(name='main_window', log_level=logging.INFO)


# 主界面类
class MainWindow(UiMainWindow):
    def __init__(self, name="Demo"):
        super().__init__()
        self.name = name
        self.project_name = None
        self.project_db = None
        self.task = None
        # 获取当前屏幕尺寸  
        monitor_info = GetMonitorInfo(MonitorFromPoint((0,0)))
        work_width, work_height = monitor_info.get("Work")[2:4]
        # 设置窗口固定大小，不可拖拽变形
        self.setFixedSize(work_width, work_height - 25)
        self.setWindowState(Qt.WindowMaximized)
        self.showMaximized()
        self.hide()
        # 添加工程界面
        self.project_panel = ProjectPanel(self)
        # 添加任务界面
        self.task_panel = TaskPanel(self)
        # 添加按钮界面
        self.button_panel = ButtonPanel(self)


        # 添加进度条
        self.progress_bar = ProgressBar(self)

        
        # 计划队列
        # self.scheduler = Scheduler(self)
        # self.log_horizontal_bar = LogHorizontalBar(self)

        # Debug
        # self.debug_console = DebugConsole(self）
        self.connect_view_menu_actions()
        self.project_panel.load_project_panel()
    

    def connect_view_menu_actions(self):
        # 显示/隐藏工程管理
        self.action_project_panel.triggered.connect(self.project_panel.show_project_panel)
        # 显示/隐藏任务管理作
        self.action_task_panel.triggered.connect(self.task_panel.show_task_panel)
    

    def adjust_window_geometry(self):
        self.ui_task_panel.hide()
        self.ui_task_panel.showMaximized()
        self.task_panel.build_task_panel()


    def build_project(self, project_name):
        self.project_name = project_name
        if project_name is not None:
            self.connect_db()
            self.build_task()
        else:
            self.task_panel.clear_task_panel()

    
    def build_task(self):
        self.task = get_active_task()
        self.task_panel.build_task_panel()
        self.set_window_title()


    def set_window_title(self):
        title = f'{self.name}'
        if self.project_name is not None:
            title += f' - 工程: {self.project_name}' 

        if self.task is not None:
            title += f' - 任务: {self.task.task_name}' 

        self.label_title.setText(title)


    def update_task(self, task):
        task.save()
        self.task = task
    

    def connect_db(self):
        self.close_db()
        db_dir = Path(BASE_DIR,'projects', self.project_name,'project.db').as_posix()
        self.project_db = connect_db(db_dir)
    

    def close_db(self):
        close_db(self.project_db)
        self.project_db = None


    def update_progress_bar(self, index, total):
        self.progress_bar.update_bar('main_bar', round((index + 1) / total * 100))
    


