import threading
import time

#create your functions for threading
def count_every_2():
    for i in range(200):
        print('thread 1: ', i)
        time.sleep(2)

def count_every_3():
    for i in range(200):
        print('thread 2: ', i)
        time.sleep(3)

#create thread object and run commands
first_thread = threading.Thread(target=count_every_2)
second_thread = threading.Thread(target=count_every_3)

#start the threading
first_thread.start()
second_thread.start()
