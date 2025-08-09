

from pathlib import Path
from mmengine import ConfigDict
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from win32api import GetMonitorInfo, MonitorFromPoint

from main.settings.path import *
from main.modules.base.widgets import *
from main.modules.base.ui.ui_main_window import UiMainWindow
from main.db.dao.service import *

# logger = get_root_logger(name='main_window', log_level=logging.INFO)


# 主界面类
class MainWindow(UiMainWindow):
    """
    主界面类，继承自QMainWindow类，统筹管理各个模块，对主要事件进行处理
    """
    def __init__(self, name="Demo"):
        super().__init__()
        self.name = name
        self.project_name = None
        self.project_db = None
        self.task = None
        
        
        # 获取当前屏幕尺寸  
        monitor_info = GetMonitorInfo(MonitorFromPoint((0,0)))
        _, _, work_witdh, work_height= monitor_info.get("Work")
        # 设置窗口固定大小，不可拖拽变形
        self.setFixedSize(work_witdh, work_height - 25)
        self.setWindowState(Qt.WindowMaximized)
        self.show()
        self.set_window_title()

        # 添加任务管理
        self.task_panel = TaskPanel(self)
        
        # 添加工程管理
        self.projec_panel = ProjectPanel(self)
        self.action_project_panel.changed.connect(self.projec_panel.show_project_panel)

        
        


        # 计划队列
        # self.scheduler = Scheduler(self)
        # self.progress_bar = ProgressHorizontalBar(self)
        # self.log_horizontal_bar = LogHorizontalBar(self)

        # Debug
        # self.debug_console = DebugConsole(self）
    

    def build_project(self, project_name, new_project = False):
        self.project_name = project_name

        if project_name is not None:
            close_db(self.project_db)
            db_dir = Path(BASE_DIR,'projects', project_name,'project.db')
            self.project_db = connect_db(db_dir.as_posix())
            # if new_project:
            #     self.task_panel.create_first_task()

            self.task = get_active_task()
            if self.task is not None:
                pass
            # task_type = self.scheduler.check_task_in_queue(self.task.uuid)
            # if isinstance(task_type, list):
            #     set_task_inactive(self.task)
            #     self.task = get_active_task()
            self.task_panel.build_tool_chain()
            # self.tool_chain_widget.show()
            # self.set_to_task(self.task)
        else:
            self.task = None
            # self.ui.action_train_procedure_analysis.setEnabled(False)
            # self.task_panel.scene.clear()

        self.set_window_title()


    def set_window_title(self):
        title = f'{self.name}'
        if self.project_name is not None:
            title += f' - 工程: {self.project_name}' 

        if self.task is not None:
            title += f' - 任务: {self.task.task_name}' 

        self.setWindowTitle(title)

    def update_task(self, task):
        self.task = task

    def resizeEvent(self, event):
        # 窗口大小改变时调用
        return
