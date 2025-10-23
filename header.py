import time
from helper_functions import get_time_convert
from helper_functions import get_time_limit
from helper_functions import track_time
from helper_functions import play_alarm
def main():
    #have user define if they want to start the time
    #call function to capture time
    start_time = get_time_convert()
    time_limit = get_time_limit()
    #print(time_limit)
    status = track_time(start_time, time_limit)
    play_alarm(status)
    #count time till amount of time has passed
    #output sound 

main()
