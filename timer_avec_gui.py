import tkinter as tk
import time
import threading
from sys import argv

def get_current_time(): #grabs time and insert the current time during the gui
    current_time = time.asctime()
    current_time = current_time[11:19]
    current_time = current_time.split(":")
    text_widget.insert('1.0', f'current_time')

    #so far this will just print out the duration every second; still need to calculate the countdown
def print_c_time(): #this will handle printing the current time on a threading wait every second: proof of concept
    end_time = grab_input_time(time.asctime()[11:19])
    for i in range(100):
        check_times(end_time) #should do the math to remove the excess time over 60
        time_text_box.delete('1.0', tk.END)
        time_text_box.insert('1.0',f'{end_time}')
        #do the math FOR THE stuff
        time.sleep(1)

def grab_input_time(current_time): #if testing does calculations
    current_time = current_time.split(':')
    duration_time = entry_widget.get().split(':')
    end_time = []
    for i in range(0, len(duration_time)): #take each of the 3 entries in current_time and duration_time then create the duration attribute
        entry = int(current_time[i].strip()) + int(duration_time[i].strip())
        end_time.append(entry)
    #print(end_time, ' ', duration_time, ' ', current_time)
    return end_time

def create_thread():
    print_time_thread = threading.Thread(target=print_c_time)
    print_time_thread.start()

def check_times(time):
    count_up = []
    for i in range(0, len(time)):
        if time[i] > 59:
            new_time = time[i] - 60
            count_up.append(1)
            time[i] = time[i] - 60
    for i in range(0, len(count_up)):
        time[i] += count_up[i]
    return time


def logic_tests(duration,argv): #simple testing alrgorithm for basic logic instead of running the whole thing, [1] is the first passed argument to sysargv
    if len(argv) == 2:
        if argv[1] == 'test_duration':
            current_time = get_current_time
            grab_input_time(current_time, argv)
            
#making the main windoiw
root = tk.Tk()
root.title('Class Timer')
root.geometry('600x600') #set the window dimensions

#create the widget for the time input11
entry_widget = tk.Entry(root, width= 25)
entry_widget.pack(pady=10)
entry_widget.insert(0, "H:M:S")

#button to start Timer
submit_button = tk.Button(root, text="Start Timer", command=create_thread)
submit_button.pack() #actually places the button in the box

#show time
time_text_box = tk.Text(root, height=9, width=65)
time_text_box.insert(tk.END, f"current time: {time.asctime()[11:19]} \n timer cannot go into next day(e.g. 24 hours!") #adds the text at the end
time_text_box.pack()

#text box
text_widget = tk.Text(root, height=2, width=45)
#text_insert('1.0', lambda get_current_time(): f'{get_current_time}' )
#update time
#timer_thread = threading.Thread(target=timer_countdown)

#actually do the timer if the test argv hasn't been passed

root.mainloop()
