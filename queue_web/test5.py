import urllib.request, urllib.parse

a = {'Content-Length': '112', 'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
     'Host': 'localhost:8000',
     'Connection': 'keep-alive', 'Accept': '*/*', 'X-Requested-With': 'XMLHttpRequest',
     'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36',
     'Origin': 'http://localhost:8000', 'Sec-Fetch-Site': 'same-origin', 'Sec-Fetch-Mode': 'cors',
     'Sec-Fetch-Dest': 'empty', 'Referer': 'http://localhost:8000/', 'Accept-Encoding': 'gzip, deflate, br',
     'Accept-Language': 'zh-CN,zh;q=0.9',
     'Cookie': 'Pycharm-bac02343=e240a97b-383c-4876-9d9e-3babd1f8f44d; Pycharm-6ad2a5e5=8b7d8b02-6f03-49aa-ab62-393b8f58fe61; csrftoken=9Gbge1ALaoSk6pvhjMPF6ne8YPNBHbcW1ErfOUsqgJAbT6M6hG6WbCbfPlJwQFfL'}

response = urllib.request.urlopen("http://localhost:8000")
headers = response.getheaders()
print(headers)
cookies = response.getheader('Set-Cookie').split(';')
print(cookies)

# stringify data dict to string
data = {
    'mission_id': 12,
}

data_string = urllib.parse.urlencode(data)
# convert to bytes
last_data = bytes(data_string, encoding='utf-8')
header = {
    'Cookie': cookies[0],
}
request =urllib.request.Request(url="http://localhost:8000/receive_result/", data=last_data, headers=header)
response = urllib.request.urlopen(request)
response_body = response.read().decode('utf-8')
print(response_body)
print(response.getheaders())