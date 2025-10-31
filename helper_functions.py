from datetime import datetime
from time import sleep
import subprocess
import pygame
import sys
from os import listdir
from ascii_art import cat
from random import randint
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
        get_time_limit('')
    return time_limit

def convert_time(time): #THIS IS CALLED FOR BOTH THE START TIME AND THE END TIME BECAUSE IT WORKS FOR BOTH H>M CONVERSION AND M>S CONVERSION
    time = time.split(':')
    minutes = int(time[0]) * 60 + int(time[1])
    return minutes

def time_presentation(seconds):
    time = seconds  

    #print(f"Starting countdown from {seconds} seconds...")

    if time > 0:
        
        remainder_h = time // 3600
        
        seconds_after_h = time % 3600
        remainder_m = seconds_after_h // 60
        
        remainder_s = seconds_after_h % 60
        
        time_str = f"{remainder_h:02d}:{remainder_m:02d}:{remainder_s:02d}"
        
        sys.stdout.write(f"Remaining: {time_str}")
        sys.stdout.flush() 
        sys.stdout.write('\r') 

    #print("\nCountdown complete! The timer reached 00:00:00.")
    
    return f"{time_str}"

def track_time(start_time, time_limit):
    #block of code that hardcodes the song you want to play while the time is going
    song_options = listdir('sounds')
    random = randint(0, len(song_options) - 1)
    pygame.mixer.init()
    pygame.mixer.music.load(f'sounds/{song_options[random]}')
    pygame.mixer.music.play(loops=-1)
    #end of block#
    time = convert_time(time_limit)
    start_time = convert_time(start_time)
    time_in_minutes_done = time + start_time
    duration = (time_in_minutes_done - start_time) #gets seconds
    message_loop_tracker = 0
    for i in range(duration, -1, -1):
        subprocess.run(['clear'])
        if i == 0:
            pygame.mixer.music.stop()
            print(cat('LE TEMPS EST FINIT', message_loop_tracker))
            return True
        else:
            if message_loop_tracker < 22: 
                message = cat(f'You have {time_presentation(i)} seconds left', message_loop_tracker)
                print(message.strip())
                message_loop_tracker += 1
            elif message_loop_tracker == 22:
                message_loop_tracker = 0
                message = cat(f'You have {time_presentation(i)} seconds left', message_loop_tracker)
                print(message)
        sleep(1)

def play_waiting_song(duration):
    duration = convert_time(duration)
    choices = get_alarm_list()
    pygame.mixer.init()
    pygame.mixer.music.load(choices)
    pygame.mixer.music.play(loops=-1)
    for i in range(duration, 0, -1):
        if i == 1:
            pygame.music.mixer.stop()
        sleep(1)
        
def play_alarm(status, choice):
    pygame.mixer.init()
    pygame.mixer.music.load(choice) #plays any track as alarm if you give it the update
    pygame.mixer.music.play(loops=-1) #loops each time
    exit = input("input EXIT to stop alarm sound: ")
    match exit:
        case 'EXIT':
            sys.exit(0)


