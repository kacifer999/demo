import json
import logging
import os
import shutil
from pathlib import Path
import types
from mmengine import ConfigDict

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

from cyai.settings.path import *
from cyai.modules.base.widgets.messagge_box import MessageBox
from cyai.modules.base.ui.ui_task_node import UiTaskNodeWidget


# from cyai.modules.base.service.logger import get_root_logger
# from cyai.settings.paths import BASE_DIR
# from cyai.settings.constant import name_to_task_mode, task_mode_to_net_class, net_type_ditc, task_mode_to_name
# from cyai.modules.base.service.misc import message_box, message_box_to_info
# from ai_hub.cyai.dao.utils import *
# from cyai.modules.base.dao.service import *
# from cyai.modules.base.service.toolchain_utils import pre_task_change, get_filter_config
# from cyai.modules.base.service.sdk_utils import create_sdk_bestpth_md5_file, create_bestpth_md5_file

# logger = get_root_logger(name='task_node_widget', log_level=logging.INFO)


class TaskNodeWidget(UiTaskNodeWidget):

    # task_selected = pyqtSignal(str)
    # set_to_task = pyqtSignal(str)

    def __init__(self, main_window=None, task_panel=None):
        super(TaskNodeWidget, self).__init__()
        self.main_window = main_window
        self.task_panel = task_panel
        self.task = None

        self.next_task_nodes = []

        self.row = 0
        self.col = 0

        self.ui.button_add.clicked.connect(self.add_task_node)
        self.ui.button_delete.clicked.connect(self.delete_task_node)
        # self.ui.button_add.hide()
        # self.ui.button_delete.hide()
        



    def set_location(self, row, col):
        self.row = row
        self.col = col


    def add_task_node(self):
        menu = QMenu(self.task_panel.view)
        menu.triggered.connect(self.create_task)
        menu.setStyleSheet('background-color: rgb(0, 0, 0);color: rgb(255, 255, 255);')
        menu_cls = QMenu('图像分类', self.task_panel.view)
        for net_type in ['resnet_18', 'resnet_50']:
            action = QAction(net_type, menu_cls)
            action.setProperty('net_class', 'classification')
            action.setProperty('net_type', net_type)
            action.setProperty('pre_task', self.task.task_name)
            menu_cls.addAction(action)
        menu.addMenu(menu_cls)
        # menu_msg = QMenu('语义分割', self)  # 第1级
        # for net_class_name in ['低精度--高速', '中精度--中速']:  # 第2级
        #     action = QAction(net_class_name, menu_msg)
        #     action.setData(net_class_name)
        #     action.setObjectName('语义分割')
        #     menu_msg.addAction(action)
        # right_menu.addMenu(menu_msg)
        # menu_msg = QMenu('异常检测', self)
        # for task in ['异常分割']:
        #     menu_thr = QMenu(task, menu_msg)
        #     for net_class_name in ['中精度--中速']:  # 第2级
        #         action = QAction(net_class_name, menu_msg)
        #         action.setData(net_class_name)
        #         action.setObjectName('异常检测')
        #         menu_thr.addAction(action)
        #     menu_msg.addMenu(menu_thr)
        # right_menu.addMenu(menu_msg)
        menu.exec_(QCursor.pos())
    

    def create_task(self, action):
        net_class = action.property('net_class')
        net_type = action.property('net_type')
        pre_task_name = action.property('pre_task')


        if pre_task_name not in ['input']:
            pre_task = get_task(pre_task_name)
            if pre_task.net_class not in ['cytools'] and \
               len(get_task_category_name_list(pre_task, remove_unlabel=True)) == 0:
                msg = f'所选模型:  {pre_task_name}\n 没有创建任何标签，请创建后重试！'
                MessageBox(self.main_window, 'warning', '警告', msg, QMessageBox.Ok).run()
                return

        if net_class in ['cytools']:
            task_name = net_type
        else:
            task_name, ok = QInputDialog().getText(self.main_window, '当前任务名称', "请输入任务名称:", QLineEdit.Normal, "")
            if not ok: return
            if task_name == "":
                msg = f'任务名称不能为空！'
                MessageBox(self.main_window, 'warning', '警告', msg, QMessageBox.Ok).run()
                return

            if task_name in get_all_task_names():
                msg = f'任务名已经存在！'
                MessageBox(self.main_window, 'warning', '警告', msg, QMessageBox.Ok).run()
                return
        
        set_task_inactive()
        task = create_task(base_dir=BASE_DIR,
                           task_name=task_name, 
                           project_name=self.main_window.project_name, 
                           net_class=net_class, 
                           net_type=net_type, 
                           pre_task = pre_task_name)
        initiate_task_category(task)
        
        # 初始化ROI
        if net_type in ['ROI']:
            pass
            # create_roi(1, task_name, {'x': 0.0, 'y': 0.0, 'w': 1.0, 'h': 1.0})
        
        pre_tool = get_pre_tool(task)
        if pre_tool in ['ROI']:
            pass
            #  apply_rois_to_views(pre_task)
        
        task_dir = Path(BASE_DIR, 'projects', self.main_window.project_name, task_name)

        # 创建task目录
        task_dir = Path(BASE_DIR, 'projects', self.main_window.project_name, task_name)
        if net_class not in ['cytools']:
            task_dir.mkdir(exist_ok=True)
        if net_class in ['segmentation', 'anomaly']:
            Path(task_dir, 'annotation_images').mkdir(exist_ok=True)

        self.main_window.update_task(task)
        self.task_panel.build_tool_chain()


    def disconnect(self):
        self.menu.triggered.disconnect()
    

    def delete_task_node(self):
        pass


    # def set_selected(self, selected=False):
    #     if selected:
    #         self.setStyleSheet("background-color: rgb(200, 200, 200);")
    #     else:
    #         self.setStyleSheet("background-color: rgb(100, 100, 100);")

    # def mouseDoubleClickEvent(self, event):
    #     self.task_selected.emit(self.task_name)

    # def enterEvent(self, a0):
    #     self.ui.button_add.show()
    #     if self.task.task_name != 'ROI':
    #         self.ui.button_delete.show()
    #     super().enterEvent(a0)

    # def leaveEvent(self, a0):
    #     self.ui.button_add.hide()
    #     self.ui.button_delete.hide()
    #     super().leaveEvent(a0)
    
