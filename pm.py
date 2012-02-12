'''
Created on 2012. 2. 11.

@author: Sandrock
'''
import threading, time
from pm_header import *
from pm_fn import *

def thread_one():
    i=0
    while 1:
        i += 1
        print "TASK1 : %5d\n" % i
        time.sleep(1)
        if i == 15:
            break

def thread_two():
    i=500
    while 1:
        i += 10
        print "\t\t\tTASK2 : %5d\n" % i
        time.sleep(1)
        if i == 600:
            break
        
def thread_three():
    i=1000
    while 1:
        i += 1
        print "\t\t\t\t\t\tTASK3 : %5d\n" % i
        time.sleep(2)
        if i == 1005:
            break    


        
if __name__ == '__main__':
    sh = schedule_handle()  
    threads = []
    
    th = threading.Thread(target=thread_one, args=())
    th.start()
    threads.append(th)
    th = threading.Thread(target=thread_two, args=())
    th.start()
    threads.append(th)
    th = threading.Thread(target=thread_three, args=())
    th.start()
    threads.append(th)
    
    # thread_wait in c
    for th in threads:
        th.join()       
    
        