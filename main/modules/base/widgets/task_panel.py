from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

from main.settings.path import *
from main.modules.base.widgets.task_node_widget import TaskNodeWidget
from main.modules.base.widgets.task_creation_dialog import CreateTaskDialog
from main.db.dao.service import *


class TaskPanel(QObject):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.widget_task_panel = main_window.widget_task_panel
        self.task_node_dict = dict()
        self.proxy_dict = dict()
    

    def clear_task_panel(self):
        self.task_node_dict.clear()
        self.proxy_dict.clear()
        if self.widget_task_panel.layout():
            layout = self.widget_task_panel.layout()
            QWidget().setLayout(layout)
        # 初始化图形视图、场景、布局
        self.scene = QGraphicsScene(self.widget_task_panel)
        self.scene.setSceneRect(0, 0, self.widget_task_panel.width() - 5, 
                                self.widget_task_panel.height() - 5)
        view = QGraphicsView(self.scene, self.widget_task_panel)
        layout = QVBoxLayout(self.widget_task_panel)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(view)


    def build_tool_chain(self):
        self.clear_task_panel()
        # 获取第一个任务并递归添加
        first_task = get_first_task()
        if first_task:
            self.recursive_add(first_task.task_name)
        # 绘制各节点之间的链接线
        self.draw_connections()


    def recursive_add(self, task_name):
        task = get_task(task_name)
        if task is None: return
        task_node = TaskNodeWidget(self, task)
        # 设置任务节点位置
        if task.toolchain_config.get('pre_task') == 'input':
            task_node.set_location(0, 0)
        else:
            pre_task_name = task.toolchain_config.get('pre_task')
            pre_task = get_task(pre_task_name)
            if pre_task:
                pre_task_node = self.task_node_dict[pre_task.task_name]
                col = pre_task_node.col + 1
                # 获取前序任务的所有后续任务
                pre_next_tasks = pre_task_node.next_tasks
                row = pre_task_node.row + pre_next_tasks.index(task_name)
                task_node.set_location(row, col)
        # 将任务节点添加至画布
        x = 10 + task_node.col * 200
        y = 10 + task_node.row * 50
        proxy = self.scene.addWidget(task_node)
        proxy.setPos(x, y)
        # 存储任务节点
        self.task_node_dict[task_name] = task_node
        self.proxy_dict[task_node.task_name]=proxy
        # 递归添加后续任务
        for next_task in task_node.next_tasks:
            self.recursive_add(next_task)
    

    def draw_connections(self):
        for task_node in self.task_node_dict.values():
            proxy = self.proxy_dict[task_node.task_name]
            pre_task_name = task_node.pre_task
            if pre_task_name == 'input': continue
            from_node = self.task_node_dict[pre_task_name]
            from_proxy = self.proxy_dict[pre_task_name]
            # 计算连接点
            start_x = from_proxy.x() + from_node.width()
            start_y = from_proxy.y() + from_node.height() // 2
            end_x = proxy.x()
            end_y = proxy.y() + task_node.height() // 2
            # 绘制连接线
            path = QPainterPath()
            path.moveTo(start_x, start_y)
            if start_y != end_y:
                mid_x = (start_x + end_x) // 2
                path.moveTo(start_x, start_y)
                path.lineTo(mid_x, start_y)
                path.lineTo(mid_x, end_y)
            path.lineTo(end_x, end_y)
            self.scene.addPath(path, QPen(QColor(93, 71, 139), 2, Qt.SolidLine))
    
    
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
                               toolchain_config=dict(pre_task=pre_task_name, next_tasks=list()))

            # TODO
            # init_task_category(task)
            task_dir.mkdir(parents=True, exist_ok=True)
            if task.task_type in ['segmentation']:
                Path(task_dir, 'annotations').mkdir(exist_ok=True)

            if pre_task_name == 'input': return
            update_pre_task(task_name, pre_task_name)
            self.main_window.update_task(task)
            self.build_tool_chain()
