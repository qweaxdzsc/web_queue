import socket
import threading
import json
import tkinter as tk
from tkinter import filedialog


class Websocket_Server(threading.Thread):
    def __init__(self, port):
        self.port = port
        self.client = dict()
        super(Websocket_Server, self).__init__()

    def run(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(("127.0.0.1", self.port))
        sock.listen(20)

        while True:                                                                 # 等待客户端连接
            conn, addr = sock.accept()
            print("客户端{}连接成功:".format(addr))
            try:

                info = conn.recv(1024)
                connId = "ID:" + str(addr[1])
                self.client[connId] = conn
                print("{0}:{1}".format(connId, info.decode("utf8")))
            except Exception as e:
                print(e)
            response = 'HTTP/1.1 200 OK\r\n'  # 模拟相应行
            response += 'Content-Type:text/html;charset=utf-8\r\n'  # 模拟响应头
            response += 'Access-Control-Allow-Origin: *\r\n'  # 模拟响应头
            response += '\r\n\r\n'  # 模拟空行

            root = tk.Tk()
            root.withdraw()

            file_path = filedialog.askopenfilename()

            data = {'path': file_path}
            response += '<meta charset="UTF-8"/>' # 模拟响应体
            response += json.dumps(data)  # 模拟响应体
            conn.send(response.encode('utf8'))
            conn.close()


if __name__ == '__main__':
    a = Websocket_Server(8500)
    a.start()
    print('Listening IP: http://localhost:8500')
