from django.shortcuts import render
from app_queue import models
from app_queue import utils
import threading


# Create your views here.
def index(request):
    mission = models.WaitList.objects.all()
    print('index:', mission)
    return render(request, 'index.html')


def add_project(request):
    order_id = utils.new_order_id(models.WaitList)
    data_dict = {'order_id': order_id,
                 'account_email': "zonghui.jin@estra-automotive.com",
                 'sender_address': '10.123.30.23',
                 'mission_name': 'test_demo',
                 'mission_data': "{‘project_address’：'/demo/demo_v1'}",
                 }
    utils.db_add_one(models.WaitList, data_dict)

    return render(request, 'add_project.html')


def view_history(request):
    return render(request, 'view_history.html')


def setting(request):
    pass
    return render(request, 'setting.html')


def receive_result(request):
    """
    listen to customer's local machine
    1. record the result
    2. move running mission from RunningList to HistoryList
    :param request:
    :return:
    """
    pass


a = threading.Thread(target=utils.take_task, args=[models.WaitList, ])
# a.start()


