from django.shortcuts import render
from app_queue import models
from app_queue import utils
import threading


# Create your views here.
def index(request):
    running_list = models.RunningList.objects.all()
    waiting_list = models.WaitList.objects.all()
    history_list = models.HistoryList.objects.all()
    parameters = {
        'running_list': running_list,
        'waiting_list': waiting_list,
        'history_list': history_list,
    }
    return render(request, 'index.html', parameters)


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


def receive_result(request):
    """
    listen to customer's local machine
    1. record the result
    2. move running mission from RunningList to HistoryList
    :param request:
    :return:
    """
    pass


a = threading.Thread(target=utils.take_task, args=[models.WaitList, False])
# a.start()


