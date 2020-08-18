import tkinter as tk
from tkinter import filedialog
import os
import socket
import sys
import threading
from flask import Flask, make_response, request
app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False


class DoTasks(threading.Thread):
    def __init__(self, tasks_dict):
        super().__init__()
        self.tasks_dict = tasks_dict
        self.app_dir = r'.\app'

    def run(self):
        task_number = len(self.tasks_dict)
        app_list = os.listdir(self.app_dir)
        for i in range(task_number):
            task_dict = eval(self.tasks_dict[str(i)])
            print('Task%s: ' % i, task_dict)
            if task_dict['software'] in app_list:
                script_path = '%s/%s/main.py' % (self.app_dir, task_dict['software'])
                print(os.getcwd())
                exec(open(script_path, 'r').read(), task_dict)

    def return_result(self):
        pass


@app.route('/get_task', methods=['GET', 'POST'])
def get_task():
    if request.method == 'POST':
        do_task = DoTasks(request.form)
        do_task.start()

    return 'receive tasks'


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


