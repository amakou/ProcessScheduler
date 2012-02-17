# -*- coding: cp949 -*-
'''
Created on 2012. 2. 12.

@author: Sandrock
'''
import signal, os, time
from itertools import cycle
from multiprocessing import Process, Lock

STACK_SIZE = 1024

class cpu_info:
	def __init__(self):
		self.frame 	= None
		self.esp	= 0

class proc_status:
	READY   = 0
	RUN	 	= 1
	YIELD   = 2
	SLEEP   = 3
	KILL	= 4

class proc_info:
	def __init__(self):
		self.proc		= None
		self.status		= None
		self.priority	= 0

		# no use
		self.stack 		= range(STACK_SIZE)
		self.frame		= None
		self.sp			= 0    

class frame:
	def __init__(self, cpu):
		self.flags		= 0
		self.ebp 		= 0
		self.edi		= 0
		self.esi		= 0
		self.edx		= 0
		self.ecx		= 0
		self.ebx		= 0
		self.eax		= 0
		self.retaddr	= 0
		self.retaddr2	= 0
		self.data		= None
	
		self.cpu		= cpu
		
class process_manager:
	def __init__(self, cpu):
		self.proc_num 		= 0
		self.running_pi 	= None
		self.root_pi 		= None
		
		self.global_sp 		= None
		self.frame_save		= None
		self.sp_save_before	= None
		self.sp_save_after	= None
		
		self.pi_list = []
		self.cpu = cpu
	
		self.lock = Lock()

	def timer(self, interval):
		print "timer"
		while 1:
			time.sleep(interval)
#			self.lock.acquire()
			os.kill(os.getppid(), signal.SIGUSR1)
#			self.lock.release()

	def proc_init(self):
		signal.signal(signal.SIGUSR1, self.proc_switch)
		p = Process(target=self.timer, args=(5, ))
		p.start()

		pi 				= proc_info()
		pi.proc 		= p
		self.root_pi 	= pi

	def proc_create(self, fn, context):
		p = Process(target=fn, args=(self.lock, ))
		p.start()

		pi  		= proc_info()
		pi.proc 	= p
		pi.status	= proc_status.READY
		
		self.proc_num += 1
		self.proc_insert(pi)

		print pi.proc.name, " is created : ", pi.proc.pid

		return p

	def proc_switch(self, test, test2):

#		self.lock.acquire()	# interrupt disable

#		self.frame_save 		= self.cpu.frame
#		self.sp_save_before		= self.cpu.esp
#		self.running_proc.sp	= self.sp_save_before

		if self.running_pi is not None:
			os.kill(self.running_pi.proc.pid, signal.SIGSTOP)
			if self.running_pi.proc.is_alive():
				self.proc_insert(self.running_pi)
			print self.running_pi.proc.pid, " stopped"

	#	try:
	#		self.lock.release()
	#	except ValueError:
	#		pass
			
		self.scheduler();
	
#		self.sp_save_after	= self.running_proc.sp
#		self.cpu.esp		= self.sp_save_after
#		self.cpu.frame		= self.frame_save

		os.kill(self.running_pi.proc.pid, signal.SIGCONT)
		print "%s (%d) is reasumed" % (self.running_pi.proc.name, self.running_pi.proc.pid)

#		self.lock.release()	# interrupt enable

	def proc_kill(self):
		print "proc_kill"
		pi = self.running_pi
		pi.status = proc_status.KILL
		self.proc_switch();	
	
	def scheduler(self):
		pi = self.running_pi

		if pi is None:
			self.select_next_proc()
			return
		if pi.status == proc_status.RUN or pi.status == proc_status.SLEEP:
			pass
		elif pi.status == proc_status.KILL:
			proc_delete(proc)
			scheduler()
		elif pi.status == proc_status.YIELD or pi.status == proc_status.READY:
			pi.status = proc_status.RUN
			
		self.select_next_proc()

	def select_next_proc(self):
		print [ x.proc.pid for x in self.pi_list ]
		self.running_pi = self.pi_list.pop(0)
#		self.pi_list.append(self.running_pi)

	def proc_insert(self, new_pi):
		os.kill(new_pi.proc.pid, signal.SIGSTOP) # proc stop

		self.pi_list.append(new_pi)


	def proc_delete(proc):
		self.proc_num -= 1
		self.pi_list.remove(proc)
