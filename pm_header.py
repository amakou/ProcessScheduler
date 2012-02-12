'''
Created on 2012. 2. 12.

@author: Sandrock
'''
STACK_SIZE = 1024

class task_status:
    READY   = 0
    RUN     = 1
    YIELD   = 2
    SLEEP   = 3
    KILL    = 4

class task_info:
    def __init__(self):
        self.stack = range(STACK_SIZE)
        self.stack_pointer
        self.id
    
        self.status

class frame:
    def __init__(self):
        self.flags
        self.ebp
        self.edi
        self.esi
        self.edx
        self.ecx
        self.ebx
        self.eax
        self.retaddr
        self.retaddr2
        self.data
        
class schedule_handle:
    def __init__(self):
        self.child_num = 0
        self.running_task
        self.root_task
        
                
        
            
