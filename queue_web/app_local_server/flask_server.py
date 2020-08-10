import tkinter as tk
from tkinter import filedialog
import sys
import threading
from flask import Flask, send_from_directory, make_response
app = Flask(__name__)
# app.config['JSON_AS_ASCII'] = False


@app.route('/download')
def download():
    return send_from_directory(r"C:\Users\BZMBN4\Desktop", filename="123.txt", as_attachment=True)


@app.route('/file')
def local_file():
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
    print('test web:  http://localhost:8500/file')
    app.run(debug=True, host='localhost', port='8500')


