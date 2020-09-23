from django.shortcuts import render, HttpResponse, redirect
from django.views.decorators.csrf import csrf_exempt
from app_queue import models
from .. import views
import json


def help(request):
    help_doc = HelpDoc()
    help_doc.manual_create()
    parameter_dict = {'doc_list': help_doc.doc_list}
    return render(request, 'api_help.html', parameter_dict)


@csrf_exempt
def api_add(request):
    # print('1')
    add_project = views.AddProject()
    add_project.post(request)
    return HttpResponse('post success')


def api_history(request):
    account_email = request.GET.get('account_email')
    filter_dict = {
        'account_email': account_email
    }
    personal_history = models.HistoryList.objects.filter(**filter_dict)
    history_list = []
    for item in personal_history:
        data_dict = item.get_data_dict()
        try:
            data_dict['register_time'] = data_dict['register_time'].strftime('%Y-%m-%d %H:%I:%S')
            data_dict['start_time'] = data_dict['start_time'].strftime('%Y-%m-%d %H:%I:%S')
            data_dict['used_time'] = data_dict['used_time'].strftime('%Y-%m-%d %H:%I:%S')
        except Exception as e:
            pass
        history_list.append(data_dict)
    print(history_list)
    return HttpResponse(json.dumps(history_list, ensure_ascii=False))
    # return HttpResponse(personal_history)


def api_suspend(request):
    new_state = eval(request.GET.get('pause'))
    views.queue_pause[0] = new_state
    return HttpResponse(views.queue_pause[0])


class HelpDoc(object):
    def __init__(self):
        self.doc_list = list()

    def append(self, url, method, description_dict):
        new_dict = dict()
        new_dict['url'] = url
        new_dict['request_method'] = method
        new_dict['description'] = description_dict
        self.doc_list.append(new_dict)

    def manual_create(self):
        url = '/api/add'
        method = 'POST'
        description = {
            'select_main_app': '选择的主任务是，例如 "fluent191_solver"',
            'select_fluent191_solver': '选择的子任务，默认为无',
            'input_local_file': '需要输入的本地文件地址，例如journal文件地址 "G:/test/queue_test3/test.jou"',
            'user_name': '使用者用户名， 例如 "zonghui.jin"',
            'host_name': '本地计算机名， 例如 "DL5FWYWG2"',
            'local_ip': '本地计算机IP地址， 例如 "10.123.30.23"',
            'cpu_left': '本地计算机剩余cpu数量， 例如"12.33"',
        }
        self.append(url, method, description)
        url = '/api/account_history'
        method = 'GET'
        description = {
            'account_email': '填写用户完整邮箱名，例如 "zonghui.jin@estra-automotive.com"'
        }
        self.append(url, method, description)
        url = '/api/pause'
        method = 'GET'
        description = {
            'pause': '是否停止整个队列，填写布尔值，例如"True"'
        }
        self.append(url, method, description)

