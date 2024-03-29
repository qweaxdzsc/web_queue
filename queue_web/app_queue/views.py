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
# connect fields in database with sequence numbers
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

# three model objects, in order to loop them
list_obj = {
    'running_list': models.RunningList.objects,
    'waiting_list': models.WaitList.objects,
    'history_list': models.HistoryList.objects,
}

threads = [24, ]
queue_pause = [False, ]  # make sure it is changeable


# Create your views here.
# index page
def index(request):
    # get session to judge if logged in
    user_name = request.session.get('user_name')
    user_name_short = ''
    user_auth = request.session.get('authorization')
    is_login = False
    if user_name:
        print('user %s already logged in' % user_name)
        is_login = True
        user_name_short = user_name.split('.')[0]
    # get every exec app and their own extend process
    main_apps = os.listdir('server_app')
    extend_apps_dict = {}
    for i, app in enumerate(main_apps):
        extend_apps_list = []
        file_list = os.listdir('server_app/%s' % app)
        # get extend app
        for file in file_list:
            if file.startswith('extend_'):
                app_name = file.replace('extend_', '')
                extend_apps_list.append(app_name)
        extend_apps_dict[app] = extend_apps_list
    # prepare parameters for index page
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
    # get all 3 data sheets, but no more than 20 items each
    for list_name, obj in list_obj.items():
        missions = obj.all()
        mission_number = missions.count()
        if mission_number > 20:
            missions = missions[:21]
        parameters[list_name] = missions

    return render(request, 'index.html', parameters)


class AddProject(View):
    """
    CBV, POST method, used to process request to add project to queue.
    Precede as follow:
    1. get all necessary parameters
    2. based on given parameters, form mission data which used to do project
    3. determine whether able to exec mission immediately, if not save to waiting queue
    """
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
        print('main_app', self.main_app)
        print('extend_app', self.extend_app)
        print('file_path', self.file_path)
        print('user_name', self.user_name)
        print('host_name', self.host_name)
        print('local_ip', self.local_ip)
        print('total_cores', self.total_cores)
        print('account_email', self.account_email)
        # determine the order in queue
        self.order_id = utils.new_order_id(models.WaitList, self.main_app)
        self.mission_data, error = self.form_mission_data()
        if error:
            return HttpResponse('exec %s error, please check %s under server_app' % self.main_app)
        # prepare data dict to register into database
        data_dict = {
            'order_id': self.order_id,
            'account_email': self.account_email,
            'exec_app': self.main_app,
            'sender_address': self.local_ip,
            'mission_name': self.project_name,
            'mission_data': self.mission_data,
        }
        if self.exec_available():
            # exec directly
            data_dict['register_time'] = datetime.datetime.utcnow().replace(tzinfo=utc)  # record register time, UTC now
            utils.exec_mission(data_dict)
        else:
            # add to waiting queue db
            self.add_to_queue(data_dict)

        return redirect('/')

    def form_mission_data(self):
        # prepare parameters
        error = False                                               # TODO ? maybe no need
        project_address, file_name = os.path.split(self.file_path)          # split address and file
        self.project_name, extension = os.path.splitext(file_name)          # split file name and extension name
        use_mpi, mpi_host = utils.thread_strategy(threads[0], self.host_name, self.total_cores)
        # form main data dict
        main_task = {
            "software": self.main_app,
            'project_name': self.project_name,
            "project_address": project_address,
            'extension': extension,
            'host_name': self.host_name,
            "order_id": self.order_id,
            'threads': threads[0],
            "use_mpi": use_mpi,
            "mpi_host": mpi_host,
        }
        self.mission_data[0] = main_task            # do main task first
        # Then do extend task, also use dict format
        for i, app in enumerate(self.extend_app):
            # maybe none
            if app:
                extend_task = {
                    "software": app,
                    'project_name': self.project_name,
                    "project_address": project_address,
                    'extension': extension,
                    'host_name': self.host_name,
                    "order_id": self.order_id,
                    'threads': threads[0],
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
        # under same app queue, no mission in running
        filter_dict = {'exec_app': self.main_app}
        running_mission = models.RunningList.objects.filter(**filter_dict)
        if running_mission:
            return False
        # check if runnable, controlled by app, usually check license usage
        check = {'threads': threads[0]}
        runnable = utils.app_prerequisite(check, self.main_app)
        # if not runnable or being purposely paused
        if (not runnable) or queue_pause[0]:
            utils.virtual_mission(self.main_app, check, queue_pause)
            return False
        # TODO should check cpu cores left
        return True

    def add_to_queue(self, data_dict):
        # add mission to wait list database
        utils.db_add_one(models.WaitList, data_dict)


def get_local_file(request):
    # TODO ? what is this used for
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
    listen to customer's local machine, POST method
    1. record the result
    2. move mission from RunningList to HistoryList
    :param request:
    :return:
    """
    if request.method == 'POST':
        main_app = request.POST.get('software')
        order_id = request.POST.get('order_id')

        # search for which mission is finished by order_id and exec_app
        filter_dict = {
            'exec_app': main_app,
            'order_id': order_id,
        }
        finished_mission = models.RunningList.objects.filter(**filter_dict).first()
        print('The finished mission is: ', finished_mission)
        # ----form data dict-----
        data_dict = finished_mission.get_data_dict()
        # record mission status
        mission_data_dict = eval(data_dict["mission_data"])
        for key in request.POST:
            if "mission_status" in key:
                mission_data_dict[key] = request.POST.get(key)
        data_dict["mission_data"] = str(mission_data_dict)
        # calculate used time
        now_time = datetime.datetime.utcnow().replace(tzinfo=utc)
        used_time_sec = (now_time - data_dict['start_time']).seconds
        hours, minutes = divmod(used_time_sec / 60, 60)
        used_time_str = '%.0f小时%.0f分钟' % (hours, minutes)
        data_dict['used_time'] = used_time_str
        data_dict.pop('id')
        # add to history
        user_obj = models.HistoryList(**data_dict)
        user_obj.save()
        # delete item in running list
        finished_mission.delete()
        # next mission, with pre check first
        check = {'threads': threads[0]}
        available = utils.app_prerequisite(check, main_app)
        if available:
            utils.next_mission(main_app, check, queue_pause)
        else:
            utils.virtual_mission(main_app, check, queue_pause)

    return HttpResponse('django server received result')


def fetch_tables(request):
    """
    used for ajax to request 3 tables data.
    1. get search condition, keyword, if_current_user, user_name;
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
    # get parameters
    condition = int(request.GET.get('condition'))
    keyword = request.GET.get('keyword')
    filter_current_user = request.GET.get('current_user')
    user_name = request.session.get('user_name')
    # form filter dict
    if field_dict[condition]:
        filter_dict = {
            '%s__icontains' % field_dict[condition]: keyword
        }
    else:
        filter_dict, parameters['error_info'] = utils.check_keyword(keyword, field_dict)

    if parameters['error_info']:
        # if have error
        return render(request, 'index.html', parameters)
    # add another condition, filter by current user
    if filter_current_user == 'true':
        account_email = user_name + '@estra-automotive.com'
        filter_dict['account_email'] = account_email
    print('filter_dict: ', filter_dict)
    # try to filter the result, and return it in list_fetched
    for list_name, obj in list_obj.items():
        try:
            list_fetched = obj.filter(**filter_dict)
            mission_number = list_fetched.count()             # no more than 20 items each table
            if mission_number > 20:
                list_fetched = list_fetched[:21]
        except Exception as e:
            print(e)
            parameters['error_info'] = 'fetch data failed, please check search keyword'
            list_fetched = []
        parameters[list_name] = list_fetched

    return render(request, 'index.html', parameters)


def get_csrf(request):
    """
    used for bypass the csrf verification
    :param request:
    :return:
    """
    csrf_token = str(csrf(request)['csrf_token'])
    csrf_request_form = {
        'header': {'Cookie': 'csrftoken=%s' % csrf_token},
        'data': {'csrfmiddlewaretoken': csrf_token},
    }
    return HttpResponse(json.dumps(csrf_request_form))


def pause_queue(request):
    """
    determine if suspend queue, connected with button in website
    :param request:
    :return:
    """
    state = int(request.GET.get('pause'))
    global queue_pause
    queue_pause[0] = bool(1 - state)

    return HttpResponse(state)


def queue_reorder(request):
    """
    used to reorder the queue, in case some mission has to jump the queue.
    paired with /reorder/ site
    :param request:
    :return:
    """
    parameters = {
        'error_info': '',
        'queue_pause': queue_pause[0],
    }
    app = {'exec_app': 'fluent191_solver'}                              # default app
    if request.method == "POST":
        drag_index = int(request.POST.get('drag_rowIndex')) - 1         # the index of item being dragged
        target_index = int(request.POST.get('target_rowIndex')) - 1     # the index of place being dropped
        select_app = request.POST.get('select_app')                     # selected item's app
        print(f'drag_index:{drag_index}, target_index:{target_index}, select_app:{select_app}')
        if drag_index == target_index:
            # if drag to same place
            pass
        else:
            # order the list of missions by select app
            filter_dict = {'exec_app': select_app}
            missions = models.WaitList.objects.all().filter(**filter_dict).order_by("order_id")
            order_id_list = list(missions.values('order_id'))
            drag_mission = missions[drag_index]
            drag_mission.order_id = order_id_list[target_index]['order_id']     # change drag mission's order id
            # change effected missions id, 2 situations
            if drag_index > target_index:
                # define effected range
                mission_range = missions[target_index: drag_index]
                order_id_range = order_id_list[target_index: drag_index]

                for Index, mission in enumerate(mission_range):
                    # all affected mission order id + 1
                    mission.order_id = order_id_range[Index]['order_id'] + 1
                    mission.save()
            else:
                # define effected range
                mission_range = missions[drag_index + 1: target_index + 1]
                order_id_range = order_id_list[drag_index + 1: target_index + 1]

                for Index, mission in enumerate(mission_range):
                    # all affected mission order id - 1
                    mission.order_id = order_id_range[Index]['order_id'] - 1
                    mission.save()
            # save at last because it will not effect ORM fetch at first
            drag_mission.save()
    else:
        # only the manager have the authorization to change order
        user_auth = request.session.get('authorization')
        if user_auth != 'manager':
            return HttpResponse('no authorize')
        search_app = request.GET.get('select_app')
        if search_app:
            app['exec_app'] = search_app
    missions = models.WaitList.objects.all().order_by("order_id")
    # add order_by() because modal have default order_by, sql require order by if use annotate method
    # show list
    app_query = models.WaitList.objects.values('exec_app').annotate(app_count=Count('exec_app')).order_by()
    parameters['app_list'] = [i['exec_app'] for i in app_query]
    parameters['waiting_list'] = missions.filter(**app)
    parameters['choose_app'] = app['exec_app']

    return render(request, 'queue_reorder.html', parameters)


def delete_mission(request):
    if request.method == 'POST':
        app = request.POST.get('exec_app')
        print(app)
        order_id = request.POST.get('order_id')
        print(order_id)
        filter_dict = {
            'exec_app': app,
            'order_id': order_id,
        }
        obj = models.WaitList.objects.filter(**filter_dict).first()
        print(obj)
        obj.delete()
    return HttpResponse('hello')


def test(request):
    pass
    # if request.method == 'POST':
    #     app = request.POST.get('exec_app')
    #     print(app)
    #     order_id = request.POST.get('order_id')
    #     print(order_id)
    #     filter_dict = {
    #         'exec_app': app,
    #         'order_id': order_id,
    #     }
    #     obj = models.WaitList.objects.filter(**filter_dict).first()
    #     print(obj)
    #     obj.delete()
    return HttpResponse('hello')


@csrf_exempt
def test_post(request):
    print('request')
    if request.method == 'POST':
        print(request.POST)
    return HttpResponse('test post')