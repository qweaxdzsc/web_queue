import time
import threading

a = [1]


def test(a):
    print(a)


timer = threading.Timer(5, test, args=(a,))
timer.start()

a[0] = 2
print(a)
