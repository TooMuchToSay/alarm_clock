from datetime import datetime
from time import sleep
import subprocess
import pygame
import sys
from os import listdir
from ascii_art import cat

def get_alarm_list():
    choices = listdir("sounds")
    for number in range(0, len(choices)):
        choices[number] = f'{number}:{choices[number]}'
    print(f'list of alarm sounds: {choices}')
    choice = int(input('input the number of your preferred song choice: '))
    alarm_name = choices[choice].split(':')
    return f'sounds/{alarm_name[1]}'

def get_time_convert():
    current_datetime = datetime.now()
    current_date = current_datetime.strftime('%H:%M')
    return current_date

def get_time_limit():
    try:
        time_limit = input("length of timer in 'minutes:seconds! ").strip()
    except ValueError:
        print('Sorry the inputted time was not convertible to a int')
        get_time_limit()
    return time_limit

def convert_time(time): #THIS IS CALLED FOR BOTH THE START TIME AND THE END TIME BECAUSE IT WORKS FOR BOTH H>M CONVERSION AND M>S CONVERSION
    time = time.split(':')
    minutes = int(time[0]) * 60 + int(time[1])
    return minutes

def track_time(start_time, time_limit):
    time = convert_time(time_limit)
    start_time = convert_time(start_time)
    time_in_minutes_done = time + start_time
    duration = (time_in_minutes_done - start_time) #gets seconds
    for i in range(duration, -1, -1):
        subprocess.run(['clear'])
        if i == 0:
            print(cat('LE TEMPS EST FINIT'))
            return True
        else:
            message = cat(f'You have {i} seconds left')
            print(message)
 
        sleep(1)
       
def play_alarm(status, choice):
    pygame.mixer.init()
    pygame.mixer.music.load(choice) #plays any track as alarm if you give it the update
    pygame.mixer.music.play(loops=-1) #loops each time
    exit = input("input EXIT to stop alarm sound: ")
    match exit:
        case 'EXIT':
            sys.exit(0)


