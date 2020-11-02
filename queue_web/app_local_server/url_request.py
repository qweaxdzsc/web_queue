import time

start_time = time.time()
import urllib.request
import urllib.parse
import socket
from psutil import cpu_percent, cpu_count

# 定义一个字典参数
# data_dict = {}
# root.withdraw()
# task_dict0 = {'software': 'fluent191_solver',
#               'project_name': 'queue_test3_solve',
#               'project_address': 'G:/test/queue_test3',
#               'extension': '.jou',
#               'host_name': 'DL5FWYWG2',
#               'order_id': 1,
#               'threads': 12,
#               'use_mpi': False,
#               'mpi_host': []}
#
# task_dict1 = {
#     "id": '105',
#     "software": "extend_report_standard",
#     "use_mpi": False,
#     "mpi_host": {},
#     "command": r"",
#     "project_address": "G:/test/queue_test2",
#     "project_name": "Test_V1",
# }
# data_dict[0] = task_dict0
# data_dict[1] = task_dict1

# host_name = socket.gethostname()
# local_ip = socket.gethostbyname(host_name)
# total_cores = cpu_count()
#
# data_dict = {
#     "select_main_app": 'fluent191_solver',
#     "select_fluent191_solve": "",
#     "input_local_file": r"G:\test\queue_test2\queue_test2_solve.jou",
#     "user_name": "zonghui.jin",
#     "host_name": host_name,
#     "local_ip": local_ip,
#     "total_cores": 28,
# }
# 使用urlencode将字典参数序列化成字符串
file = r'G:\_HAVC_Project\GEM\GEM_05_defog\GEM_V12.5_defog\result_GEM_V12.5_defog\evap_out.jpg'
data_dict = {
    "file_list": [open(file, 'rb').read()]
}
data_string = urllib.parse.urlencode(data_dict)
# 将序列化后的字符串转换成二进制数据，因为post请求携带的是二进制参数
print(data_string)
last_data = bytes(data_string, encoding='utf-8')
# # 如果给urlopen这个函数传递了data这个参数，那么它的请求方式则不是get请求，而是post请求
response = urllib.request.urlopen("http://localhost:80/api/upload/", data=last_data)
# # 我们的参数出现在form表单中，这表明是模拟了表单的提交方式，以post方式传输数据
#
# dict = response.read().decode('utf-8')
# print(dict)
# print(response.getheaders())

end_time = time.time()
print(end_time - start_time)
