'''
Created on 2012. 2. 12.

@author: Sandrock
'''

import signal, os, time
from itertools import cycle, islice
from pm_header import * 
from copy import *

def thread_init():
    thread_create(parent_task, None)

def thread_create(callback_fn, context):
    task = task_info()
    f = frame()
    
    f.retaddr = callback_fn
    #f.retaddr2 = thread_kill
    f.data = context
    
    task.stack_pointer = f.flags
    f.ebp = f.eax
    
    global sh, task_list
    task.id = sh.child_num
    task.status = task_status.READY
    task.frame = f
    
    sh.child_num += 1    
    task_list.append(task)
    
    return task

def task_switch():
    global sh, cpu
    sh.frame_save = cpu.frame # push ~  
    sh.sp_save_before = cpu.esp # movl %esp, spsave        
    sh.running_task.sp = sh.sp_save_before; # sh -> task

    scheduler();    
    
    sh.sp_save_after = sh.running_task.sp
    cpu.esp = sh.sp_save_after # movl sptmp, %esp
    cpu.frame = sh.frame_save
     
def scheduler():
    global sh
    task = sh.running_task
    
    # task���°� TASK_RUN�̳� TASK_SLEEP�̸� ���õ�
    if task.status == task_status.RUN or task.status == task_status.SLEEP:
        break
    # task���°� TASK_KILL�̸� delete�ϰ�, swiching�Լ� �ٽ� ȣ��
    elif task.status == task_status.KILL:
        task_delete(task)
        scheduler()
        break
    # task���°� TASK_YIELD�̸� ���¸� TASK_RUN���� �ٲٰ� ���õ�    
    elif task.status == task_status.YIELD:
        task.status = task_status.RUN
        break
    # task���°� TASK_READY�̸� ���׸� TASK_RUN���� �ٲٰ� ���õ�
    elif task.status == task_status.READY:
        task.status = task_status.RUN
        break
    # ���� ���μ��� 
    task_next()

def task_kill():
    # task ���¸� TASK_KILL�� ���� ��, yield
    task = sh.running_task    
    task.status = task_status.KILL
    task_switch()

# child thread�� ���̻� ���������� thread_switch
def parent_task():    
    global sh
    
    # signal handler�� thread_switch() ���
    signal.signal(signal.SIGABRT, task_switch)
    
    pid = os.fork()
        
    if pid == 0: 
        while 1:
            time.sleep(1)
            os.kill(os.getppid(), signal.SIGABRT)
    else:
        while 1:
            # child_task�� 1�� ������ ��, ��, parent_task�� ������ ��
            if sh.child_num == 1:
                os.kill(pid, signal.SIGINT)
                break
            
# linkedlist�� ���ο� taskinfo ����
def task_insert(new_task):
    global sh
    
    if sh.root_task is None:
        sh.root_task = new_task
        sh.running_task = new_task
    else:
        sh.task_list.append(new_task)

def roundrobin(*iterables):
    "roundrobin('ABC', 'D', 'EF') --> A D E B F C"
    # Recipe credited to George Sakkis
    pending = len(iterables)
    nexts = cycle(iter(it).next for it in iterables)
    while pending:
        try:
            for next_task in nexts:
                yield next()
        except StopIteration:
            pending -= 1
            nexts = cycle(islice(nexts, pending))

def task_next():
    global sh
    
    if sh.running_task is None:
        sh.running_task = sh.root_task
    else:
        sh.running_task = roundrobin(sh.task_list)

def task_delete(task):
    global sh
    
    if sh.root_task == task:
        sh.root_task = None
        sh.running_task = None
        sh.child_num = 0
    else:
        task_list.remove(task)   


    
    
    