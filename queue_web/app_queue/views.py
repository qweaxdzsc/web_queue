from django.shortcuts import render, HttpResponse, redirect
from app_queue import models
from app_queue import utils
# import threading
import os


# Create your views here.
def index(request):
    user_name = request.session.get('user_name')
    is_login = False
    if user_name:
        is_login = True
        user_name = user_name.split('.')[0]
    condition = request.GET.get('condition')
    keyword = request.GET.get('keyword')
    print(request.get_full_path())
    filter_dict = {
        0: None,
        1: 'id',
        2: 'order_id',
        3: 'account_email',
        4: 'sender_address',
        5: 'mission_name',
        6: 'mission_data',
        7: 'register_time',
        8: 'start_time',
        9: 'used_time',
    }
    parameters = {
        'user_name': user_name,
        'is_login': is_login,
    }

    list_obj = {
        'running_list': models.RunningList.objects,
        'waiting_list': models.WaitList.objects,
        'history_list': models.HistoryList.objects,
    }
    for list_name, obj in list_obj.items():
        parameters[list_name] = obj.all()                    # TODO extract to a function or a class
    # email_check = models..objects.filter(email=account_email)
    # running_list = models.RunningList.objects.all()
    # waiting_list = models.WaitList.objects.all()
    # history_list = models.HistoryList.objects.all()

    return render(request, 'index.html', parameters)


def add_project(request):
    if request.method == 'POST':
        file_path = request.POST.get('input_local_file')
        iterations = request.POST.get('input_iter')
        project_address, file_name = os.path.split(file_path)
        project_name, extension = os.path.splitext(file_name)
        journal_path = '%s/%s.jou' % (project_address, project_name)
        print(file_path)
        print(iterations)
        order_id = utils.new_order_id(models.WaitList)
        mission_data = {
            'project_name': project_name,
            "project_address": project_address,
            "journal": journal_path,
        }
        data_dict = {'order_id': order_id,
                     'account_email': "zonghui.jin@estra-automotive.com",
                     'sender_address': '10.123.30.23',
                     'mission_name': project_name,
                     'mission_data': mission_data,
                     }
        utils.db_add_one(models.WaitList, data_dict)

        return redirect("/")


def get_local_file(request):
    print(request.GET.get('request'))
    org_data = 'none'
    response = HttpResponse(org_data)

    response["Access-Control-Allow-Origin"] = "*"
    # response["Access-Control-Allow-Methods"] = "POST,GET,OPTIONS"
    # response["Access-Control-Max-Age"] = "1000"
    # response["Access-Control-Allow-Headers"] = "*"
    return response


def receive_result(request):
    """
    listen to customer's local machine
    1. record the result
    2. move running mission from RunningList to HistoryList
    :param request:
    :return:
    """
    return HttpResponse('hello')


def test(request):
    condition_dict = {
        0: None,
        1: 'id',
        2: 'order_id',
        3: 'account_email',
        4: 'sender_address',
        5: 'mission_name',
        6: 'mission_data',
        7: 'register_time',
        8: 'start_time',
        9: 'used_time',
    }
    parameters = {
    }

    list_obj = {
        'running_list': models.RunningList.objects,
        'waiting_list': models.WaitList.objects,
        'history_list': models.HistoryList.objects,
    }
    condition = 7
    keyword = '8'
    filter_dict = {
        '%s__icontains' % condition_dict[condition]: keyword
    }
    # TODO solve multi filter request
    try:
        result = models.RunningList.objects.filter(**filter_dict)
    except Exception as e:
        result = []
    else:
        print(result)
    return HttpResponse(result)

# a = threading.Thread(target=utils.take_task, args=[models.WaitList, False])
# a.start()


