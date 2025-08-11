import uuid
from playhouse.apsw_ext import *
from main.db.model.base import *

def get_task(task_name):
    return TaskModel.select().where(TaskModel.task_name == task_name).first()




def bulk_create(_model, create_list):
    if len(create_list) > 0:
        _model.bulk_create(create_list, batch_size=500)
    reindex_id(_model)


def reindex_id(_model):
    update_list = list()
    model_items = _model.select().order_by(_model.id)
    for index, model_item in enumerate(model_items):
        new_id = index + 1
        if model_item.id == new_id: continue
        model_item.id = new_id
        update_list.append(model_item)
    if len(update_list) > 0:
        _model.bulk_update(update_list, fields=[_model.id], batch_size=500)

        
