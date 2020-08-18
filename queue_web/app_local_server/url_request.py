import time

start_time = time.time()
import urllib.request
import urllib.parse

# 定义一个字典参数
data_dict = {}
# root.withdraw()
task_dict0 = {
    "id": '105',
    "software": "fluent191_solver",
    "use_mpi": True,
    "mpi_host": {'DL5FWYWG2': 2, 'DL25TW5V2': 2},
    "command": r"3d -t4 -i G:/test/queue_test2/Test_V1_solve.jou -mpi=ibmmpi -cnf=mpi_host.txt",
    "project_address": "G:/test/queue_test2",
    "project_name": "Test_V1_solve",
}

task_dict1 = {
    "id": '105',
    "software": "report_standard",
    "use_mpi": False,
    "mpi_host": {},
    "command": r"",
    "project_address": "G:/test/queue_test2",
    "project_name": "Test_V1_solve",
}
data_dict[0] = task_dict1
# data_dict[1] = task_dict1

# 使用urlencode将字典参数序列化成字符串
data_string = urllib.parse.urlencode(data_dict)
# 将序列化后的字符串转换成二进制数据，因为post请求携带的是二进制参数
last_data = bytes(data_string, encoding='utf-8')
# 如果给urlopen这个函数传递了data这个参数，那么它的请求方式则不是get请求，而是post请求
response = urllib.request.urlopen("http://localhost:8500/get_task", data=last_data)
# 我们的参数出现在form表单中，这表明是模拟了表单的提交方式，以post方式传输数据

dict = response.read().decode('utf-8')
print(dict)
print(response.getheaders())


end_time = time.time()
print(end_time - start_time)