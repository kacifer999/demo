import uuid
from playhouse.apsw_ext import *
from main.db.model.base import *

def get_task(task_name):
    return Task.select().where(Task.task_name == task_name).first()

