# -*- coding: cp949 -*-
'''
Created on 2012. 2. 12.

@author: Sandrock
'''

import signal, os, time
from itertools import cycle, islice
from pm_header import * 

# child thread가 더이상 없을때까지 thread_switch
def parent_proc():	
	global sh
	
	# signal handler로 thread_switch() 등록
	signal.signal(signal.SIGABRT, task_switch)
	
	pid = os.fork()
		
	if pid == 0: 
		while 1:
			time.sleep(1)
			os.kill(os.getppid(), signal.SIGABRT)
	else:
		while 1:
			# child_task가 1개 남았을 때, 즉, parent_task만 남았을 때
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
