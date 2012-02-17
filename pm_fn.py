# -*- coding: cp949 -*-
'''
Created on 2012. 2. 12.

@author: Sandrock
'''

import signal, os, time
from itertools import cycle, islice
from pm_header import * 

# child thread�� ���̻� ���������� thread_switch
def parent_proc():	
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
