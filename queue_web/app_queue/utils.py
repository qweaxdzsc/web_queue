import time
from app_queue import models
from django.db.models import Min, Max


def max_order_id(db_model):
    order_id_dict = db_model.objects.aggregate(Max('order_id'))
    return order_id_dict['order_id__max']


def min_order_id(db_model):
    order_id_dict = db_model.objects.aggregate(Min('order_id'))
    return order_id_dict['order_id__min']


def new_order_id(db_model):
    order_id_dict = db_model.objects.aggregate(Max('order_id'))
    order_id = order_id_dict['order_id__max']
    if order_id:
        order_id += 1
    else:
        order_id = 1

    return order_id


def db_add_one(db_model, data_dict):
    user_obj = db_model(**data_dict)
    user_obj.save()


def get_first_mission(db_model):
    obj = db_model.objects.all().order_by("order_id").first()
    return obj


def db_to_running(obj):
    data_dict = obj.get_data_dict()
    data_dict.pop('id')
    data_dict.pop('order_id')
    db_add_one(models.RunningList, data_dict)
    obj.delete()


def take_task(db_wait, pause):
    while True:
        if not pause:
            first_obj = get_first_mission(db_wait)
            if first_obj:
                if able_to_run(first_obj):
                    db_to_running(first_obj)
                    run_task()
            else:
                print('empty')

        time.sleep(5)


def run_task():
    """
    1. send data and signal to tell local machine to run
    :return:
    """
    pass


def able_to_run(mission):
    """
    is it enough resources?
    :param mission:
    :return:
    """
    pass
    return bool()


