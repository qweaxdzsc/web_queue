import os
import subprocess
import socket
import threading
import urllib.request
import urllib.parse
import tkinter as tk
from tkinter import filedialog
from psutil import cpu_percent, cpu_count

from flask import Flask, make_response, request, send_from_directory
app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

# Global variable
running_list = list()
temporary_file = './temp.txt'  # in case the connection with server is down
version = 1.1


class DoTasks(threading.Thread):
    def __init__(self, tasks_dict):
        super().__init__()
        self.tasks_dict = tasks_dict
        self.app_dir = r'local_app'
        self.return_data = dict()

    def run(self):
        task_number = len(self.tasks_dict)
        app_list = os.listdir(self.app_dir)
        for i in range(task_number):
            task_dict = eval(self.tasks_dict[str(i)])
            print('Task%s: ' % i, task_dict)
            task_dict['mission_status'] = 'not start'
            if task_dict['software'] in app_list:
                script_path = '%s/%s/main.py' % (self.app_dir, task_dict['software'])
                try:
                    # print('pass')
                    exec(open(script_path, 'r').read(), task_dict)
                except Exception as e:
                    print(e)
                else:
                    print(task_dict['mission_status'])
            self.return_data['%s_mission_status' % i] = task_dict['mission_status']
        self.return_data['order_id'] = task_dict['order_id']
        self.return_data['software'] = task_dict['software']
        running_list.remove(self.tasks_dict)
        self.return_result()

    def return_result(self):
        url = "http://localhost/receive_result/"
        response = self.post_request(url, self.return_data)
        print(response)

    def post_request(self, url, new_dict):
        """
        1. get csrf token dict include data and header
        2. add new data dict
        3. make post request with formed data and header
        :param url: post address
        :param new_dict: new data dict
        :return: urllib request response object
        """
        response = urllib.request.urlopen("http://localhost/get_csrf")
        csrf_dict = eval(response.read().decode())
        # stringify data dict to string
        data_dict = csrf_dict['data']
        data_dict.update(new_dict)
        data_string = urllib.parse.urlencode(data_dict)
        # # convert to bytes
        last_data = bytes(data_string, encoding='utf-8')
        header = csrf_dict['header']
        formed_request = urllib.request.Request(url=url, data=last_data, headers=header)
        try:
            response = urllib.request.urlopen(formed_request)
        except Exception as e:
            print(e)
            with open(temporary_file, 'a') as f:
                f.write(str(self.return_data))
        else:
            response_body = response.read().decode('utf-8')
            print(response_body)
            return response


@app.route('/get_task', methods=['GET', 'POST'])
def get_task():
    if request.method == 'POST':
        do_task = DoTasks(request.form)
        do_task.start()
        running_list.append(request.form)

    return 'flask server receive tasks'


@app.route('/file')
def get_local_file():
    root = tk.Tk()
    root.withdraw()
    root.attributes('-topmost', True)
    file_path = filedialog.askopenfilename()

    root.destroy()

    host_name = socket.gethostname()
    local_ip = socket.gethostbyname(host_name)
    cpu_left = cores_left()
    data = {
        'path': file_path,
        'host_name': host_name,
        'local_ip': local_ip,
        'cpu_left': cpu_left,
    }
    response = make_response(data)
    # 设置响应请求头
    response.headers["Access-Control-Allow-Origin"] = '*'
    response.headers["Access-Control-Allow-Methods"] = 'GET'
    response.headers["Access-Control-Allow-Headers"] = "x-requested-with,content-type"
    return response


@app.route('/cores')
def get_cores_left():
    cpu_left = str(cores_left())

    return cpu_left


@app.route('/connection')
def get_cores_left():
    return version


def cores_left():
    cpu_usage = cpu_percent(0.1)
    output_cores = cpu_count()
    cpu_left = output_cores * (1 - cpu_usage/100)

    return cpu_left

#
# @app.route('/download')
# def download():
#     directory = r'C:\Users\zonghui\Desktop'
#     file_name = 'freecad.7z'
#     return send_from_directory(directory, filename=file_name, as_attachment=True)
#


if __name__ == '__main__':
    # print('test web:  http://localhost:37171/do_task')
    app.run(debug=True, host='0.0.0.0', port='37171')


