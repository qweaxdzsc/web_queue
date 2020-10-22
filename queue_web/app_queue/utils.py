from app_queue import models
from django.db.models import Min, Max, Count

import csv
import threading


import urllib.request
import urllib.parse


def max_order_id(db_model):
    order_id_dict = db_model.objects.aggregate(Max('order_id'))
    return order_id_dict['order_id__max']


def min_order_id(db_model):
    order_id_dict = db_model.objects.aggregate(Min('order_id'))
    return order_id_dict['order_id__min']


def new_order_id(db_model, main_app):
    # based on exec app, determine the order id. Each app have their own queue.
    filter_dict = {'exec_app': main_app}
    order_id_dict = db_model.objects.filter(**filter_dict).aggregate(Max('order_id'))  # find the max number
    order_id = order_id_dict['order_id__max']
    if order_id:
        order_id += 1
    else:
        order_id = 1

    return order_id


def db_add_one(db_model, data_dict):
    user_obj = db_model(**data_dict)
    user_obj.save()


def get_first_mission(db_model, exec_app):
    filter_dict = {'exec_app': exec_app}
    obj = db_model.objects.filter(**filter_dict).order_by("order_id").first()
    return obj


def db_to_running(obj):
    data_dict = obj.get_data_dict()
    db_add_one(models.RunningList, data_dict)
    obj.delete()


def next_mission(main_app, check_dict, queue_pause, need_check=False):
    """
    do next mission, but check if doable first
    :param main_app:
    :param check_dict:
    :param queue_pause:
    :param need_check:
    :return:
    """
    print('bring next mission')
    mission = get_first_mission(models.WaitList, main_app)
    # if mission exist
    if mission:
        data_dict = mission.get_data_dict()                          # get data dict from mission
        data_dict['mission_data'] = eval(data_dict['mission_data'])  # convert str from database to dict
        if not queue_pause[0]:
            if need_check:
                available = app_prerequisite(check_dict, main_app)
                # if pass check, do it. Otherwise, create another virtual mission
                if available:
                    exec_mission(data_dict)
                    print('perform delete')
                    mission.delete()
                    print('exec_mission')
                else:
                    virtual_mission(main_app, check_dict, queue_pause)
            else:
                exec_mission(data_dict)
                mission.delete()
                print('exec_mission')
        else:
            virtual_mission(main_app, check_dict, queue_pause)


def exec_mission(data_dict):
    # send mission to local to run
    print('exec mission')
    data_string = urllib.parse.urlencode(data_dict['mission_data'])  # stringify data dict
    last_data = bytes(data_string, encoding='utf-8')                 # form bytes like
    response = urllib.request.urlopen("http://%s:37171/get_task" % data_dict['sender_address'], data=last_data)
    content = response.read().decode('utf-8')  # parse response
    print('response from local', content)
    # add to running list
    db_add_one(models.RunningList, data_dict)


def virtual_mission(main_app, check_dict, queue_pause):
    """
    When no mission in front, but without license, it need an auto check afterwards.
    create virtual mission to call next after short certain time.
    :return:
    """
    print('create virtual mission')
    timer = threading.Timer(10, next_mission, args=(main_app, check_dict, queue_pause, True,))
    timer.start()


def app_prerequisite(check_dict, main_app):
    """
    usually check the license sufficiency
    :param check_dict:
    :param main_app:
    :return:
    """
    try:
        exec(open(r'./server_app/%s/prerequisite.py' % main_app, 'r').read(), check_dict)
        print('have license: ', check_dict['runnable'])
    except Exception as e:
        return False
    else:
        if not check_dict['runnable']:
            return False
    return True


def key_exist(string_key, condition_dict):
    """
    check if the key is in condition_dict
    :param string_key: string format key extract from keyword
    :param condition_dict: the number key relation with field name
    :return:
    if exist: the corresponding field name
    if not: False
    """
    try:
        real_key = int(string_key)
    except Exception as e:
        return False
    else:
        if real_key in condition_dict.keys():
            return condition_dict[real_key]
        else:
            return False


def check_keyword(keyword, condition_dict):
    """
    check the keyword format, and process it into django ORM filter dict
    :param keyword: come from front end search word
    :param condition_dict: the number key relation with field name
    :return:
    if right: "field__action" and search keyword will form filter dict, return empty error info
    if wrong: add error info
    """
    error_info = ''
    keyword_dict = {}
    filter_dict = {}
    if keyword:
        # split keyword by ','
        keyword_list = keyword.split(',')
    else:
        # keyword is empty, search empty
        return filter_dict, error_info

    for i in keyword_list:
        # split it into field and search keyword
        split = i.split(':')
        if len(split) == 2:
            keyword_dict[split[0]] = split[1]               # form keyword_dict, {"string_ley : value"}
            string_key = split[0]
            value = split[1]

            split_key = string_key.split('__')
            # get real field name
            real_key = split_key[0]
            field = key_exist(real_key, condition_dict)

            if (len(split_key) == 2) and field:
                # if it contains '__'
                filter_method = split_key[1]
                field = '%s__%s' % (condition_dict[int(real_key)], filter_method)     # eg.'account_email__icontains'
                filter_dict[field] = value                                            # form filter_dict for return
            elif len(split_key) == 1 and field:
                # if it not contains '__'
                field = '%s__icontains' % field                                       # default output '__icontains'
                filter_dict[field] = value
            else:
                # error format
                error_info = 'key error, has incorrect key'
                break
        else:
            error_info = 'misuse of "," or ":"'
            break

    return filter_dict, error_info


def thread_strategy(threads_request, host_name, local_threads):
    """
    This function is to determine how to dispatch cpu threads in the local cluster.
    Since the local cluster is not yet being constructed, the strategy mainly for problems under 36 threads.
    1. if sender itself have enough threads, use local instead of mpi(but it is not recommend, because the purpose
    of this system is to use license more efficiently. In short, use as much threads as you can)
    2. in most case, use 2 powerful CAE workstation first.
    3. when use 3 hpc, or unlimited license. 2 CAE WS first, then the local, then use global
    :param threads_request:
    :param host_name:
    :param local_threads:
    :return:
    """
    use_mpi = False
    mpi_host = []
    local_threads = int(local_threads) - 2          # leave 2 threads to be cautious

    if local_threads >= threads_request and threads_request <= 12:
        use_mpi = False
        mpi_host = []
    elif threads_request <= 36:
        with open('./other/cluster_info.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if host_name == row['computer_name']:
                    use_mpi = True
        mpi_host = [['DL5FWYWG2', 10], ['DL5FWYWG2', 10], ['DL25TW5V2', 8], ['DL25TW5V2', 8]]
    else:
        pass                # launch new global strategy
    return use_mpi, mpi_host


