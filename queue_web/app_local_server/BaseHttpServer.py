from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import tkinter as tk
from tkinter import filedialog

#
# class Resquest(BaseHTTPRequestHandler):
#     def do_GET(self):
#         self.dispatch_url()
#
#     def do_POST(self):
#         self.dispatch_url()
#
#     def dispatch_url(self):
#         print('path:%s' % self.path)
#         self.url_dict = {
#             '/file': self.get_local_file,
#         }
#         for url, func in self.url_dict.items():
#             if self.path == url:
#                 print('find view func: %s' % func.__name__)
#                 func()
#
#     def form_response_json(self, data):
#         self.send_response(200)
#         self.close_connection = True
#         self.send_header('Content-type', 'application/json')
#         self.send_header('Access-Control-Allow-Origin', '*')
#         self.send_header('Access-Control-Allow-Methods', 'PUT,GET,POST,DELETE')
#         self.end_headers()
#         self.wfile.write(json.dumps(data).encode())
#         self.wfile.flush()
#         self.connection.close()
#
#     def get_local_file(self):
#         # root = tk.Tk()
#         # root.withdraw()
#         #
#         # file_path = filedialog.askopenfilename()
#
#         # data = {'path': file_path}
#         data = {'path': 'file_path'}
#         self.form_response_json(data)


class Resquest(BaseHTTPRequestHandler):
    def do_GET(self):
        data = {'path': 'file_path'}
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Connection', 'close')
        self.send_header('Access-Control-Allow-Origin', '*')
        # self.send_header('Access-Control-Allow-Methods', 'PUT,GET,POST,DELETE')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())
        self.finish()




if __name__ == '__main__':
    host = ('localhost', 8888)
    server = HTTPServer(host, Resquest)
    print("Starting server, listen at: http://%s:%s" % host)
    server.serve_forever()
