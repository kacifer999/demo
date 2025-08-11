import traceback
from PIL import Image
from pathlib import Path

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from main.settings.path import BASE_DIR

from main.db.dao.service import *


class LoadImagesThread(QThread):
    one_finished = pyqtSignal(int, int)
    thread_finished = pyqtSignal()

    def __init__(self, task, image_dir_list):
        super().__init__()
        self.task = task
        self.image_dir_list = image_dir_list
        self.project_db = None

    def run(self):
        try:
            create_image_list = list()
            create_view_list = list()
            self.project_db = connect_db(Path(self.task.project_dir, 'project.db').as_posix())
            current_image_list = get_image_name_list()
            total = len(self.image_dir_list)
            save_dir = Path(self.task.project_dir, 'images')
            save_dir.mkdir(parents=True, exist_ok=True)
            for index, image_file_dir in enumerate(self.image_dir_list):
                image_name = Path(image_file_dir).stem
                if image_name in current_image_list: continue
                image = Image.open(image_file_dir)
                width, height = image.size
                image.save(Path(save_dir, f'{image_name}.png'))
                create_image_list.append(ImageModel(uuid=str(uuid.uuid1()),
                                                    image_name=image_name,
                                                    width=width,
                                                    height=height))
                
                create_view_list.append(ViewModel(uuid=str(uuid.uuid1()),
                                                  view_name=f'{image_name}_0',
                                                  view_id=0,
                                                  image_name=image_name,
                                                  prev_task='input',
                                                  xywha=dict(x=0, y=0, w=1, h=1, a=0)))
                
                self.one_finished.emit(index, total)

            if len(create_image_list) > 0:
                bulk_create(ImageModel, create_image_list)
            if len(create_view_list) > 0:
                bulk_create(ViewModel, create_view_list)
            
            close_db(self.project_db)
            self.project_db = None
            self.thread_finished.emit()
        except:
            if self.project_db is not None:
                close_db(self.project_db)
                self.project_db = None

            self.thread_finished.emit()
            traceback.print_exc()
            self.quit()
