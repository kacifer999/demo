import datetime
from peewee import *
from playhouse.sqlite_ext import JSONField

DB_PROXY = DatabaseProxy()

class BaseModel(Model):
    uuid = CharField()
    updated_at = DateTimeField(default=datetime.datetime.now)
    class Meta:
        database = DB_PROXY

class Task(BaseModel):
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
    
    







