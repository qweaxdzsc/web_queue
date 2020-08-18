#
# # from tkinter import filedialog
# #
# # root = tkinter.Tk()
# # root.withdraw()
# task_dict = {
#     "id": '105',
#     "software": "fluent191_solver",
#     "use_mpi": False,
#     "mpi_host": "",
#     "command": r"3d -t4 -i G:\test\queue_test2\Test_V1_mesh.jou",
#     "project_address": "G:/test/queue_test2",
#     "project_name": "Test_V1_solve",
# }
#
# file_name = r'app_local_server/app/fluent191_solver/main.py'
# # while not file_name.endswith('.py'):
# #     file_name = filedialog.askopenfilename()
#
# parameter = {
#
# }
#
# exec(open(file_name, 'r').read(), task_dict)
#
# # print(parameter)
# # print(task_dict)

from app_local_server.app.report_standard import main