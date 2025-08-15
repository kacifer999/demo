from main.db.dao.utils import *


def get_active_task():
    task = TaskModel.select().where(TaskModel.is_active == True).first() or TaskModel.select().first()
    if task is not None:
        task.is_active = True
        task.save()
    return task

def get_task_name_list():
    return list(TaskModel.select(TaskModel.task_name.distinct()).scalars())

def set_task_inactive():
    TaskModel.update(is_active=False).where(TaskModel.is_active == True).execute()


def change_next_tasks(task_name, prev_task_name, remove=False):
    prev_task = get_task(prev_task_name)
    if prev_task is None: return
    toolchain_config = prev_task.toolchain_config
    next_tasks = toolchain_config.get('next_tasks', list())
    if remove:
        if task_name in next_tasks:
            next_tasks.remove(task_name)
    else:
        if task_name not in next_tasks:
            next_tasks.append(task_name)

    toolchain_config['next_tasks'] = next_tasks
    prev_task.toolchain_config = toolchain_config
    prev_task.save()

def get_first_task():
    return next((task for task in TaskModel.select() if task.toolchain_config.get('prev_task') == 'input'), None)

# TODO
def delete_task_dbs(task):
    task.delete_instance()

















