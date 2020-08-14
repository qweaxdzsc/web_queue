class a:
    def __init__(self):
        self.attr = 2


dic = {
    a: 5,
}

for key in dic.keys():
    b = a()
    print(b.attr)