
"""
backup plan for queue. Use While loop to constantly call mission.
If all the conditions are satisfied, especially the license and queue, then do the mission
"""
from .utils import get_first_mission, db_to_running
import time


def take_task(db_wait, pause):
    while True:
        if not pause:
            print('here')
            first_obj = get_first_mission(db_wait)
            if first_obj:
                if able_to_run(first_obj):
                    db_to_running(first_obj)
                    run_task()
            else:
                print('empty')

        time.sleep(5)


def run_task():
    """
    1. send data and signal to tell local machine to run
    :return:
    """
    pass


def able_to_run(mission):
    """
    is it enough resources?
    :param mission:
    :return:
    """
    pass
    return True



# a = threading.Thread(target=utils.take_task, args=[models.WaitList, False])
# a.start()