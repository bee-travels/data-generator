# 100 users
# start 100 timerTask
from threading import Timer
import atexit

class Repeat(object):

    count = 0
    @staticmethod
    def repeat(rep, delay, func):
        "repeat func rep times with a delay given in seconds"

        if Repeat.count < rep:
            # call func, you might want to add args here
            func()
            Repeat.count += 1
            # setup a timer which calls repeat recursively
            # again, if you need args for func, you have to add them here
            timer = Timer(delay, Repeat.repeat, (rep, delay, func))
            # register timer.cancel to stop the timer when you exit the interpreter
            atexit.register(timer.cancel)
            timer.start()



