import datetime
from turtle import width
from peewee import *
from playhouse.sqlite_ext import JSONField

DB_PROXY = DatabaseProxy()

class BaseModel(Model):
    uuid = CharField()

    class Meta:
        database = DB_PROXY


class TaskModel(BaseModel):
    task_name = CharField()
    task_type = CharField()
    project_dir = CharField()
    task_dir = CharField()
    is_active = BooleanField(default=False)
    model_type = CharField()
    model_config = TextField(default='')
    train_time = CharField(default='')
    mask_config = JSONField(default={})
    task_config = JSONField(default={})
    filter_config = JSONField(default={})
    toolchain_config = JSONField(default={})


class ImageModel(BaseModel):
    image_name = CharField()
    width = IntegerField()
    height = IntegerField()


class ViewModel(BaseModel):
    view_name = CharField()
    view_id = IntegerField()
    prev_task = CharField()
    xywha = JSONField()











