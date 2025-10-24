from datetime import datetime
from time import sleep
import subprocess
import pygame
import sys

def get_time_convert():
    current_datetime = datetime.now()
    current_date = current_datetime.strftime('%H:%M')
    return current_date

def get_time_limit():
    try:
        time_limit = int(input("length of timer in minutes: "))
    except ValueError:
        print('Sorry the inputted time was not convertible to a float')
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
            subprocess(["echo 'TIMER IS UP' | cowsay"], shell=True)
            pygame.mixer.init()
            pygame.mixer.music.load('/home/toomuchtosay/alarm_clock/Subwoofer Lullaby.mp3')
            pygame.mixer.music.play()
            return True
        else:
            with open("text.txt", 'w') as file:
                file.write(f'time left in seconds: {i}')
            #importint(f'time left in seconds: {i}')
            subprocess.run(['cat text.txt | cowsay'], shell=True, check=True) #shell allows it to run as a single lined command
            with open('text.txt', 'w') as file:
                file.write('')
        #if i % 5 == 0:
         #   subprocess.run(['clear'])
            

        sleep(1) #wait for one second to update loopme````
def play_alarm(status):
    pygame.mixer.init()
    pygame.mixer.music.load(sys.argv[1]) #plays any track as alarm if you give it the update
    pygame.mixer.music.play()
    exit = input("input EXIT to stop alarm sound")
    match exit:
        case 'EXIT':
            sys.exit(0)


