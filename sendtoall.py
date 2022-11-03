#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os,sys,urllib,time,thread

global token
token="<insert token>"

global thn
thn=0
global sent
sent=0

def snd(chat_id,text):
	global token
	global sent
	
	try:
		cont=urllib.urlopen("https://api.telegram.org/bot"+token+"/sendMessage?chat_id="+str(chat_id)+"&text="+str(text))
		#cont=urllib.urlopen("https://api.telegram.org/bot"+token+"/sendMessage?chat_id="+str(chat_id)+'&text=Do you like the bot?\nHow many stars would you give it?&reply_markup={"inline_keyboard":[[{"text":"1 ⭐️","callback_data":"[\'review\',1]"},{"text":"2 ⭐️","callback_data":"[\'review\',2]"},{"text":"3 ⭐️","callback_data":"[\'review\',3]"}],[{"text":"4 ⭐️","callback_data":"[\'review\',4]"},{"text":"5 ⭐️","callback_data":"[\'review\',5]"}]]}')
		if "403" in cont:
			print cont
			print "{} blocked.".format(chat_id)
	except Exception as e:
		print("Error in urllib.urlopen: {}".format(e))

	sent+=1

def thsnd(subslist,text):
	global thn
	thn+=1
	
	for sub in subslist:
		#print "Sending to "+str(sub)+"..."
		snd(sub,text)
	
	thn-=1

subf=open("subs.txt","r")
subr=subf.read()
subf.close()
subs=[]
for line in subr.split("\n"):
	line=line.strip()
	if line!="":
		subs.append(line)

lsubs=len(subs)
print str(lsubs)+" subs"
text=raw_input("Message: ")
text=text.replace("\\n","\n")

nproc=int(os.popen("nproc").read())

# Moltiplicate process number
nproc*=2

subth=[]
for n in range(nproc):
		if n<nproc-1:
			subth.append(subs[n*lsubs/4:(n+1)*lsubs/4])
		else:
			subth.append(subs[n*lsubs/4:])

for sublist in subth:
	thread.start_new_thread(thsnd,(sublist,text))
time.sleep(.5)

oldsent=None
while thn>0:
	#print("Wait ending of {} processes.".format(thn))
	if sent!=oldsent:
		sys.stdout.write("Sent {}/{}\r".format(sent,lsubs))
		sys.stdout.flush()
	time.sleep(.5)

print("\nDone.")
