data_dict = {}
task_dict0 = {'software': 'fluent191_solver',
              'project_name': 'queue_test3_solve',
              'project_address': 'G:/test/queue_test3',
              'extension': '.jou',
              'host_name': 'DL5FWYWG2',
              'order_id': 1,
              'threads': 12,
              'use_mpi': False,
              'mpi_host': []}

task_dict1 = {
    "id": '105',
    "software": "extend_report_standard",
    "use_mpi": False,
    "mpi_host": {},
    "command": r"",
    "project_address": "G:/test/queue_test2",
    "project_name": "Test_V1",
}
data_dict['0'] = task_dict0
import os
task_number = len(data_dict)
app_dir = r'./app_local_server/local_app'
app_list = os.listdir(app_dir)
for i in range(task_number):
    task_dict = data_dict[str(i)]
    print('Task%s: ' % i, task_dict)
    task_dict['mission_status'] = 'not start'
    if task_dict['software'] in app_list:
        script_path = '%s/%s/main.py' % (app_dir, task_dict['software'])
        exec(open(script_path, 'r').read(), task_dict)