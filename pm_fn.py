'''
Created on 2012. 2. 12.

@author: Sandrock
'''
from pm_header import * 

def thread_init:
    global sh
    
    
        

def thread_create(callback_fn, context):
    task = task_info()
    f = frame()
    
    f.retaddr = callback_fn
    f.retaddr2 = thread_kill
    f.data = context
    
    task.stack_pointer = f.flags
    f.ebp = f.eax
    
    global sh, task_list
    task.id = sh.child_num
    sh.child_num += 1
    task.status = task_status.READY
    task_list.append(task)
    
    return task

    
     
    
    
    
    
    