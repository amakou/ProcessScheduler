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
        self.sp
        self.frame
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
        self.running_task = None
        self.root_task = None
        
        self.global_sp
        self.frame_save
        self.sp_save_before
        self.sp_save_after
        
        self.task_list = []
        
class cpu_info:
    def __init(self):
        self.frame
        self.esp
                        
        
            
