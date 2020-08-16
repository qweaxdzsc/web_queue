from django.shortcuts import render, HttpResponse, redirect
from app_queue import models
from app_queue import utils
import json
# import threading
import os

field_dict = {
    0: None,
    1: 'order_id',
    2: 'account_email',
    3: 'mission_name',
    4: 'sender_address',
    5: 'register_time',
    6: 'start_time',
    7: 'used_time',
    8: 'id',
    9: 'mission_data',
}

list_obj = {
    'running_list': models.RunningList.objects,
    'waiting_list': models.WaitList.objects,
    'history_list': models.HistoryList.objects,
}


# Create your views here.
def index(request):
    user_name = request.session.get('user_name')
    is_login = False
    if user_name:
        is_login = True
        user_name = user_name.split('.')[0]
    parameters = {
        'error_info': '',
        'user_name': user_name,
        'is_login': is_login,
    }
    for list_name, obj in list_obj.items():
        parameters[list_name] = obj.all()
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


def fetch_tables(request):
    """
    used for ajax to request 3 tables data.
    1. get search condition, keyword, filter_current_user, user_name;
    2. check the keyword format;
    3. if correct, form filter dict, if not, return render with error_info
    4. if correct, use filter dict to filter data from database, return render
    :param request:
    :return: rendered index.html, error_info which hide in index.html
    if check ok, rendered index.html with 3 tables data
    if wrong, add error info
    """
    parameters = {
        'error_info': ''
    }
    list_fetched = []

    condition = int(request.GET.get('condition'))
    keyword = request.GET.get('keyword')
    filter_current_user = request.GET.get('current_user')
    user_name = request.session.get('user_name')

    if field_dict[condition]:
        filter_dict = {
            '%s__icontains' % field_dict[condition]: keyword
        }
    else:
        filter_dict, parameters['error_info'] = utils.check_keyword(keyword, field_dict)
    if parameters['error_info']:
        return render(request, 'index.html', parameters)
    if filter_current_user == 'true':
        account_email = user_name + '@estra-automotive.com'
        filter_dict['account_email'] = account_email
    print('filter_dict: ', filter_dict)
    for list_name, obj in list_obj.items():
        try:
            list_fetched = obj.filter(**filter_dict)
        except Exception as e:
            print(e)
            parameters['error_info'] = 'fetch data failed, please check search keyword'
            list_fetched = []
        parameters[list_name] = list_fetched

    return render(request, 'index.html', parameters)

# a = threading.Thread(target=utils.take_task, args=[models.WaitList, False])
# a.start()


