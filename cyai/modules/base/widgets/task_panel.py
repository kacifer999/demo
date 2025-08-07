from mmengine import ConfigDict

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

from cyai.settings.path import *
from cyai.modules.base.widgets.task_node_widget import TaskNodeWidget
from cyai.modules.base.widgets.messagge_box import MessageBox

class TaskPanel(object):
    def __init__(self, main_window):
        self.main_window = main_window
        self.widget_task_panel = main_window.widget_task_panel
        self.task_node_dict = dict()
        self.first_task = ConfigDict(dict(task_name = 'ROI',
                                          net_class = 'cytools',
                                          net_type = 'ROI'))


    def build_tool_chain(self):
        # self.widget_task_panel.clear()
        for child in self.widget_task_panel.children():
            child.setParent(None)

        self.task_node_dict.clear()

        self.recursive_add(self.first_task.task_name)
        self.build_scene()
    
        
    def recursive_add(self, task_name):
        task = get_task(task_name)
        if task is None: return
        next_tasks = get_next_tasks(task)
        task_node = TaskNodeWidget(self.main_window, self)
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
    
    def create_first_task(self):
        action = QAction('ROI')
        action.setProperty('net_class', self.first_task.net_class)
        action.setProperty('net_type', self.first_task.net_type)
        action.setProperty('pre_task', 'input')
        task_node = TaskNodeWidget(self.main_window, self)
        task_node.create_task(action)

    
    # def create_task(self, action):
    #     net_class = action.property('net_class')
    #     net_type = action.property('net_type')
    #     pre_task_name = action.property('pre_task')


    #     if pre_task_name not in ['input']:
    #         pre_task = get_task(pre_task_name)
    #         if pre_task.net_class not in ['cytools'] and \
    #            len(get_task_category_name_list(pre_task, remove_unlabel=True)) == 0:
    #             msg = f'所选模型:  {pre_task_name}\n 没有创建任何标签，请创建后重试！'
    #             MessageBox(self.main_window, 'warning', '警告', msg, QMessageBox.Ok).run()
    #             return

    #     if net_class in ['cytools']:
    #         task_name = net_type
    #     else:
    #         task_name, ok = QInputDialog().getText(self.main_window, '当前任务名称', "请输入任务名称:", QLineEdit.Normal, "")
    #         if not ok: return
    #         if task_name == "":
    #             msg = f'任务名称不能为空！'
    #             MessageBox(self.main_window, 'warning', '警告', msg, QMessageBox.Ok).run()
    #             return

    #         if task_name in get_all_task_names():
    #             msg = f'任务名已经存在！'
    #             MessageBox(self.main_window, 'warning', '警告', msg, QMessageBox.Ok).run()
    #             return
        
    #     set_task_inactive()
    #     task = create_task(base_dir=BASE_DIR,
    #                        task_name=task_name, 
    #                        project_name=self.main_window.project_name, 
    #                        net_class=net_class, 
    #                        net_type=net_type, 
    #                        pre_task = pre_task_name)
    #     initiate_task_category(task)
        
    #     # 初始化ROI
    #     if net_type in ['ROI']:
    #         pass
    #         # create_roi(1, task_name, {'x': 0.0, 'y': 0.0, 'w': 1.0, 'h': 1.0})
        
    #     pre_tool = get_pre_tool(task)
    #     if pre_tool in ['ROI']:
    #         pass
    #         #  apply_rois_to_views(pre_task)
        
    #     task_dir = Path(BASE_DIR, 'projects', self.main_window.project_name, task_name)

    #     # 创建task目录
    #     task_dir = Path(BASE_DIR, 'projects', self.main_window.project_name, task_name)
    #     if net_class not in ['cytools']:
    #         task_dir.mkdir(exist_ok=True)
    #     if net_class in ['segmentation', 'anomaly']:
    #         Path(task_dir, 'annotation_images').mkdir(exist_ok=True)

    #     self.main_window.update_task(task)
    #     self.build_tool_chain()


    
    def build_scene(self):

        # self.scene.clear()
        # pen = QPen()
        # pen.setColor(QColor(0, 0, 255))

        max_rows = 0

        for task_name in self.task_node_dict.keys():
            task = get_task(task_name)
            next_tasks = get_next_tasks(task)
            max_rows = max(max_rows, len(next_tasks))

        for task_name, task_node in self.task_node_dict.items():
            # task_node.move(task_node.col * 220, task_node.row * 100)
            # self.widget_task_panel.addWidget(task_node)
            # proxy = QGraphicsProxyWidget()
            # proxy.setWidget(task_node)
            task_node.move(task_node.col * 220, task_node.row * 100)
            print('!!!!!',task_name)
            
        
        
        # self.scene.update()


        # self.scene.update()
        # for task_name in self.map_between_task_name_and_task_node.keys():
        #     task = get_task(task_name)
        #     next_task_name_list = json.loads(task.next_task)
        #     task_node = self.map_between_task_name_and_task_node[task_name]
        #     task_point = QPoint(task_node.x() + task_node.width(), task_node.y() + task_node.height() / 2)

        #     index_in_pre_task = 0
        #     previous_task = get_task(task.previous_task)
        #     if previous_task:
        #         index_in_pre_task = json.loads(previous_task.next_task).index(task_name)

        #     point_x = 0
        #     for index, next_task_name in enumerate(next_task_name_list):
        #         next_task_node = self.map_between_task_name_and_task_node[next_task_name]
        #         next_task_point = QPoint(next_task_node.x(), next_task_node.y() + next_task_node.height() / 2)

        #         if task_node.row() == next_task_node.row():
        #             line_item = QGraphicsLineItem(task_point.x(), task_point.y(),
        #                                           next_task_point.x(), next_task_point.y())
        #             line_item.setPen(pen)
        #             self.scene.addItem(line_item)

        #         else:
        #             if not point_x:
        #                 point_x = task_point.x() + (next_task_point.x() - task_point.x() - 20 - 8 * index_in_pre_task)

        #             polyline_first_point = QPoint(point_x, task_point.y())
        #             polyline_second_point = QPoint(point_x, next_task_point.y())

        #             first_line_item = QGraphicsLineItem(task_point.x(), task_point.y(),
        #                                                 polyline_first_point.x(), polyline_first_point.y())

        #             first_line_item.setPen(pen)
        #             self.scene.addItem(first_line_item)

        #             second_line_item = QGraphicsLineItem(polyline_first_point.x(), polyline_first_point.y(),
        #                                                  polyline_second_point.x(), polyline_second_point.y())
        #             second_line_item.setPen(pen)
        #             self.scene.addItem(second_line_item)

        #             third_line_item = QGraphicsLineItem(polyline_second_point.x(), polyline_second_point.y(),
        #                                                 next_task_point.x(), next_task_point.y())
        #             third_line_item.setPen(pen)
        #             self.scene.addItem(third_line_item)

        #             self.scene.update()