from datetime import datetime
from time import sleep
import sys
def get_time_convert():
    current_datetime = datetime.now()
    current_date = current_datetime.strftime('%H:%M')
    return current_date

def get_time_limit():
    try:
        time_limit = int(input("length of timer in minutes: "))
    except ValueError:
        print('Sorry the inputted time was not convertable to an integer')
        get_time_limit()
    return time_limit

def convert_time(time):
    time = time.split(':')
    minutes = int(time[0]) * 60 + int(time[1])
    return minutes

def track_time(start_time, time_limit):
    time = start_time.split(":")
    time_in_minutes_start = int(time[0]) * 60 + int(time[1])
    time_in_minutes_done = time_in_minutes_start + time_limit
    #gives you minutes since midnight
    #get the time between done and start_time
    duration = (time_in_minutes_done - time_in_minutes_start) * 60 #gets seconds
    for i in range(duration, 0, -1):
        if i == 0:
            print('Timer done' * 100)
            break
        else:
            print(f'time left in seconds: {i}')




        sleep(1) #wait for one second to update loopme````
