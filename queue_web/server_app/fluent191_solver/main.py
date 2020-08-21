
import os

global extension

task_info = {
    "make_journal": True,
    "iterations": 1000,
    "use_mpi": True,
    "mpi_host": {'DL5FWYWG2': 2, 'DL25TW5V2': 2},
    "command": r"3d -t4 -i G:/test/queue_test2/Test_V1_solve.jou -mpi=ibmmpi -cnf=mpi_host.txt",
}

if extension == '.jou':
    task_info["make_journal"] = False


file_name = 'sods_v1_solve.py'
project_name, extension = os.path.splitext(file_name)
