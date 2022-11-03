#!/usr/bin/env python
import time,os
try:
	import thread
except:
	import _thread as thread

global runningThreads
runningThreads=0

def exe(txt):
	print(txt)
	time.sleep(.5)

def thr(thId,l):
	global runningThreads
	runningThreads+=1
	
	for i in l:
		exe(str(thId)+" "+str(i))

	runningThreads-=1

def main():
	global runningThreads
	
	ths=range(1000)
	nproc=int(os.popen("nproc").read())
	npt=int(len(ths)/nproc)
	t=[]
	for p in range(nproc):
		t.append(ths[p:npt+p])
	for i,p in enumerate(t):
		thread.start_new_thread(thr,(i,p))

	time.sleep(.5)
	while runningThreads>0:
		#print("{} running threads".format(runningThreads),end="\r")
		time.sleep(.5)
	
	return 0

if __name__=="__main__":
	exit(main())
