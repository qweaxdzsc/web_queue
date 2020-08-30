import threading
print('create virtual mission')


def next_mission(main_app, check_dict, pre_check=False):
    print('bring next mission')
    timer = threading.Timer(1, next_mission, args=(main_app, check_dict, True,))
    timer.start()
    print(threading.activeCount())

main_app = '1'
check_dict = 'asd'
timer = threading.Timer(1, next_mission, args=(main_app, check_dict, True,))
timer.start()

