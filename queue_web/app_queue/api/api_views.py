from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Count
from django.http import QueryDict
from app_queue import models
from .. import views, utils
import urllib.request
import urllib.parse
import json
import os
import time
import hashlib


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


@csrf_exempt
def api_test(request):
    print('some one try to connect and success')
    return HttpResponse('success')


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


def api_relaunch(request):
    running_missions = models.RunningList.objects.all()
    processed_list = []
    print('running missions:', running_missions)
    for mission in running_missions:
        data_dict = mission.get_data_dict()
        mission_data = eval(data_dict['mission_data'])
        data_string = urllib.parse.urlencode(mission_data)
        last_data = bytes(data_string, encoding='utf-8')
        response = urllib.request.urlopen("http://%s:37171/check_running" % data_dict['sender_address'], data=last_data)
        content = response.read().decode('utf-8')
        print('response from local', content)
        processed_list.append(data_dict['exec_app'])

    app_query = models.WaitList.objects.values('exec_app').annotate(app_count=Count('exec_app')).order_by()
    for i in processed_list:
        exclude_dict = {'exec_app': i}
        app_query = app_query.exclude(**exclude_dict)
    print('Those app queue prepare to launch', app_query)
    check = {'threads': views.threads[0]}
    for i in app_query:
        print('launch virtual mission for app: ', i['exec_app'])
        utils.virtual_mission(i['exec_app'], check, views.queue_pause)

    return HttpResponse('hello')


@csrf_exempt
def api_upload(request):
    if request.method == "POST":
        # 获取上传的文件，如果没有文件，则默认为None
        file_list = request.FILES.getlist("file_list", None)
        exec_file_name = request.POST.get('exec_file_name')
        user_name = request.POST.get('user_name')
        file_md5 = request.POST.getlist('file_md5')
        result_folder = request.POST.get('result_folder')
        # main_software = request.POST.get('main_software')
        # extend_software = request.POST.get('extend_software')
        print('file list:', file_list)
        print('exec file name: ', exec_file_name)
        print('user_name : ', user_name)
        print('file_md5 : ', file_md5)
        if not file_list:
            return HttpResponse("no files for upload!")
        # create folder for upload file
        upload_store_path = "G:\CFD_share\queue_calculation"
        time_mark = time.strftime("%m%d%H%M%S")
        folder_name = os.path.splitext(file_list[0].name)[0]
        folder = "%s\%s_%s" % (upload_store_path, folder_name, time_mark)  # make folder special
        if not os.path.exists(folder):
            os.makedirs(folder)
        # write file from upload list
        for file in file_list:
            file_path = os.path.join(folder, file.name)
            destination = open(file_path, 'wb+')  # 打开特定的文件进行二进制的写操作
            for chunk in file.chunks():  # 分块写入文件
                destination.write(chunk)
            destination.close()
            if not os.path.exists(file_path):
                return HttpResponse("file (%s) upload failed!" % file.name)
        # md5 verify file
        # make result folder
        if result_folder:
            result_folder_path = f"{folder}\{result_folder}"
            if not os.path.exists(result_folder_path):
                os.makedirs(result_folder_path)
        # form data dict to submit mission to queue
        main_software = "fluent191_solver"
        data_dict = {
            "select_main_app": main_software,
            "select_%s" % main_software: [],
            "input_local_file": folder + '\\' + exec_file_name,
            "user_name": user_name,
            "host_name": 'DL5FWYWG2',
            "local_ip": 'localhost',
            "total_cores": 28,
        }
        request_dict = QueryDict('', mutable=True)  # update request data
        request_dict.update(data_dict)
        request.POST = request_dict
        api_add(request)
        return HttpResponse("upload over, submit mission")
    # else:
    #     return HttpResponse('''
    #         <!doctype html>
    #         <title>Upload new File</title>
    #         <h1>Upload new File</h1>
    #         <form method=post enctype=multipart/form-data>
    #           <input type=file name=file_list multiple="">
    #           <input type=submit value=Upload>
    #         </form>
    #         ''')


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
