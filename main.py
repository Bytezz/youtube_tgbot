#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os,sys,urllib,requests,re,time,datetime,ast,random,traceback,thread,ctypes,hashlib
from lxml import etree
from PIL import Image

os.chdir(os.path.dirname(os.path.realpath(__file__)))

# https://github.com/bytezz/xml2dict/
def x2d(file):
	xmlf=open(file,"r")
	xml=xmlf.read()
	xmlf.close()
	di={}
	xml=xml.replace("    ","").replace("	","").replace("\n","").replace("\t","")
	xmlr=xml.split("<")
	da=["di"]
	for e in xmlr:
		if not e.startswith("?") and e!="":
			if not e.startswith("/"):
				n=e[:[pos for pos,char in enumerate(e) if char==">"][-1]]
				if len(e)>[pos for pos,char in enumerate(e) if char==">"][-1]+1:
					tmp=e[[pos for pos,char in enumerate(e) if char==">"][-1]+1:len(e)]
					w=da[0]
					for d in da:
						if d!=da[0]:
							w=w+"['"+d+"']"
					if tmp.lower()=="true":
						exec("%s[n]=int(1)"%w)
					elif tmp.lower()=="false":
						exec("%s[n]=int(0)"%w)
					elif tmp.isdigit():
						exec("%s[n]=int(tmp)"%w)
					elif tmp.startswith("-") and tmp[1:].isdigit():
						exec("%s[n]=int(tmp)"%w)
					elif "." in tmp and tmp.split(".")[-1].isdigit():
						if tmp.split(".")[0].isdigit() and tmp.split(".")[-1].isdigit():
							exec("%s[n]=float(tmp)"%w)
						elif tmp.split(".")[0].startswith("-") and tmp.split(".")[0][1:].isdigit() and tmp.split(".")[-1].isdigit():
							exec("%s[n]=float(tmp)"%w)
						else:
							exec("%s[n]=tmp"%w)
					else:
						exec("%s[n]=tmp"%w)
				else:
					w=da[0]
					for d in da:
						if d!=da[0]:
							w=w+"['"+d+"']"
					tmp={}
					exec("%s[n]=tmp"%w)
					da.append(n)
			else:
				if e[1:[pos for pos,char in enumerate(e) if char==">"][-1]] in da:
					da.remove(e[1:[pos for pos,char in enumerate(e) if char==">"][-1]])
	return di
def d2x(di):
	global xml;xml='<?xml version="1.0" encoding="utf-8"?>'
	def innerdict(dic):
		global xml;global t
		for e in dic:
			xml+="\n"+"\t"*t+"<"+e+">"
			t+=1
			if type(dic[e])==type([]):
				xml+=str(dic[e])
			elif type(dic[e])==type({}):
				innerdict(dic[e])
				xml+="\n"+"\t"*(t-1)
			else:
				xml+=str(dic[e])
			t-=1
			xml+="</"+e+">"
	global t;t=0
	for e in di:
		xml+="\n"+"\t"*t+"<"+e+">"
		t+=1
		if type(di[e])==type([]):
			xml+=str(di[e])
		elif type(di[e])==type({}):
			innerdict(di[e])
			xml+="\n"+"\t"*(t-1)
		else:
			xml+=str(di[e])
		t-=1
		xml+="</"+e+">"
	return xml
def checkSubstr(string, substrings):
	for substring in substrings:
		if substring in string:
			return [True, substring]
	return [False, ""]
def readurl(url):
	page=urllib.urlopen(url)
	content=page.read()
	page.close()
	return content
def readurlAdv(url):
	h={'User-Agent':'Mozilla/5.0 (X11; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'}
	r=requests.get(url,headers=h).content
	return r
def epoch():
	return (datetime.datetime.now()-datetime.datetime(1970,1,1)).total_seconds()
def dellast(chat_id):
	global lastsendid
	lastsendid[chat_id].pop(0)
	if len(lastsendid[chat_id])==0:
		del lastsendid[chat_id]
def search(q,site="youtube"):
	try:
		result="https://www.youtube.com/watch?v="+re.findall(r'{"webCommandMetadata":{"url":"/watch\?v=(.*?)"',readurl("https://www.youtube.com/results?q="+str(q)))[0]
		return result
	except Exception as e:
		log(str(e))
		return ""
def snd(chat_id,text,filename="",vid="",songname="",artist="",lowq="",site="youtube",deletable=False,ulang="en"):
	global token
	global lastsendid
	if text=="<!MusiC!>" and filename!="":
		#os.rename(filename,songname+".mp3")
		#filename=songname+".mp3"
		if site=="soundcloud":
			urllib.urlretrieve(re.findall(r'<meta property="og:image" content="(.*?)">',readurl("https://soundcloud.com/"+vid))[0],filename+"default.jpg")
		elif site=="instagram":
			imgurl=readurlAdv("https://www.instagram.com/p/"+vid)
			imgurl=re.findall(r'<meta property="og:image" content="(.*?)" />',imgurl)[0]
			urllib.urlretrieve(imgurl,filename+"default.jpg")
		elif site=="facebook":
			if not "/" in vid:
				imgurl=readurlAdv("https://fb.watch/"+vid)
			else:
				imgurl=readurlAdv(vid)
			imgurl=re.findall(r'<meta property="og:image" content="(.*?)" />',imgurl)[0]
			urllib.urlretrieve(imgurl,filename+"default.jpg")
		else:
			urllib.urlretrieve("https://img.youtube.com/vi/"+vid+"/maxresdefault.jpg",filename+"default.jpg")
			# check image if its blank
			if (hashlib.md5(readf(filename+"default.jpg","rb"))).hexdigest().lower()=="e2ddfee11ae7edcae257da47f3a78a70":
				urllib.urlretrieve("https://img.youtube.com/vi/"+vid+"/hqdefault.jpg",filename+"default.jpg")
		img=Image.open(filename+"default.jpg")
		x,y=img.size
		#size=max(x,y)
		size=min(x,y)
		#nimg=Image.new("RGBA",(size,size),(0,0,0,0))
		#nimg.paste(img,(int((size-x)/2),int((size-y)/2)))
		#nimg.save("default.jpg")
		w=(x-size)/2
		h=(y-size)/2
		nimg=img.crop((w,h,x-w,y-h))
		nimg.save(filename+"rdefault.jpg")
		nimg=nimg.resize((320,320),Image.ANTIALIAS)
		nimg.save(filename+"default.jpg")
		if lowq=="low":
			nimg.save(filename+"rdefault.jpg")
		#os.system('eyeD3 --title "'+songname.replace('"','\\"')+'" --artist "'+artist.replace('"','\\"')+'" --add-image "'+filename+'rdefault.jpg:FRONT_COVER" --add-comment "t.me/utubmp3_bot" "'+filename+'"')
		os.system('eyeD3 --title {} --artist {} --add-image {} --add-comment "t.me/utubmp3_bot" {}'.format( repr(songname), repr(artist), repr(filename+'rdefault.jpg:FRONT_COVER'), repr(filename) ))
		f={"audio":open(filename,"rb"),"thumb":open(filename+"default.jpg","rb")}
		try:
			requests.post("https://api.telegram.org/bot"+token+"/sendAudio?chat_id="+chat_id+"&title="+songname+"&performer="+artist,files=f)
			readurl("https://api.telegram.org/bot"+token+"/deleteMessage?chat_id="+chat_id+"&message_id="+lastsendid[chat_id][0])
			dellast(chat_id)
			os.remove(filename)
			os.remove(filename+"default.jpg")
			os.remove(filename+"rdefault.jpg")
		except:
			log(str(traceback.print_exc()))
			try:
				readurl("https://api.telegram.org/bot"+token+"/deleteMessage?chat_id="+chat_id+"&message_id="+lastsendid[chat_id][0])
				readurl("https://api.telegram.org/bot"+token+"/sendMessage?chat_id="+chat_id+"&text="+translate("errUpload",ulang))
			except:
				pass
			dellast(chat_id)
			os.remove(filename)
			os.remove(filename+"default.jpg")
			os.remove(filename+"rdefault.jpg")
	elif text=="<!VideO!>" and filename!="":
		if site=="soundcloud":
			urllib.urlretrieve(re.findall(r'<meta property="og:image" content="(.*?)">',readurl("https://soundcloud.com/"+vid))[0],filename+"default.jpg")
		elif site=="instagram":
			imgurl=readurlAdv("https://www.instagram.com/p/"+vid)
			imgurl=re.findall(r'<meta property="og:image" content="(.*?)" />',imgurl)[0]
			urllib.urlretrieve(imgurl,filename+"default.jpg")
		elif site=="facebook":
			if not "/" in vid:
				imgurl=readurlAdv("https://fb.watch/"+vid)
			else:
				imgurl=readurlAdv(vid)
			imgurl=re.findall(r'<meta property="og:image" content="(.*?)" />',imgurl)[0]
			urllib.urlretrieve(imgurl,filename+"default.jpg")
		else:
			urllib.urlretrieve("https://img.youtube.com/vi/"+vid+"/maxresdefault.jpg",filename+"default.jpg")
			# check image if its blank
			if (hashlib.md5(readf(filename+"default.jpg","rb"))).hexdigest().lower()=="e2ddfee11ae7edcae257da47f3a78a70":
				urllib.urlretrieve("https://img.youtube.com/vi/"+vid+"/hqdefault.jpg",filename+"default.jpg")
		img=Image.open(filename+"default.jpg")
		f={"video":open(filename,"rb"),"thumb":open(filename+"default.jpg","rb")}
		try:
			requests.post("https://api.telegram.org/bot"+token+"/sendVideo?chat_id="+chat_id+"&caption="+songname,files=f)
			readurl("https://api.telegram.org/bot"+token+"/deleteMessage?chat_id="+chat_id+"&message_id="+lastsendid[chat_id][0])
			dellast(chat_id)
			os.remove(filename)
			os.remove(filename+"default.jpg")
		except:
			log(str(traceback.print_exc()))
			try:
				readurl("https://api.telegram.org/bot"+token+"/deleteMessage?chat_id="+chat_id+"&message_id="+lastsendid[chat_id][0])
				readurl("https://api.telegram.org/bot"+token+"/sendMessage?chat_id="+chat_id+"&text="+translate("errUpload",ulang))
			except:
				pass
			dellast(chat_id)
			os.remove(filename)
			os.remove(filename+"default.jpg")
	elif text=="<!PiC!>":
		if site=="soundcloud":
			urllib.urlretrieve(re.findall(r'<meta property="og:image" content="(.*?)">',readurl("https://soundcloud.com/"+vid))[0],filename+"default.jpg")
		elif site=="instagram":
			imgurl=readurlAdv("https://www.instagram.com/p/"+vid)
			imgurl=re.findall(r'<meta property="og:image" content="(.*?)" />',imgurl)[0]
			urllib.urlretrieve(imgurl,filename+"default.jpg")
		elif site=="facebook":
			if not "/" in vid:
				imgurl=readurlAdv("https://fb.watch/"+vid)
			else:
				imgurl=readurlAdv(vid)
			imgurl=re.findall(r'<meta property="og:image" content="(.*?)" />',imgurl)[0]
			urllib.urlretrieve(imgurl,filename+"default.jpg")
		else:
			urllib.urlretrieve("https://img.youtube.com/vi/"+vid+"/maxresdefault.jpg",filename+"default.jpg")
			# check image if its blank
			if (hashlib.md5(readf(filename+"default.jpg","rb"))).hexdigest().lower()=="e2ddfee11ae7edcae257da47f3a78a70":
				urllib.urlretrieve("https://img.youtube.com/vi/"+vid+"/hqdefault.jpg",filename+"default.jpg")
		f={"document":open(filename+"default.jpg","rb")}
		try:
			requests.post("https://api.telegram.org/bot"+token+"/sendDocument?chat_id="+chat_id+"&caption="+songname,files=f)
			readurl("https://api.telegram.org/bot"+token+"/deleteMessage?chat_id="+chat_id+"&message_id="+lastsendid[chat_id][0])
			dellast(chat_id)
			os.remove(filename+"default.jpg")
		except:
			log(str(traceback.print_exc()))
			try:
				readurl("https://api.telegram.org/bot"+token+"/deleteMessage?chat_id="+chat_id+"&message_id="+lastsendid[chat_id][0])
				readurl("https://api.telegram.org/bot"+token+"/sendMessage?chat_id="+chat_id+"&text="+translate("errUpload",ulang))
			except:
				pass
			dellast(chat_id)
			os.remove(filename+"default.jpg")
	else:
		if text!="":
			if deletable:
				if not chat_id in lastsendid:
					lastsendid[chat_id]=[]
				try:
					lastsendid[chat_id].append(str(ast.literal_eval(readurl("https://api.telegram.org/bot"+token+"/sendMessage?chat_id="+chat_id+"&text="+str(text)).replace("\n","").replace("true","True").replace("false","False"))["result"]["message_id"]))
				except:
					log(str(traceback.print_exc()))
					errorcont=readurl("https://api.telegram.org/bot"+token+"/sendMessage?chat_id="+chat_id+"&text="+str(text))
					if '"error_code":403' in errorcont:
						print "User blocked the bot."
						rmuser(chat_id)
					else:
						print errorcont
			else:
				readurl("https://api.telegram.org/bot"+token+"/sendMessage?chat_id="+chat_id+"&text="+str(text))
def get_medium(url):
	o=os.popen("youtube-dl -F "+url).read()
	for i,line in enumerate(o.split("\n")):
		if "format code" in line:
			break
	formats=o.split("\n")[i+1:]
	for k,x in enumerate(formats):
		d=0
		formats[k]=x.split(" ")
		for i,y in enumerate(x.split(" ")):
			if y=="":
				formats[k].pop(i-d)
				d+=1
	d=0
	for i,f in enumerate(formats):
		if f==[]:
			formats.pop(i-d)
			d+=1
	return formats[len(formats)/2][0]
def checkurl(url):
	invidious_clients=["invidious.snopyta.org", "invidious-us.kavin.rocks", "invidious-jp.kavin.rocks", "invidio.xamh.de", "vid.mint.lgbt", "vid.puffyan.us", "invidious.namazso.eu", "inv.riverside.rocks", "yewtu.be", "yt.artemislena.eu", "youtube.076.ne.jp", "invidious.kavin.rocks", "invidious.osi.kr", "yt.didw.to"]

	isvideo=False
	ispic=False
	lowq=""
	medq=False
	site=""
	q=url
	if " " in url:
		while url.split(" ")[0]=="":
			url=" ".join(url.split(" ")[1:])
		while url.split(" ")[-1]=="":
			url=" ".join(url.split(" ")[:-1])
		if len(url.split(" "))>1:
			#if "youtu" in url.split(" ")[0] or "soundcloud" in url.split(" ")[0]:
			if len(url.split(" "))>1:
				if url.split(" ")[1]=="-v":
					isvideo=True
					url=url.replace(" -v","")
				elif url.split(" ")[1]=="-i":
				    ispic=True
				    url=url.replace(" -i","")
				if "-low" in url.split(" "):
					lowq="low"
					url=url.replace(" -low","")
				if "-med" in url.split(" "):
					lowq="med"
					url=url.replace(" -med","")
	if not url.startswith("http"):
		url="http://"+url
	if "https://" in url:
		rawurl=url.replace("https://","")
	else:
		rawurl=url.replace("http://","")
	if "." in rawurl:
		if len(rawurl.split(".")[0])>0 and len(rawurl.split(".")[1])>0:
			try:
				#r=urllib.urlopen(url).read()
				#h={'User-Agent':'Mozilla/5.0 (X11; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'}
				#r=requests.get(url,headers=h).content
				r='"movie_player"'
				if "youtube.com" in url or "youtu.be" in url or checkSubstr(url,invidious_clients)[0]:
					is_invidious = checkSubstr(url,invidious_clients)
					if is_invidious[0]:
						url = url.replace(is_invidious[1], "youtube.com")

					site="youtube"
					if "http://youtu.be" in url or "https://youtu.be" in url:
						url="https://youtube.com/watch?v="+url.split("youtu.be/")[1]
					if "/watch?v=" in url:
						if len(url.split("/watch?v=")[1])>0:
							#if not "Questo video non è disponibile." in r and '"movie_player"' in r:
							if '"movie_player"' in r:
								#open("file.html","w+").write(r)
								for var in url.split("?")[1].split("&"):
									if var.startswith("v="):
										vid=var.replace("v=","")
								url="https://www.youtube.com/watch?v="+vid
								video=etree.HTML(readurl(url))
								#with open("test.txt","w+") as fo:
								#	fo.write(readurl(url))
								#tit="".join(video.xpath("//span[@id='eow-title']/@title")).encode('utf-8')
								tit=re.findall(r'<meta name="title" content="(.*?)"/>',etree.tostring(video).replace("\n","").replace("  ",""))[0].encode("utf-8")
								#artist=re.findall(r'>(.*?)<',re.findall(r'<div class="yt-user-info">(.*?)</div>',etree.tostring(video).replace("\n","").replace("  ",""))[0])[0].encode('utf-8')
								artist=re.findall(r'"name": "(.*?)"',etree.tostring(video))[0].encode("utf-8")
								if isvideo:
									return ["Ok",tit,url,artist,"video",lowq,site]
								elif ispic:
								    return ["Ok",tit,url,artist,"pic",lowq,site]
								else:
									return ["Ok",tit,url,artist,"",lowq,site]
							else:
								return "err5"
						else:
							return "err4"
					else:
						return "err4"
				elif "soundcloud.com" in url:
					site="soundcloud"
					if len(url.split("soundcloud.com"))>1:
						if url.split("soundcloud.com")[1]!="":
							if url.split("soundcloud.com")[1].startswith("/"):
								if len(url.split("soundcloud.com")[1][1:].split("/"))>1:
									if url.split("soundcloud.com")[1][1:].split("/")[1]!="":
										artist=url.split("soundcloud.com")[1][1:].split("/")[0]
										tit=url.split("soundcloud.com")[1][1:].split("/")[1]
										url="https://soundcloud.com/"+artist+"/"+tit
										content=readurl(url)
										if '<meta property="og:image" content="' in content:
											artist=re.findall(r'<meta itemprop="name" content="(.*?)"',content)[0]
											tit=re.findall(r'<meta property="og:title" content="(.*?)">',content)[0]
											if ispic:
												return ["Ok",tit,url,artist,"pic",lowq,site]
											else:
												return ["Ok",tit,url,artist,"",lowq,site]
										else:
											return "err7"
									else:
										return "err6"
								else:
									return "err6"
							else:
								return "err6"
						else:
							return "err6"
					else:
						return "err6"
				elif "instagram.com" in url:
					site="instagram"
					if "instagram.com/p/" in url and len(url.split("instagram.com/p/")[1])>0:
						vid=url.split("instagram.com/p/")[1]
						url="https://www.instagram.com/p/"+vid
						content=readurlAdv(url)
						with open("/tmp/instpg.html","w+") as testlp:
							testlp.write(content)
							testlp.close()
						try:
							artist=re.findall(r'"alternateName":"(.*?)"',content)[0]
							tit="{} from instagram".format(artist)
						except:
							tit="From instagram"
							artist="Unknown"
						if isvideo:
							return ["Ok",tit,url,artist,"video",lowq,site]
						elif ispic:
							return ["Ok",tit,url,artist,"pic",lowq,site]
						else:
							return ["Ok",tit,url,artist,"",lowq,site]
					else:
						return "err3"
				elif "fb.watch" in url:
					site="facebook"
					if ("facebook.com/" in url) or ("fb.watch/" in url and len(url.split("fb.watch/")[1])>0):
						if "fb.watch/" in url:
							vid=url.split("fb.watch/")[1]
							url="https://fb.watch/"+vid
						content=readurlAdv(url)
						try:
							artist=re.findall(r'<title id="pageTitle">(.*?)</title>',content)[0]
							tit="{} from facebook".format(artist)
						except:
							tit="from facebook"
							artist="Unknown"
						if isvideo:
							return ["Ok",tit,url,artist,"video",lowq,site]
						elif ispic:
							return ["Ok",tit,url,artist,"pic",lowq,site]
						else:
							return ["Ok",tit,url,artist,"",lowq,site]
					else:
						return "err3"
				else:
					return "err3"
			except:
				traceback.print_exc()
				return "err2"
		else:
			s=search(q)
			if s!="":
				if "-v" in q.split(" "):
					s+=" -v"
				elif "-i" in q.split(" "):
					s+=" -i"
				if "-low" in q.split(" "):
					s+=" -low"
				return checkurl(s)
			else:
				return "err1"
	else:
		s=search(q)
		if s!="":
			if "-v" in q.split(" "):
				s+=" -v"
			elif "-i" in q.split(" "):
				s+=" -i"
			if "-low" in q.split(" "):
				s+=" -low"
			return checkurl(s)
		else:
			return "err1"
def readf(p,t="r"):
	with open(p,t) as f:
		c=f.read()
		f.close()
	return c
def log(t):
	with open("log.log","a") as log:
		log.write(str(datetime.datetime.now())+" - "+str(t)+"\n")
		log.close()
def adduser(uid):
	subf=open("subs.txt","r")
	subs=subf.read()
	subf.close()
	subs=subs.split("\n")
	if not uid in subs:
		#subs.append(uid)
		subf=open("subs.txt","a")
		#subf.write("\n".join(subs))
		subf.write(str(uid)+"\n")
		subf.close()
def rmuser(uid):
	subf=open("subs.txt","r")
	subs=subf.read()
	subf.close()
	subs=subs.split("\n")
	if uid in subs:
		for i,sub in enumerate(subs):
			if sub==uid:
				subs.pop(i)
		subf=open("subs.txt","w+")
		subf.write("\n".join(subs)+"\n")
		subf.close()
def smsg(text):
	with open("msgs.txt","a") as msgs:
		msgs.write(str(text)+"\n")
		msgs.close()

global reviews
try:
	with open("reviews.txt","r") as reviewsF:
		cont=reviewsF.read()
		if cont != "":
			reviews = ast.literal_eval(cont)
		else:
			reviews = {}
		reviewsF.close()
except:
	reviews = {}
def addReview(user,review):
	global reviews
	reviews[user] = int(review)
	with open("reviews.txt","w+") as reviewsF:
		reviewsF.write(str(reviews))
		reviewsF.close()

def getReviewRank():
	rank = 0.0
	try:
		with open("reviews.txt","r") as reviewsF:
			reviews =  ast.literal_eval(reviewsF.read()).values()
			reviewsN = len(reviews)
			for review in reviews:
				rank += review
			rank = rank/reviewsN
			rank = str(rank).split(".")
			rank = rank[0]+"."+rank[1][:3]
			return "{} reviews,\n{} ⭐️".format(reviewsN, rank)
	except:
		return "Still no review."

def translate(text,ulang):
	global lang
	if text in lang[ulang]:
		o=lang[ulang][text]
	elif text in lang["en"]:
		o=lang["en"][text]
	else:
		o=text
	return o.replace("\\n","\n")
def elaborate(d):
	global token
	global lastsendid
	global lui
	global lang
	c=""
	text=""
	lui=d["update_id"]
	fileid=(str(epoch())+str(random.randint(1000,9999))).replace(".","")
	if "message" in d:
		chat_id=str(d["message"]["chat"]["id"])
		if "username" in d["message"]["from"]:
			user="@"+d["message"]["from"]["username"]
		elif "first_name" in d["message"]["from"]:
			user=d["message"]["from"]["first_name"]
		else:
			user=str(d["message"]["from"]["id"])
		try:
			if chat_id!=admin_id:
				adduser(chat_id)
				print user+" used me."
				log(chat_id+" used me.")
		except Exception as e:
			print "Error: "+str(e)
			log(str(e))
		if "from" in d["message"]:
			if "language_code" in d["message"]["from"]:
				if d["message"]["from"]["language_code"] in lang:
					ulang=d["message"]["from"]["language_code"]
				else:
					if "-" in d["message"]["from"]["language_code"]:
						if d["message"]["from"]["language_code"].split("-")[0] in lang:
							ulang=d["message"]["from"]["language_code"].split("-")[0]
						else:
							ulang="en"
							log("Language '"+d["message"]["from"]["language_code"]+"' not supported.")
					else:
						ulang="en"
						log("Language '"+d["message"]["from"]["language_code"]+"' not supported.")
			else:
				ulang="en"
		else:
			ulang="en"
		if "text" in d["message"]:
			if d["message"]["text"]!="":
				c=d["message"]["text"]
				# Huge logging, useful for finding a bug or a vulnerability.
				## Keep disabled if not useful. (Can lead to privacy issues)
				if huge_logging and chat_id!=admin_id:
					with open("history.txt","a+") as hist:
						hist.write("{} --- {} --- {}\n".format(str(datetime.datetime.now()),chat_id,c))
						hist.close()
				# End huge logging
				if c=="/start":
					text="strt"
				elif c=="loggol" and chat_id==admin_id:
					with open("log.log","r") as logf:
						snd(chat_id,"\n".join(logf.read().split("\n")[-50:]))
						logf.close()
				elif c=="subus" and chat_id==admin_id:
					with open("subs.txt","r") as subs:
						snd(chat_id,len(subs.read().split("\n")))
						subs.close()
				elif c.split(" ")[0].lower()=="/help":
					#text="""If the bot doesn't reply, just wait.\nSupported links: YouTube and SoundCloud.\nThis bot reply to your links with an mp3 file (with song name, artist and cover) of the content that you share. Add "-v" after link to receive mp4 file, or add "-i" to receive an uncompressed jpg. Add at the end "-low" to get the worst quality or "-med" to get the medium quality.\n\nFrom Italy\nwith love."""
					with open("utubhelp.txt","r") as f:
						text=f.read()
						f.close()
				elif c.split(" ")[0].lower()=="/msg":
					if c.lower()=="/msg" or c.lower()=="/msg ":
						text="/msg - Send a message to the bot's creator.\nYou have to write a message, like:\n/msg Sample text."
					else:
						if chat_id==admin_id:
							try:
								snd(c.split(" ")[1]," ".join(c.split(" ")[2:]))
							except:
								pass
						else:
							msgtxt=user+" - "+str(chat_id)+" - "+str(d["message"]["message_id"])+":\n"+(" ".join(c.split(" ")[1:]))
							smsg(msgtxt+"\n########")
							log(chat_id+" sent a message.")
							urllib.urlopen("https://api.telegram.org/bot"+token+"/sendMessage?chat_id="+admin_id+"&text="+msgtxt)
							text="Your message has been sent to the bot's creator."
				elif c.split(" ")[0].lower()=="/rank":
					snd(chat_id, getReviewRank())
					readurl("https://api.telegram.org/bot"+token+"/sendMessage?chat_id="+chat_id+'&text=Do you like the bot?\nHow many stars would you give it?&reply_markup={"inline_keyboard":[[{"text":"1 ⭐️","callback_data":"[\'review\',1]"},{"text":"2 ⭐️","callback_data":"[\'review\',2]"},{"text":"3 ⭐️","callback_data":"[\'review\',3]"}],[{"text":"4 ⭐️","callback_data":"[\'review\',4]"},{"text":"5 ⭐️","callback_data":"[\'review\',5]"}]]}')
				else:
					ck=checkurl(c)
					if type(ck)==type([]):
						tit=ck[1].replace("/","")
						artist=ck[3]
						isvideo=False
						ispic=False
						if ck[4]=="video":
						    isvideo=True
						elif ck[4]=="pic":
						    ispic=True
						lowq=ck[5]
						site=ck[6]
						if site=="soundcloud":
							vid=ck[2].split("soundcloud.com/")[1]
						elif site=="instagram":
							vid=ck[2].split("instagram.com/p/")[1]
							ck[2]="--playlist-item 0 "+ck[2]
						elif site=="facebook":
							if "fb.watch/" in ck[2]:
								vid=ck[2].split("fb.watch/")[1]
							else:
								vid=ck[2]
						else:
							for var in ck[2].split("?")[1].split("&"):
								if var.startswith("v="):
									vid=var.replace("v=","")
						if isvideo:
							snd(chat_id,translate("dwnv",ulang),deletable=True)
							if lowq=="low":
								if site=="youtube" or site=="instagram":
									oc=os.system("youtube-dl -o "+fileid+".mp4 -f worstvideo "+ck[2])
									oc=os.system("youtube-dl -o "+fileid+".mp4 -f worstvideo "+ck[2])
								else:
									oc=os.system("youtube-dl -o "+fileid+".mp4 -f worst "+ck[2])
							elif lowq=="med":
								oc=os.system("youtube-dl -o "+fileid+".mp4 -f "+get_medium(ck[2])+" "+ck[2])
							else:
								oc=os.system("youtube-dl -o "+fileid+".mp4 -f mp4 "+ck[2])
							
							if oc==0:
								try:
									snd(chat_id,"<!VideO!>",fileid+".mp4",vid,tit,artist,lowq,site,ulang=ulang)
								except:
									snd(chat_id,"Error. Maybe pic it's expired.")
							elif site=="instagram" and oc!=0:
								readurl("https://api.telegram.org/bot"+token+"/deleteMessage?chat_id="+chat_id+"&message_id="+lastsendid[chat_id][0])
								dellast(chat_id)
								snd(chat_id,translate("err8",ulang))
							else:
								readurl("https://api.telegram.org/bot"+token+"/deleteMessage?chat_id="+chat_id+"&message_id="+lastsendid[chat_id][0])
								dellast(chat_id)
								snd(chat_id,"Error downloading.")
						elif ispic:
						    snd(chat_id,translate("dwnp",ulang),deletable=True)
						    try:
						    	snd(chat_id,"<!PiC!>",fileid,vid,tit,artist,lowq,site,ulang=ulang)
						    except:
								snd(chat_id,"Error. Maybe pic it's expired.")
						else:
							snd(chat_id,translate("dwnm",ulang),deletable=True)
							if lowq=="low":
								oc=os.system("youtube-dl -o '"+fileid+".%(ext)s' -f worstaudio --extract-audio --audio-quality 9 --audio-format mp3 "+ck[2])
							else:
								oc=os.system("youtube-dl -o '"+fileid+".%(ext)s' --extract-audio --audio-format mp3 "+ck[2])
							
							if oc==0:
								try:
									snd(chat_id,"<!MusiC!>",fileid+".mp3",vid,tit,artist,lowq,site,ulang=ulang)
								except:
									snd(chat_id,"Error. Maybe pic it's expired.")
							elif site=="instagram" and oc!=0:
								readurl("https://api.telegram.org/bot"+token+"/deleteMessage?chat_id="+chat_id+"&message_id="+lastsendid[chat_id][0])
								dellast(chat_id)
								snd(chat_id,translate("err8",ulang))
							else:
								readurl("https://api.telegram.org/bot"+token+"/deleteMessage?chat_id="+chat_id+"&message_id="+lastsendid[chat_id][0])
								dellast(chat_id)
								snd(chat_id,"Error downloading.")
						os.system("youtube-dl --rm-cache-dir")
					else:
						text=ck
		else:
			text="err1"
		if text!="":
			text=translate(text,ulang)
			snd(chat_id,text)
	elif "callback_query" in d:
		data = d["callback_query"]["data"]
		chat_id = str(d["callback_query"]["message"]["chat"]["id"])

		data = ast.literal_eval(data)
		if data[0] == "review":
			addReview(chat_id, data[1])
			snd(chat_id, "Thanks for the feedback.")
			log(chat_id+" ranked me.")
	elif "inline_query" in d:
		if "username" in d["inline_query"]["from"]:
			user="@"+d["inline_query"]["from"]["username"]
		elif "first_name" in d["inline_query"]["from"]:
			user=d["inline_query"]["from"]["first_name"]
		else:
			user=str(d["inline_query"]["from"]["id"])
		iid=d["inline_query"]["id"]
		c=d["inline_query"]["query"]
		print "inline_query: "+c
		laq="https://api.telegram.org/bot"+token+"/answerInlineQuery?id="+iid+"&results=type=article,title=Test,message_text=Test."
		print laq
		print readurl(laq)

c=""
global token
global lastsendid
global lui
global admin_id
global huge_logging
global lang
token="<insert token>"
lang=x2d("lang.xml")
lastsendid={}
lui=0
admin_id="133918178"
huge_logging=False
#stat=urllib.urlopen("https://api.telegram.org/bot"+token+"/getUpdates").read()
stat='{"ok":true,"result":[]}'
running=True
while running:
	time.sleep(.5)
	try:
		ns=readurl("https://api.telegram.org/bot"+token+"/getUpdates?offset="+str(lui+1))
		if ns!=stat:
			da=ns.replace("\n","")
			da=da.replace('false','False').replace("true","True")
			#stat=ns
			da=ast.literal_eval(da)
			if "result" in da:
				for d in da["result"]:
					thread.start_new_thread(elaborate,(d,))
	except Exception as e:
		print "Error: "+str(e)
		log(str(e))
		#snd(admin_id,"Error:"+str(e).replace("\n",""))
	#except:
	#	e=str(traceback.print_exc())
	#	print e
	#	snd(admin_id,"Error:"+str(e).replace("\n",""))
