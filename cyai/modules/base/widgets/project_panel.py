# python packages
import json
import logging
import shutil
import time
from pathlib import Path
import types

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

from cyai.settings.path import *
from cyai.modules.base.service.project_config import ProjectsConfig
from cyai.modules.base.widgets.messagge_box import MessageBox
# self packages
# from cyai.modules.base.ui.project_set import Ui_ProjectSetDialog
# from cyai.settings.paths import BASE_DIR, THEME_DIR
# from cyai.modules.base.service.logger import get_root_logger
# from cyai.modules.base.service.misc import message_box
# from cyai.modules.base.service.projects import Projects
# from cyai.modules.base.service.migration import Migration
# from cyai.modules.base.service.sdk_utils import export_sdk
# from cyai.modules.base.service.thread_import_project import ImportProjectThread
# from cyai.modules.base.service.thread_export_project import ExportProjectThread



# 工程设置及管理类
class ProjectPanel(ProjectsConfig):
    def __init__(self, main_window=None):
        self.main_window = main_window
        self.project_panel = main_window.list_project_panel
        self.project_panel.mousePressEvent = types.MethodType(self.mouse_press_event, self.project_panel)
        self.load_projects_config()
        self.load_projects()

        self.project_panel.itemClicked.connect(self.switch_project)
        self.project_panel.customContextMenuRequested.connect(self.create_menu)
    

    def load_projects(self):
        self.project_panel.clear()
        for project in self.projects:
            item = self.add_widget_item(project.name)
            if project.status == "active":
                self.project_panel.setCurrentItem(item)
                self.main_window.build_project(project.name)



    def show_project_panel(self):
        if self.main_window.action_project_panel.isChecked():
            self.main_window.ui_project_panel.show()
        else:
            self.main_window.ui_project_panel.hide()

    

    def create_menu(self):
        item = self.project_panel.currentItem()
        right_menu = QMenu(self.project_panel)
        right_menu.setStyleSheet('background-color: rgb(0, 0, 0);color: rgb(255, 255, 255);')
        action_create = QAction("创建", self.project_panel)
        action_create.triggered.connect(self.create_project)
        action_delete = QAction("删除", self.project_panel)
        action_delete.triggered.connect(self.delete_project)
        action_import = QAction("导入", self.project_panel)
        # action_import.triggered.connect(self.import_project)
        if item is None:
            right_menu.addAction(action_create)
            # right_menu.addAction(action_import)
        else:
            right_menu.addAction(action_create)
            right_menu.addAction(action_delete)
            right_menu.addSeparator()

        right_menu.exec_(QCursor.pos())


    def switch_project(self):
        item = self.project_panel.currentItem()
        project_name = item.text()
        if item is None: return
        if self.main_window.project_name == project_name: return
        self.switch(project_name)
        self.main_window.build_project(project_name)


    def create_project(self):
        input_dialog = QInputDialog(self.main_window)
        project_name, ok = input_dialog.getText(self.main_window, "输入对话框", "请输入工程名称:", QLineEdit.Normal, "")
        if not ok: return
        if project_name == "":
            msg = '工程名称不能为空！'
            MessageBox(self.main_window, 'information', '提示', msg, QMessageBox.Ok).run()
            return
        
        if project_name in self.get_project_name_list():
            msg = '工程名已经存在，不能新建！'
            MessageBox(self.main_window, 'information', '提示', msg, QMessageBox.Ok).run()
            return
        
        self.create(project_name)
        db_dir = Path(BASE_DIR,'projects', project_name,'project.db')
        db_dir.parent.mkdir(parents=True, exist_ok=True)
        self.main_window.project_db = connect_db(db_dir.as_posix(), self.main_window.project_db)
        create_db_tables(self.main_window.project_db)
        init_data_set_type()
        self.main_window.build_project(project_name, True)
        item = self.add_widget_item(project_name)
        self.project_panel.setCurrentItem(item)

    
    
    def delete_project(self):
        item = self.project_panel.currentItem()
        self.project_panel.takeItem(self.project_panel.row(item))
        self.main_window.project_db = close_dbs(self.main_window.project_db)
        self.delete(item.text())
        shutil.rmtree(Path(BASE_DIR, 'projects', item.text()), ignore_errors=True)
        self.project_panel.setCurrentItem(None)
        # project_name = self.get_active()
        # if len(self.projects) > 0:
        #     for index in range(self.project_panel.count()):
        #         item = self.project_panel.item(index)
        #         if item.text() == project_name:
        #             self.project_panel.setCurrentItem(item)
        self.main_window.build_project(None)


    def add_widget_item(self, project_name):
        item = QListWidgetItem()
        item.setText(project_name)
        item_width = self.project_panel.geometry().width() - 10
        item_height = (self.project_panel.geometry().height() - 10)// 15
        item.setSizeHint(QSize(item_width, item_height))
        item.setIcon(QIcon(Path(ICONS_DIR, 'folder.png').as_posix()))
        self.project_panel.addItem(item)
        return item


    
    def get_project_name_list(self):
        return [project.name for project in self.projects]
    

    def mouse_press_event(self, project_panel, event):
        index = project_panel.indexAt(event.pos())
        if index.isValid():
            QListWidget.mousePressEvent(project_panel, event)
        else:
            project_panel.setCurrentItem(None)