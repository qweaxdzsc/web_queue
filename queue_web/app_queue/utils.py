from app_queue import models
from django.db.models import Min, Max
import csv
import threading
import datetime
import urllib.request
import urllib.parse


def max_order_id(db_model):
    order_id_dict = db_model.objects.aggregate(Max('order_id'))
    return order_id_dict['order_id__max']


def min_order_id(db_model):
    order_id_dict = db_model.objects.aggregate(Min('order_id'))
    return order_id_dict['order_id__min']


def new_order_id(db_model, main_app):
    filter_dict = {'exec_app': main_app}
    order_id_dict = db_model.objects.filter(**filter_dict).aggregate(Max('order_id'))
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


def next_mission(main_app, check_dict, pre_check=False):
    print('bring next mission')
    mission = get_first_mission(models.WaitList, main_app)
    if mission:
        data_dict = mission.get_data_dict()
        if pre_check:
            available = app_prerequisite(check_dict, main_app)
            if available:
                exec_mission(data_dict)
                print('exec_mission')
            else:
                virtual_mission(main_app, check_dict)
        else:
            exec_mission(data_dict)
            print('exec_mission')


def exec_mission(data_dict):
    # send mission to local to run
    print('direct run')
    data_string = urllib.parse.urlencode(data_dict['mission_data'])
    last_data = bytes(data_string, encoding='utf-8')
    response = urllib.request.urlopen("http://%s:37171/get_task" % data_dict['host_name'], data=last_data)
    dict = response.read().decode('utf-8')
    print('response from local', dict)
    # add to running list
    data_dict['register_time'] = datetime.datetime.now()
    db_add_one(models.RunningList, data_dict)


def virtual_mission(main_app, check_dict):
    """
    This function is design to solve the problem when have empty running list,
    but without license. it need a trigger to check when have license available.
    create virtual mission to occupy the running list, when it's done.
    will call the next mission
    :return:
    """
    threading.Timer(10, next_mission, args=(main_app, check_dict, True, ))


def app_prerequisite(check_dict, main_app):
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
        keyword_list = keyword.split(',')
    else:
        return filter_dict, error_info

    for i in keyword_list:
        split = i.split(':')
        if len(split) == 2:
            keyword_dict[split[0]] = split[1]
            string_key = split[0]
            value = split[1]
            split_key = string_key.split('__')
            real_key = split_key[0]
            field = key_exist(real_key, condition_dict)
            if (len(split_key) == 2) and field:
                filter_method = split_key[1]
                field = '%s__%s' % (condition_dict[int(real_key)], filter_method)
                filter_dict[field] = value
            elif len(split_key) == 1 and field:
                field = '%s__icontains' % field
                filter_dict[field] = value
            else:
                error_info = 'key error, has incorrect key'
                break
        else:
            error_info = 'misuse of "," or ":"'
            break

    return filter_dict, error_info


def thread_strategy(threads, host_name, cpu_left):
    """
    This function is to determine how to dispatch cpu threads in the local cluster.
    Since the local cluster is not yet being constructed, the strategy mainly for problems under 36 threads.
    1. if sender itself have enough threads, use local instead of mpi(but it is not recommend, because the purpose
    of this system is to use license more efficiently. In short, use as much threads as you can)
    2. in most case, use 2 powerful CAE workstation first.
    3. when use 3 hpc, or unlimited license. 2 CAE ws first, then the local, then use global
    :param threads:
    :param host_name:
    :param cpu_left:
    :return:
    """
    use_mpi = False
    mpi_host = []
    cpu_left = float(cpu_left) - 4

    if cpu_left > threads and threads <= 12:
        use_mpi = False
        mpi_host = []
    elif threads <= 36:
        with open('./other/cluster_info.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if host_name == row['computer_name']:
                    use_mpi = True
        mpi_host = [['DL5FWYWG2', 10], ['DL5FWYWG2', 10], ['DL25TW5V2', 8], ['DL25TW5V2', 8]]
    else:
        pass                # launch new global strategy
    return use_mpi, mpi_host


