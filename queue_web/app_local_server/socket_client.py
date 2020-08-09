import socket
import threading


class Websocket_Client(threading.Thread):
    def __init__(self):
        super().__init__()
        self.host = "localhost"
        self.port = 8500
        self.address = (self.host, self.port)
        self.buffer = 1024

    def run(self):
        # 创建TCP客户端程序
        tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 连接服务端
        tcp_client.connect(self.address)
        while True:
            info = tcp_client.recv(self.buffer)
            print("{}".format(str(info, encoding="utf8")))

            msg = input()
            tcp_client.send(msg.encode("utf8"))
            if info.lower().decode("utf8") == "bye":
                tcp_client.close()
                break


if __name__ == '__main__':
    b = Websocket_Client()
    b.start()