import time

start_time = time.time()
import urllib.request
import urllib.parse

# 定义一个字典参数
task_dict = {
    "software": "fluent_solver",
    "use_mpi": True,
    "command": r"3d -t12 -i G:\test\queue_test1\test2.jou",
    "mpi_host": "",
}

data_dict = {}
data_dict[0] = task_dict
# 使用urlencode将字典参数序列化成字符串
data_string = urllib.parse.urlencode(data_dict)
# 将序列化后的字符串转换成二进制数据，因为post请求携带的是二进制参数
last_data = bytes(data_string, encoding='utf-8')
# 如果给urlopen这个函数传递了data这个参数，那么它的请求方式则不是get请求，而是post请求
response = urllib.request.urlopen("http://localhost:8500/do_task", data=last_data)
# 我们的参数出现在form表单中，这表明是模拟了表单的提交方式，以post方式传输数据

dict = response.read().decode('utf-8')
print(dict)
print(response.getheaders())


end_time = time.time()
print(end_time - start_time)