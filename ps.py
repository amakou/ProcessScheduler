#!/usr/local/bin/python
# -*- coding: cp949 -*-
'''
Created on 2012. 2. 11.

@author: Sandrock
'''
import signal, os, threading, time
from pm_header import *

def parent_proc():
	signal.signal(signal.SIGUSR1, task_switch)

	pid = os.fork()

	if pid == 0:	 # child 
		print "child created"
		while 1:
			time.sleep(1)
			os.kill(os.getppid(), signal.SIGUSR1)
	else:			# parent
		while 1:
			if pm.proc_num == 1:
				os.kill(pid, signal.SIGINT)

def proc_one(l):
	i=0
	while i < 15:
		i += 1
		time.sleep(1)
		#l.acquire()
		print "TASK1 : %5d\n" % i
		#l.release()
	

def proc_two(l):
	i=500
	while i < 600:
		i += 10
		time.sleep(1)
		#l.acquire()
		print "\t\t\tTASK2 : %5d\n" % i
		#l.release()

def proc_three(l):
	i=1000
	while i < 1010:
		i += 1
		time.sleep(1)
		#l.acquire()
		print "\t\t\t\t\t\tTASK3 : %5d\n" % i
		#l.release()

if __name__ == '__main__':
	cpu = cpu_info()
	pm = process_manager(cpu)
	pm.proc_init()

	plist = [ proc_one, proc_two, proc_three ]
	pid_list = []
#	print "process start!!!!!!!!!!!!!!!"
	for x in plist:
#		if os.getpid()== pm.pid:
		pid_list.append(pm.proc_create(x, None))
#		pm.proc_create(x, None).join()

	for y in pid_list:
		y.join()
	pm.root_pi.proc.join()
