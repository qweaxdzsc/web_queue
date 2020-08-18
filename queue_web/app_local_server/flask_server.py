import tkinter as tk
from tkinter import filedialog
import os
import socket
import threading
import urllib.request
import urllib.parse
from flask import Flask, make_response, request
app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False


class DoTasks(threading.Thread):
    def __init__(self, tasks_dict):
        super().__init__()
        self.tasks_dict = tasks_dict
        self.app_dir = r'.\app'
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
                    print('pass')
                    # exec(open(script_path, 'r').read(), task_dict)
                except Exception as e:
                    print(e)
                else:
                    print(task_dict['mission_status'])
            self.return_data['%s_mission_status' % i] = task_dict['mission_status']
        self.return_data['mission_id'] = task_dict['id']
        self.return_result()

    def return_result(self):
        # GET request to get cookie
        response = urllib.request.urlopen("http://localhost:8000")
        cookie = response.getheaders('Set-Cookie')
        # stringify data dict to string
        data_string = urllib.parse.urlencode(self.return_data)
        # convert to bytes
        last_data = bytes(data_string, encoding='utf-8')
        response = urllib.request.urlopen("http://localhost:8000/receive_result/", data=last_data)
        response_body = response.read().decode('utf-8')
        print(response_body)
        print(response.getheaders())


@app.route('/get_task', methods=['GET', 'POST'])
def get_task():
    if request.method == 'POST':
        do_task = DoTasks(request.form)
        do_task.start()

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
    data = {
        'path': file_path,
        'host_name': host_name,
        'local_ip': local_ip,
    }
    response = make_response(data)
    # 设置响应请求头
    response.headers["Access-Control-Allow-Origin"] = '*'
    response.headers["Access-Control-Allow-Methods"] = 'GET'
    response.headers["Access-Control-Allow-Headers"] = "x-requested-with,content-type"
    return response


if __name__ == '__main__':
    print('test web:  http://localhost:8500/do_task')
    app.run(debug=True, host='0.0.0.0', port='8500')


