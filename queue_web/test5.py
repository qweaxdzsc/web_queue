import os

task_info = {
    'project_name': 'Test_V1_solve',
    "project_address": r'G:/test/queue_test2',
    'extension': '.jou',
    'host_name': 'DL5FWYWG2',
    'iterations': 1000,
    "id": '105',
    "use_mpi": True,
    'threads': 12,
    "mpi_host": {'DL5FWYWG2': 2, 'DL25TW5V2': 2},
    "command": r"3d -t4 -i G:/test/queue_test2/Test_V1_solve.jou -mpi=ibmmpi -cnf=mpi_host.txt",
}


print(os.getcwd())
exec(open(r'./server_app/fluent191_solver/main.py', 'r').read(), task_info)
print(task_info)
