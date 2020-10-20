from django.shortcuts import render, HttpResponse, redirect
from django.views import View
from django.template.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Count
from django.utils.timezone import utc

from app_queue import models
from app_queue import utils
import datetime
import json
import os

# import datetime
# import urllib.request
# import urllib.parse

# --------global variable--------
field_dict = {
    0: None,
    1: 'order_id',
    2: 'account_email',
    3: 'mission_name',
    4: 'exec_app',
    5: 'register_time',
    6: 'start_time',
    7: 'used_time',
    8: 'id',
    9: 'mission_data',
    10: 'sender_address',
}

list_obj = {
    'running_list': models.RunningList.objects,
    'waiting_list': models.WaitList.objects,
    'history_list': models.HistoryList.objects,
}

threads = 4
queue_pause = [False, ]  # make sure it is changeable


# Create your views here.
def index(request):
    user_name = request.session.get('user_name')
    user_name_short = ''
    user_auth = request.session.get('authorization')
    is_login = False
    if user_name:
        is_login = True
        user_name_short = user_name.split('.')[0]

    main_apps = os.listdir('server_app')
    extend_apps_dict = {}
    for i, app in enumerate(main_apps):
        extend_apps_list = []
        file_list = os.listdir('server_app/%s' % app)
        for file in file_list:
            if file.startswith('extend_'):
                app_name = file.replace('extend_', '')
                extend_apps_list.append(app_name)
        extend_apps_dict[app] = extend_apps_list

    parameters = {
        'error_info': '',
        'user_name_short': user_name_short,
        'user_name': user_name,
        'user_auth': user_auth,
        'is_login': is_login,
        'queue_pause': queue_pause[0],
        'main_apps': main_apps,
        'extend_apps_dict': extend_apps_dict,
    }
    for list_name, obj in list_obj.items():
        missions = obj.all()
        mission_number = missions.count()
        if mission_number > 20:
            missions = missions[:21]
        parameters[list_name] = missions

    return render(request, 'index.html', parameters)


class AddProject(View):
    main_app = str()
    extend_app = list()
    file_path = str()
    user_name = str()
    host_name = str()
    local_ip = str()
    total_cores = int()
    account_email = str()
    project_name = str()
    mission_data = dict()
    order_id = int()

    def get(self, request):
        return HttpResponse('do not access by GET')

    def post(self, request):
        # get account email
        print("new mission submit")
        self.main_app = request.POST.get('select_main_app')
        self.extend_app = request.POST.getlist('select_%s' % self.main_app)
        self.file_path = request.POST.get('input_local_file')
        self.user_name = request.POST.get('user_name')
        self.host_name = request.POST.get('host_name')
        self.local_ip = request.POST.get('local_ip')
        self.total_cores = request.POST.get('total_cores')
        self.account_email = self.user_name + '@estra-automotive.com'

        self.order_id = utils.new_order_id(models.WaitList, self.main_app)
        self.mission_data, error = self.form_mission_data()
        if error:
            return HttpResponse('exec %s error, please check %s under server_app' % self.main_app)
        data_dict = {
            'order_id': self.order_id,
            'account_email': self.account_email,
            'exec_app': self.main_app,
            'sender_address': self.local_ip,
            'mission_name': self.project_name,
            'mission_data': self.mission_data,
        }
        if self.exec_available():
            data_dict['register_time'] = datetime.datetime.utcnow().replace(tzinfo=utc)
            utils.exec_mission(data_dict)
        else:
            self.add_to_queue(data_dict)

        return redirect('/')

    def form_mission_data(self):
        error = False
        project_address, file_name = os.path.split(self.file_path)
        self.project_name, extension = os.path.splitext(file_name)
        use_mpi, mpi_host = utils.thread_strategy(threads, self.host_name, self.total_cores)

        main_task = {
            "software": self.main_app,
            'project_name': self.project_name,
            "project_address": project_address,
            'extension': extension,
            'host_name': self.host_name,
            "order_id": self.order_id,
            'threads': threads,
            "use_mpi": use_mpi,
            "mpi_host": mpi_host,
        }
        self.mission_data[0] = main_task
        for i, app in enumerate(self.extend_app):
            if app:
                extend_task = {
                    "software": app,
                    'project_name': self.project_name,
                    "project_address": project_address,
                    'extension': extension,
                    'host_name': self.host_name,
                    "order_id": self.order_id,
                    'threads': threads,
                    "use_mpi": use_mpi,
                    "mpi_host": mpi_host,
                }
                self.mission_data[i + 1] = extend_task

        return self.mission_data, error

    def exec_available(self):
        """
        等待队列有无，有（取order_id最大值加1），
        无，判断有无正在计算的，有（取order_id为1），
        无，判断有无license和核数，有（发送信号计算，有响应则进入正在计算队列，无则），造一个虚拟定时任务
        :return:
        """
        # waiting list have none in front
        if self.order_id > 1:
            return False
        filter_dict = {'exec_app': self.main_app}
        running_mission = models.RunningList.objects.filter(**filter_dict)
        if running_mission:
            return False
        # check if runnable, written in app, usually check license usage
        check = {'threads': threads}
        runnable = utils.app_prerequisite(check, self.main_app)
        if (not runnable) or queue_pause[0]:
            utils.virtual_mission(self.main_app, check, queue_pause)
            return False
        # TODO should check cpu cores left
        return True

    def add_to_queue(self, data_dict):
        utils.db_add_one(models.WaitList, data_dict)


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
    if request.method == 'POST':
        main_app = request.POST.get('software')
        order_id = request.POST.get('order_id')
        mission_status = request.POST.get('0_mission_status')  # get all mission status, save to mission data
        filter_dict = {
            'exec_app': main_app,
            'order_id': order_id,
        }
        finished_mission = models.RunningList.objects.filter(**filter_dict).first()
        print(finished_mission)
        data_dict = finished_mission.get_data_dict()
        now_time = datetime.datetime.utcnow().replace(tzinfo=utc)
        used_time_sec = (now_time - data_dict['start_time']).seconds
        hours, minutes = divmod(used_time_sec / 60, 60)
        used_time_str = f'{hours}小时{minutes}分钟'
        data_dict['used_time'] = used_time_str
        data_dict.pop('id')
        # add to history
        user_obj = models.HistoryList(**data_dict)
        user_obj.save()
        # delete self
        finished_mission.delete()
        # next mission
        check = {'threads': threads}
        available = utils.app_prerequisite(check, main_app)
        if available:
            utils.next_mission(main_app, check, queue_pause)
        else:
            utils.virtual_mission(main_app, check, queue_pause)

    return HttpResponse('django server received result')


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
            mission_number = list_fetched.count()
            if mission_number > 20:
                list_fetched = list_fetched[:21]
        except Exception as e:
            print(e)
            parameters['error_info'] = 'fetch data failed, please check search keyword'
            list_fetched = []
        parameters[list_name] = list_fetched

    return render(request, 'index.html', parameters)


def get_csrf(request):
    csrf_token = str(csrf(request)['csrf_token'])
    csrf_request_form = {
        'header': {'Cookie': 'csrftoken=%s' % csrf_token},
        'data': {'csrfmiddlewaretoken': csrf_token},
    }
    return HttpResponse(json.dumps(csrf_request_form))


def pause_queue(request):
    state = int(request.GET.get('pause'))
    global queue_pause
    queue_pause[0] = bool(1 - state)

    return HttpResponse(state)


def queue_reorder(request):
    parameters = {
        'error_info': '',
        'queue_pause': queue_pause[0],
    }
    app = {'exec_app': 'fluent191_solver'}
    if request.method == "POST":
        drag_index = int(request.POST.get('drag_rowIndex')) - 1
        target_index = int(request.POST.get('target_rowIndex')) - 1
        select_app = request.POST.get('select_app')
        print(f'drag_index:{drag_index}, target_index:{target_index}, select_app:{select_app}')
        if drag_index == target_index:
            pass
        else:
            filter_dict = {'exec_app': select_app}
            missions = models.WaitList.objects.all().filter(**filter_dict).order_by("order_id")
            order_id_list = list(missions.values('order_id'))
            drag_mission = missions[drag_index]
            drag_mission.order_id = order_id_list[target_index]['order_id']

            if drag_index > target_index:
                mission_range = missions[target_index: drag_index]
                order_id_range = order_id_list[target_index: drag_index]

                for Index, mission in enumerate(mission_range):
                    mission.order_id = order_id_range[Index]['order_id'] + 1
                    mission.save()
            else:
                mission_range = missions[drag_index + 1: target_index + 1]
                order_id_range = order_id_list[drag_index + 1: target_index + 1]

                for Index, mission in enumerate(mission_range):
                    mission.order_id = order_id_range[Index]['order_id'] - 1
                    mission.save()
            # save at last because it will not effect ORM get
            drag_mission.save()
    else:
        user_auth = request.session.get('authorization')
        if user_auth != 'manager':
            return HttpResponse('no authorize')
        search_app = request.GET.get('select_app')
        if search_app:
            app['exec_app'] = search_app
    missions = models.WaitList.objects.all().order_by("order_id")
    # add order_by() because modal have default order_by, sql require order by if use annotate method
    app_query = models.WaitList.objects.values('exec_app').annotate(app_count=Count('exec_app')).order_by()
    parameters['app_list'] = [i['exec_app'] for i in app_query]
    parameters['waiting_list'] = missions.filter(**app)
    parameters['choose_app'] = app['exec_app']

    return render(request, 'queue_reorder.html', parameters)


def test(request):
    app_query = models.WaitList.objects.values('exec_app').annotate(app_count=Count('exec_app')).order_by()
    processed_list = ['fluent191_solver', 'fluent191_mesh']
    for i in processed_list:
        exclude_dict = {'exec_app': i}
        app_query = app_query.exclude(**exclude_dict)
    print(app_query)
    check = {'threads': threads}
    for i in app_query:
        utils.virtual_mission(i['exec_app'], check, queue_pause)
    return HttpResponse('hello')


@csrf_exempt
def test_post(request):
    print('request')
    if request.method == 'POST':
        print(request.POST)
    return HttpResponse('test post')