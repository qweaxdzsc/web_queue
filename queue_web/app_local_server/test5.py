a = b'HTTP/1.1 200 OK\r\nContent-Type:text/html;charset=utf-8\r\nAccess-Control-Allow-Origin: ' \
    b'*\r\n\r\n\r\n<meta charset="UTF-8"/>' \
    b'{"path": "C:/Users/BZMBN4/Desktop/ansys \\u4e0e Python\\u8054\\u5408\\u5e94\\u7528.pptx"}'

print(a.decode('unicode_escape'))
