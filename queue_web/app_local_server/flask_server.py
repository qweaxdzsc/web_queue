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
temporary_folder = './temp_store'  # in case the connection with server is down
version = 1.1


class DoTasks(threading.Thread):
    def __init__(self, tasks_dict, remote_addr):
        super().__init__()
        self.tasks_dict = tasks_dict
        self.remote_addr = remote_addr
        self.app_dir = r'local_app'
        self.return_data = dict()

    def run(self):
        task_number = len(self.tasks_dict)
        app_list = os.listdir(self.app_dir)
        script_path = ""
        main_task_folder = ""
        print("task_number", task_number)
        for i in range(task_number):
            task_dict = eval(self.tasks_dict[str(i)])
            print('Task%s: ' % i, task_dict)
            task_dict['mission_status'] = 'not start'
            if i == 0:
                main_task_folder = f"{self.app_dir}/{task_dict['software']}"
                script_path = f"{main_task_folder}/main.py"
                self.return_data['order_id'] = task_dict['order_id']
                self.return_data['project_name'] = task_dict['project_name']
                self.return_data['software'] = task_dict['software']
            else:
                script_path = f"{main_task_folder}/extend_{task_dict['software']}/main.py"
            try:
                print('start exec')
                exec(open(script_path, 'r').read(), task_dict)
            except Exception as e:
                print(e)
            else:
                print(task_dict['mission_status'])
            self.return_data['%s_mission_status' % i] = task_dict['mission_status']
        running_list.remove(self.tasks_dict)
        self.return_result()

    def return_result(self):
        response = post_request(self.remote_addr, self.return_data)
        print(response)


def post_request(remote_addr, new_dict):
    """
    1. get csrf token dict include data and header
    2. add new data dict
    3. make post request with formed data and header
    :param url: post address
    :param new_dict: new data dict
    :return: urllib request response object
    """
    response = urllib.request.urlopen("http://%s/get_csrf" % remote_addr)
    csrf_dict = eval(response.read().decode())
    # stringify data dict to string
    data_dict = csrf_dict['data']
    data_dict.update(new_dict)
    data_string = urllib.parse.urlencode(data_dict)
    # # convert to bytes
    last_data = bytes(data_string, encoding='utf-8')
    header = csrf_dict['header']
    url = "http://%s/receive_result/" % remote_addr
    formed_request = urllib.request.Request(url=url, data=last_data, headers=header)
    try:
        response = urllib.request.urlopen(formed_request)
    except Exception as e:
        print(e)
        temporary_file = f'{temporary_folder}/{new_dict["project_name"]}_{new_dict["order_id"]}.txt'
        with open(temporary_file, 'w') as f:
            f.write(str(new_dict))
    else:
        response_body = response.read().decode('utf-8')
        print(response_body)
        return response


@app.route('/get_task', methods=['GET', 'POST'])
def get_task():
    if request.method == 'POST':
        do_task = DoTasks(request.form, request.remote_addr)
        do_task.start()
        running_list.append(request.form)
        print('task from: ', request.remote_addr)
        print('running_list:', request.form)

    return 'flask server receive tasks'


@app.route('/file')
def get_local_file():
    root = tk.Tk()
    root.withdraw()
    root.attributes('-topmost', True)

    file_path = filedialog.askopenfilename()

    root.destroy()
    # recommend app
    recommend_app = 'none'
    file_name = os.path.split(file_path)[1]
    if 'solve' in file_name:
        recommend_app = 'fluent191_solver'
    elif 'mesh' in file_name:
        recommend_app = 'fluent201_mesh'

    # get local computer info
    host_name = socket.gethostname()
    local_ip = socket.gethostbyname(host_name)
    total_cores = cpu_count()
    data = {
        'path': file_path,
        'recommend_app': recommend_app,
        'host_name': host_name,
        'local_ip': local_ip,
        'total_cores': total_cores,
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
def get_version():
    return version


@app.route('/check_running', methods=['GET', 'POST'])
def check_running():
    check_data = request.form
    print(request.form)
    if check_data in running_list:
        return 'running'
    else:
        print('request form first dict', request.form["0"])
        task_dict = eval(request.form["0"])
        return_data = dict()
        try:
            temporary_file = f'{temporary_folder}/{task_dict["project_name"]}_{task_dict["order_id"]}.txt'
        except Exception as e:
            return_data['%s_mission_status' % 0] = 'abnormal'
            return_data['order_id'] = request.form['order_id']
            return_data['project_name'] = request.form['project_name']
            return_data['software'] = request.form['software']
        else:
            if os.path.exists(temporary_file):
                # if record temporary file
                with open(temporary_file, 'r') as f:
                    return_data = eval(f.read())
            else:
                # if no temporary file, consider it abolished
                return_data['%s_mission_status' % 0] = 'abnormal'
                return_data['order_id'] = request.form['order_id']
                return_data['project_name'] = request.form['project_name']
                return_data['software'] = request.form['software']

        # return info anyway to finish this mission
        url = "http://%s/receive_result/" % request.remote_addr
        response = post_request(url, return_data)
        print(response)


def cores_left():
    cpu_usage = cpu_percent(0.1)                    # use psutil to get cpu using percentage
    total_cores = cpu_count()                       # use psutil to get total threads number
    cpu_left = total_cores * (1 - cpu_usage/100)

    return cpu_left


# @app.route('/download')
# def download():
#     directory = r'C:\Users\zonghui\Desktop'
#     file_name = 'freecad.7z'
#     return send_from_directory(directory, filename=file_name, as_attachment=True)
#


if __name__ == '__main__':
    # print('test web:  http://localhost:37171/do_task')
    app.run(debug=True, host='0.0.0.0', port='37171')


