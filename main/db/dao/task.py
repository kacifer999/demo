from main.db.dao.utils import *

def get_active_task():
    task = Task.select().where(Task.is_active == True).first() or Task.select().first()
    if task is not None:
        task.is_active = True
        task.save()
    return task

def get_task_name_list():
    return list(Task.select(Task.task_name.distinct()).scalars())

def set_task_inactive():
    Task.update({Task.is_active: False,
                 Task.updated_at: datetime.datetime.now()}).where(
                 Task.is_active == True).execute()

def update_pre_task(task_name, old_pre_task_name=None, new_pre_task_name=None):
    if old_pre_task_name:
        change_next_tasks(task_name, old_pre_task_name, remove=True)

    if new_pre_task_name:
        change_next_tasks(task_name, new_pre_task_name)

def change_next_tasks(task_name, pre_task_name, remove=False):
    pre_task = get_task(pre_task_name)
    if pre_task is None: return
    toolchain_config = pre_task.toolchain_config
    next_tasks = toolchain_config.get('next_tasks', list())
    if remove:
        if task_name in next_tasks:
            next_tasks.remove(task_name)
    else:
        if task_name not in next_tasks:
            next_tasks.append(task_name)

    toolchain_config['next_tasks'] = next_tasks
    pre_task.toolchain_config = toolchain_config
    pre_task.save()

def get_first_task():
    return next((task for task in Task.select() if task.toolchain_config.get('pre_task') == 'input'), None)

def get_next_tasks(task):
    return task.toolchain_config.get('next_tasks', list())














