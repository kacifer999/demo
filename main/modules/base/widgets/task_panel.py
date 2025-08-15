import shutil
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from main.settings.path import *
from main.modules.base.widgets.task_node_widget import TaskNodeWidget
from main.modules.base.widgets.task_creation_dialog import CreateTaskDialog
from main.modules.base.widgets.messagge_box import MessageBox

from main.db.dao.service import *


class TaskPanel(QObject):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.panel = main_window.widget_task_panel
        self.panel.installEventFilter(self)
        self.selected_task_name = None
        self.task_node_dict = dict()
        self.proxy_dict = dict()
        self.location_list = list()


    def eventFilter(self, obj, event):
        if obj == self.panel and event.type() == QEvent.Resize:
            self.build_task_panel()
        return super().eventFilter(obj, event)


    def clear_task_panel(self):
        self.selected_task_name = None
        for task_node in self.task_node_dict.values():
            task_node.signal_create_task.disconnect()
            task_node.signal_delete_task.disconnect()
            task_node.signal_select_task.disconnect()
            task_node.deleteLater()

        if self.panel.layout():
            layout = self.panel.layout()
            QWidget().setLayout(layout)
        
        self.task_node_dict.clear()
        self.proxy_dict.clear()
        self.location_list.clear()
        # 初始化图形视图、场景、布局
        self.scene = QGraphicsScene(self.panel)
        # 初始场景大小设为视图大小
        self.scene.setSceneRect(0, 0, self.panel.width() - 10, 
                                      self.panel.height() - 10)
        # 创建视图
        view = QGraphicsView(self.scene, self.panel)
        view.setStyleSheet("border: none; border-radius: 0px;")
        # 初始设置为不显示滚动条
        view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        # 创建布局并添加视图
        layout = QVBoxLayout(self.panel)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(view)
        self.view = view


    def build_task_panel(self):
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
        # 创建任务节点并连接信号
        task_node = TaskNodeWidget(self, task)
        task_node.signal_create_task.connect(self.create_task)
        task_node.signal_delete_task.connect(self.delete_task)
        task_node.signal_select_task.connect(self.select_task)
        if task.is_active:
            self.selected_task_name = task_name
            task_node.setStyleSheet('background-color: rgb(200, 200, 200);')
        else:
            task_node.setStyleSheet('background-color: rgb(120, 120, 120);')
        
        # 设置任务节点位置
        prev_task_name = task.toolchain_config.get('prev_task')
        if prev_task_name == 'input':
            task_node.set_location(0, 0)
        else:
            prev_task = get_task(prev_task_name)
            if prev_task:
                prev_node = self.task_node_dict[prev_task.task_name]
                col, row = prev_node.col + 1, prev_node.row + prev_node.next_tasks.index(task_name)
                while (row, col) in self.location_list: row += 1
                self.location_list.append((row, col))
                task_node.set_location(row, col)

        # 将任务节点添加至画布
        x = 10 + task_node.col * 200
        y = 10 + task_node.row * 50
        proxy = self.scene.addWidget(task_node)
        proxy.setPos(x, y)
        # 存储任务节点
        self.task_node_dict[task_name] = task_node
        self.proxy_dict[task_node.task_name]=proxy
        # 检查是否需要调整场景大小
        rect = QRectF(0, 0, max(self.scene.width(), x + task_node.width() + 10), 
                            max(self.scene.height(), y + task_node.height() + 10))
        if rect != self.scene.sceneRect():
            self.scene.setSceneRect(rect)
            # 检查是否需要显示滚动条
            h_policy = Qt.ScrollBarAlwaysOn if rect.width() > self.view.width() else Qt.ScrollBarAlwaysOff
            v_policy = Qt.ScrollBarAlwaysOn if rect.height() > self.view.height() else Qt.ScrollBarAlwaysOff
            self.view.setHorizontalScrollBarPolicy(h_policy)
            self.view.setVerticalScrollBarPolicy(v_policy)
        
        # 递归添加后续任务
        for next_task in task_node.next_tasks:
            self.recursive_add(next_task)
    

    def draw_connections(self):
        for task_node in self.task_node_dict.values():
            proxy = self.proxy_dict[task_node.task_name]
            prev_task_name = task_node.prev_task
            if prev_task_name == 'input': continue
            from_node = self.task_node_dict[prev_task_name]
            from_proxy = self.proxy_dict[prev_task_name]
            # 计算连接点
            start_x = from_proxy.x() + from_node.width() + 1
            start_y = from_proxy.y() + from_node.height() // 2
            end_x = proxy.x() - 1
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
    
    
    def create_task(self, project_name, prev_task_name):
        # 创建任务对话框
        dialog = CreateTaskDialog(self.main_window)
        if dialog.exec() == QDialog.Accepted:
            task_name = dialog.task_name
            task_type = dialog.task_type
            project_dir = Path(BASE_DIR, 'projects', project_name)
            task_dir = Path(project_dir, task_name)
            set_task_inactive()
            task = TaskModel.create(uuid=str(uuid.uuid1()),
                               task_name=task_name,
                               task_type=task_type,
                               project_dir=project_dir.as_posix(),
                               task_dir=task_dir.as_posix(),
                               is_active=True,
                               model_type='',
                               toolchain_config=dict(prev_task=prev_task_name, next_tasks=list()))

            # TODO
            # init_task_category(task)
            task_dir.mkdir(parents=True, exist_ok=True)
            if task.task_type in ['segmentation']:
                Path(task_dir, 'annotations').mkdir(exist_ok=True)

            if prev_task_name == 'input': return
            change_next_tasks(task_name, prev_task_name)
            self.main_window.update_task(task)
            QTimer.singleShot(0, self.main_window.build_task)
    
    def delete_task(self, task_name):
        # 删除任务对话框
        msg = '确认删除任务？'
        if MessageBox(self.main_window, 'information', '提示', msg, QMessageBox.Ok|QMessageBox.Cancel).run(): return
        task = get_task(task_name)
        if task is None: return
        prev_task_name = task.toolchain_config.get('prev_task')
        change_next_tasks(task_name, prev_task_name, remove=True)
        prev_task = get_task(prev_task_name)
        if task.is_active:
            prev_task.is_active = True

        delete_task_dbs(task)
        shutil.rmtree(task.task_dir, ignore_errors=True)
        shutil.rmtree(Path(task.project_dir, 'sdk', task_name), ignore_errors=True)
        self.main_window.update_task(prev_task)
        QTimer.singleShot(0, self.main_window.build_task)

    
    def select_task(self, task_name):
        if self.selected_task_name == task_name:return
        self.selected_task_name = task_name
        set_task_inactive()
        task = get_task(task_name)
        if task is None: return
        task.is_active = True
        self.main_window.update_task(task)
        QTimer.singleShot(0, self.main_window.build_task)
    
    def show_task_panel(self):
        if self.main_window.action_task_panel.isChecked():
            self.main_window.ui_task_panel.show()
        else:
            self.main_window.ui_task_panel.hide()
