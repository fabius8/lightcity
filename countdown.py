#!/usr/local/bin/python3

import time
import datetime
import os

now = datetime.datetime.now()
seconds = now.hour * 60 * 60 + now.minute * 60 + now.second
last_seconds = 86400 - seconds
print("Last seconds to 00:00 left", last_seconds, "secs")


def countdown(t):
    while t:
        mins, secs = divmod(t, 60)
        timer = '{:02d}:{:02d}'.format(mins, secs)
        print(timer, end="\r")
        time.sleep(1)
        t -= 1
    print('Blast Off!!!')


t = input("Enter the time in seconds: ")
if t == "":
    t = last_seconds
countdown(int(t))
os.system("say blast off")
