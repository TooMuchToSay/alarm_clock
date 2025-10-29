import tkinter as tk
import time

def input_time(): #get time from the entry widget
    input_text = entry_widget.get()
    split_text = input_text.split(':')
    #print(split_text)
    hours = int(split_text[0])
    minutes = int(split_text[1])
    seconds = int(split_text[2])
    return [hours, minutes, seconds] #this has passed 


def timer_countdown(): #doing the timing
    list = input_time()
    end_time = time.asctime()
    end_time = end_time[11:19]
    end_time = end_time.split(':')
    end_hours = int(end_time[0])
    end_minutes = int(end_time[1])
    end_seconds = int(end_time[2]) #this is correct
    end_time = [end_hours, end_minutes, end_seconds]
    end_time = [list[0]+end_time[0], list[1]+end_time[1], list[2]+end_time[2]]
    print('end:',end_seconds)
    print('list[2]: ', list[2])
    print('end time 2: ',end_time[2])
    print('list[2] + end_time[2]: ', list[2]+end_time[2])
    if end_time[2] > 59:
        end_time[2] = end_time[2]%60
        end_time[1] += 1
    if end_time[1] > 59:
        end_time[1] = end_time[1]%60
        end_time[0] += 1
    if end_time[0] > 23:
        raise ValueError("sorry time can't be more than 24 hours")
    print(end_time)
#making the main window
root = tk.Tk()
root.title('Class Timer')
root.geometry('600x600') #set the window dimensions

#create the widget for the time input
entry_widget = tk.Entry(root, width= 25)
entry_widget.pack(pady=10)
entry_widget.insert(0, "H:M:S")

#button to start Timer
submit_button = tk.Button(root, text="Start Timer", command=timer_countdown)
submit_button.pack() #actually places the button in the box

#show time
time_text_box = tk.Text(root, height=10, width=65)
time_text_box.insert(tk.END, f"current time: {time.asctime()[11:19]} \n timer cannot go into next day(e.g. 24 hours!") #adds the text at the end
time_text_box.pack()

root.mainloop()
