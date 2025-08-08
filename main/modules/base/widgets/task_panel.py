from mmengine import ConfigDict

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

from main.settings.path import *
from main.modules.base.widgets.task_node_widget import TaskNodeWidget
from main.modules.base.widgets.task_creation_dialog import CreateTaskDialog
from main.db.dao.service import *


class TaskPanel(object):
    def __init__(self, main_window):
        self.main_window = main_window
        self.widget_task_panel = main_window.widget_task_panel
        self.task_node_dict = dict()


    def build_tool_chain(self):
        first_task = get_first_task()
        self.recursive_add(first_task.task_name)
        pass

    
        
    def recursive_add(self, task_name):
        task = get_task(task_name)
        if task is None: return
        next_tasks = get_next_tasks(task)
        task_node = TaskNodeWidget(self)
        task_node.task = task
        if task.pre_task == 'input':
            task_node.set_location(0, 0)
        else:
            pre_task = get_task(task.pre_task)
            row = get_next_tasks(pre_task).index(task_name)
            col = self.task_node_dict[pre_task.task_name].col + 1
            task_node.set_location(row, col)

        self.task_node_dict[task_name] = task_node
        for next_task in next_tasks:
            self.recursive_add(next_task)
    
    
    def create_task(self, project_name, pre_task_name):
        # 创建任务对话框
        dialog = CreateTaskDialog(self.main_window)
        if dialog.exec() == QDialog.Accepted:
            task_name = dialog.task_name
            task_type = dialog.task_type
            project_dir = Path(BASE_DIR, 'projects', project_name)
            task_dir = Path(project_dir, task_name)
            set_task_inactive()
            task = Task.create(uuid=str(uuid.uuid1()),
                               task_name=task_name,
                               task_type=task_type,
                               project_dir=project_dir.as_posix(),
                               task_dir=task_dir.as_posix(),
                               is_active=True,
                               model_type='',
                               toolchain_config=dict(pre_task=pre_task_name, next_tasks=[]))
            # TODO
            # init_task_category(task)
            task_dir.mkdir(parents=True, exist_ok=True)
            if task.task_type in ['segmentation']:
                Path(task_dir, 'annotations').mkdir(exist_ok=True)

            if pre_task_name == 'input': return
            update_pre_task(task_name, pre_task_name)
            self.main_window.update_task(task)
            self.build_tool_chain()
