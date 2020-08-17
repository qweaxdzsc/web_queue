import tkinter as tk
from tkinter import filedialog
import sys
import threading
from flask import Flask, make_response, request
app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False


@app.route('/do_task', methods=['GET', 'POST'])
def do_task():
    if request.method == 'POST':
        task_number = len(request.form)
        for i in range(task_number):
            task_dict = eval(request.form[str(i)])
            print(type(task_dict), task_dict)

    # set CORS response
    response_dict = {
        'connected': True,
    }
    response = make_response(response_dict)
    return response


@app.route('/file')
def get_local_file():
    root = tk.Tk()
    root.withdraw()
    root.attributes('-topmost', True)
    file_path = filedialog.askopenfilename()
    data = {
        'path': file_path,
    }
    root.destroy()

    response = make_response(data)
    # 设置响应请求头
    response.headers["Access-Control-Allow-Origin"] = '*'
    response.headers["Access-Control-Allow-Methods"] = 'GET'
    response.headers["Access-Control-Allow-Headers"] = "x-requested-with,content-type"
    return response


if __name__ == '__main__':
    print('test web:  http://localhost:8500/do_task')
    app.run(debug=True, host='0.0.0.0', port='8500')


