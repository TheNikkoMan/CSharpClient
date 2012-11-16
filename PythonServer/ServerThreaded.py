#Python Server DGram
from __future__ import division
from threading import Thread
import socket, os, time, string, sys, traceback

FPSpt=time.gmtime()[5]
FPSi=0
FPS=0
TT=time.gmtime()[5]
Conn=0
CThreads={}
PStatus=""
Error=""
BError=""
MsgSep="z_*"
LogStr=""

ip="localhost"
port=27000

# default_colors = win32con.get_text_attr()
# default_bg = default_colors & 0x0070
# win32con.set_text_attr(win32con.FOREGROUND_GREY | default_bg)

# def FPSloop():
# 	global FPSi, FPSpt, FPS
# 	if FPSpt!=time.gmtime()[5]:
# 		FPSpt=time.gmtime()[5]
# 		FPS=FPSi
# 		FPSi=0
# 	FPSi=FPSi+1
# def TTStart():
# 	global TT
# 	TT=time.clock()
# def TTEnd():
# 	return time.clock()-TT
# 	#Shit here
# def #(Status=PStatus):
# 	global PStatus
# 	if Status!="":
# 		PStatus=Status
# 	os.system("title "+PStatus+" "+str(FPS)+"FPS "+str(Conn)+"Conn")

def Logg(arg,arg2):
 	global LogStr
# 	if arg2==0: #Info
# 		win32con.set_text_attr(win32con.FOREGROUND_GREY | default_bg)
# 	elif arg2==1: #attention
# 		win32con.set_text_attr(win32con.FOREGROUND_CYAN | default_bg | win32con.FOREGROUND_INTENSITY)
# 		#print("Client")
# 	elif arg2==3: #usershit
# 		win32con.set_text_attr(win32con.FOREGROUND_GREEN | default_bg)
# 	elif arg2==2: #warning
# 		win32con.set_text_attr(win32con.FOREGROUND_YELLOW | default_bg | win32con.FOREGROUND_INTENSITY)
# 	elif arg2==4: #error
# 		win32con.set_text_attr(win32con.FOREGROUND_RED | default_bg | win32con.FOREGROUND_INTENSITY)
# 	elif arg2==5: #critical
# 		win32con.set_text_attr(win32con.FOREGROUND_RED | win32con.BACKGROUND_GREY | win32con.FOREGROUND_INTENSITY | win32con.BACKGROUND_INTENSITY)
# 		print("====================================")
# 		print("==Critical Error!===================")
# 	##(str(arg2))
	time.sleep(0.05)

	foo=str(time.localtime()[3])
	bar=str(time.localtime()[4])
	fob=str(time.localtime()[5])
	preq="0"*(2-len(foo))+foo+":"+"0"*(2-len(bar))+bar+":"+"0"*(2-len(fob))+fob+" "
	if arg2==3:
		print(arg)
	elif arg2==5:
		bar=str(sys.exc_info()[0])[18:]
		foo=bar[:(len(bar)-2)]
		print("=="+preq+"=========================")
		print("====================================")
		print("=="+arg+"="*(34-len(arg)))
		print(foo)
		print(sys.exc_info()[1])
		print("\n==Traceback=========================")
		print(traceback.format_exc())
		#LogStr=LogStr+"\n"+"====================================\n"+preq+arg
	else:
		print(preq+arg)
		LogStr=LogStr+"\n"+preq+arg

# 	win32con.set_text_attr(win32con.FOREGROUND_GREEN | default_bg)


server_socket=None


#________________________________________________________________________________________________________________
#SERVERTHREAD: UID 0
class server(Thread):
	def __init__(self, ip=ip, port=port):
		Thread.__init__(self)
		self.setName(ip+":"+str(port))
		self.alive=True
		self.CList={}
		self.CTLock=False

	def broadcast(self, Str):
		for x in CThreads:
			CThreads[x].send(Str)

	def broadcastMSG(self, From, UID, Mesg):
		for x in CThreads:
			if not str(x)==str(UID):
				CThreads[x].MESG(str(UID),Mesg)

	def UpdateCList(self):
		self.CList={}
		for x in CThreads:
			self.CList[x]={}
			self.CList[x]["UID"]=CThreads[x].UID
			self.CList[x]["Uname"]=CThreads[x].Uname

	def UpdateCThreads(self):
		if self.CTLock==False:
			self.CTLock=True
			DeadThreads={}
			for x in CThreads:
				if not CThreads[x].isAlive():
					DeadThreads[x]=CThreads[x]
					Logg("Removing dead thread: "+str(x),0)
					self.broadcast("DCONN"+MsgSep+str(CThreads[x].UID)+MsgSep+CThreads[x].state)
			for x in DeadThreads:
				del CThreads[x]
			self.UpdateCList()
			self.CTLock=False

	def Crash(self):
		crash=10+"Fuckthis"

	def run(self):
		global Conn, CThreads, Error, LastConn
		Logg(str(self),0)
		while self.alive:
			try:
				#("Accepting Connections...")
				channel, details = server_socket.accept()
				Logg("Client connected "+ str(details),0)
				Conn+=1
				CThreads[Conn]=client(channel,Conn)
				CThreads[Conn].state="Starting"
				CThreads[Conn].start()
				CThreads[Conn].setName(details)
				self.UpdateCThreads()
				LastConn=Conn
				if self.alive==False:
					print("I should be dead.. :(")

			except socket.timeout:
				pass

			except socket.error, e:
				SError=e
				Logg(str(e),4)
				self.alive=False
		if self.alive==False:
			Logg("Server stopped..",0)

#________________________________________________________________________________________________________________
#CLIENTTHREAD: UID1-inf
class client(Thread):
	def __init__ (self, channel,UID):
		Thread.__init__(self)
		self.channel=channel
		self.alive=True
		self.UID=UID
		self.Uname="N/A"
		self.state="START"

	def send(self, msg):
		try:
			self.channel.send(msg)
		except socket.error, e:
			lasterror=e
			Logg("Failed to send message, client: "+str(self.UID)+" lost connection?",0)
			self.state="FAILEDSEND"
			self.alive=False

	def ping(self):
		try:
			self.channel.send("PING")
			self.pong=None
			timeout=time.clock()+10
			while self.pong==None:
				if time.clock()>timeout:
					self.pong=False
				pass
			if self.pong==True:
				return time.clock()-(timeout-10)
			else:
				return False
		except socket.error, e:
			Logg(e,1)
			Error=e
			return False

	def MESG(self, uid, msg):
		#From argument removed, can be done clientside instead
		self.send("MESG"+MsgSep+str(uid)+MsgSep+msg)

	def run(self):
		global Error, BError
		try:
			self.send("UID"+MsgSep+str(self.UID))
			#self.send("CList"+MsgSep+str(ServerListener.CThreadsToString()))
		except socket.error, e:
			error=e
			Logg("Failed to initialize UID "+str(self.UID),1)
			self.state="INITFAIL"
			self.alive=False
		
		self.clock=time.clock()
		while self.alive:
			try:
				data=self.channel.recv ( 200 )
				datasplit=string.split(data,MsgSep)
				command=string.split(data,MsgSep)[0]
				BError=data
				if not data:
					Logg("Client disconnected: "+str(self.channel.getsockname()),0)
					self.alive=False
					self.state="DCONN"
				else:
					if command=="MESG":
						Logg(str(self.UID)+":"+datasplit[1],1)
						self.channel.send("RECV"+MsgSep)
						ServerListener.broadcastMSG("USER",str(self.UID),datasplit[1])
					elif command=="UNAME":
						#print(datasplit)
						Logg("User: "+self.Uname+": "+str(self.UID)+"changed name to: "+datasplit[1],0)
						self.Uname=datasplit[1]
						ServerListener.UpdateCList()
						ServerListener.broadcast("UNAME"+str(self.UID)+self.Uname)
					elif command=="crash":
						a=a+1
					elif command=="PING":
						Logg("Ping recived from "+str(self.UID),1)
						self.pong=True
					else:
						Logg("UNDEFINED RESPONSE FROM UID"+str(self.UID)+": "+data,1)

					# if time.clock()>(self.clock+5):
					# 	PingThread=Tempty()
					# 	def PingThread.ping(self, UID):
					# 		self.ptime=CThreads[UID].ping()
					# 		if self.ptime==False:
					# 			print("Lost connection to UID "+str(UID))
					# 			CThreads[UID].alive=False
					# 			CThreads[UID].state="LOSTCONN"
					# 			ServerListener.UpdateCThreads()
					# 	def PingThread.run(self):
					# 		PingThread.ping(self.UID)
					# 	PingThread.start()
			except socket.error, e:
				#Error=e
				pass
			except IndexError, e:
				Logg("Bad behaviour from: "+str(self.UID)+" : "+str(self.getName()),1)
			except:
				Logg("Client "+str(self.UID)+" crashed: "+str(sys.exc_info()[0])[18:],4)
				ServerListener.UpdateCThreads()
				self.tback=traceback.format_exc()
				self.alive=False
		if self.alive==False:
			ServerListener.UpdateCThreads()
			pass

#________________________________________________________________________________________________________________
#EMPTYTHREAD: 
class Tempty(Thread):
	def __init__(self):
		Thread.__init__(self)
		self.alive=True

	def run(self):
		pass

def Bootup():
	global server_socket, ServerListener, ip, port
#	#("Starting up...")
	server_socket = socket.socket ( socket.AF_INET, socket.SOCK_STREAM )
	server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	server_socket.bind ( ( ip, port ) )
	server_socket.settimeout(1)
	server_socket.listen(5)
#	#("Listening...")
	ServerListener=server(ip, port)
	ServerListener.start()
Bootup()

Malive=True
while Malive:
	arg=raw_input()
	ServerListener.UpdateCThreads()
	#_____________________________________________________________________________________________________________________
	#Commands
	try:
		ComPar=string.split(arg, " ")
		Command=ComPar[0]
		
		if Command=="ls":
			Logg("UID TYPE      IP          PORT    STATE   TID",3)
			for x in CThreads:
				Logg(str(x)+" "*(3-len(str(x)))+":"+str(CThreads[x]),3)

		elif Command=="killinactive":
			Logg("Killing inactive client threads",3)
			ServerListener.UpdateCThreads()

		elif Command=="clist":
			Logg("CLI:    Info:",3)
			for x in ServerListener.CList:
				Logg(ServerListener.CList[x],3)
		
		elif Command=="clistupd":
			Logg("Updating Client List...",3)
			ServerListener.UpdateCList()

		elif Command=="crashtest":
			if ComPar[1]=="index":
				a=ComPar[20]
			elif ComPar[1]=="value":
				a=10+"fuckme"
			elif ComPar[1]=="type":
				False=True
			elif ComPar[1]=="1":
				a=a+1

		elif Command=="restart":
			#("Shutting down...")
			for x in CThreads:
				Logg("Disconnecting Client: "+CThreads[x].getName(),3)
				CThreads[x].channel.close()
				CThreads[x].alive=False
			Logg("Killing server manager",3)
			#ServerManager.alive=False
			Logg("Killing server thread: "+ServerListener.getName(),3)
			ServerListener.alive=False
			server_socket.close()
			#Startup process
			Logg("Booting up..",3)
			Bootup()
			Logg("Reboot complete",1)

		elif Command=="send":
			try:
				if int(ComPar[1]) in CThreads:
					foo=""
					for x in ComPar:
						if not x=="send" and x!=ComPar[1]:
							foo=foo+x+" "
					CThreads[int(ComPar[1])].send(foo)
			except ValueError, e:
				Error=e
				Logg("send must be used with an userid",3)

		elif Command=="broadcast":
			try:
				foo=""
				for x in ComPar:
					if not x=="broadcast":
						foo=foo+x+" "
				ServerListener.broadcast(foo)
			except ValueError, e:
				Error=e
				Logg("broadcast must be used with shit",3)

		elif Command=="ping":
			try:
				if int(ComPar[1]) in CThreads:
					Logg("Pinging: UID"+ComPar[1]+" | "+CThreads[int(ComPar[1])].getName(),3)
					fooping=CThreads[int(ComPar[1])].ping()
					if fooping:
						Logg("Pinging successful, time taken: "+str(fooping),3)
					else:
						Logg("Client refused to respond to ping in time",3)
				else:
					Logg("User ID: "+ComPar[1]+" does not exsist",3)
			except ValueError, e:
				Error=e
				Logg("Ping must be used with an user id (UID)",3)

		elif Command=="exit":
			#("Shutting down...")
			for x in CThreads:
				Logg("Disconnecting Client: "+CThreads[x].getName(),3)
				CThreads[x].channel.close()
				CThreads[x].alive=False
			Logg("Killing server manager",3)
			#ServerManager.alive=False
			Logg("Killing server thread: "+ServerListener.getName(),3)
			ServerListener.alive=False
			server_socket.close()
			Logg("Killing mainloop",3)
			os.system("PAUSE")
			Malive=False

		elif Command=="lasterror":
			Logg(Error,3)

		elif Command=="berror":
			Logg(BError,3)

		elif Command=="traceback":
			Logg(traceback.format_exc(),3)
		
		elif Command=="kick":
			try:
				if int(ComPar[1]) in CThreads:
					Logg("Kicking: UID"+ComPar[1]+" | "+CThreads[int(ComPar[1])].getName(),3)
					reason=""
					for x in ComPar:
						if not (x=="kick" or x==str(ComPar[1])):
							reason=reason+x+" "
					ServerListener.broadcast("KICK"+MsgSep+ComPar[1]+MsgSep+reason)
					CThreads[int(ComPar[1])].alive=False
					del CThreads[int(ComPar[1])]
					ServerListener.UpdateCList()
				else:
					Logg("User ID: "+ComPar[1]+" does not exsist",3)
			except ValueError, e:
				Error=e
				Logg("Kick must be used with an user id (UID)",3)
	
		elif Command=="say":
			stri=""
			for x in ComPar:
				if not x=="say":
					stri=stri+x+" "
			ServerListener.broadcastMSG("SERVER",0,stri)

		elif Command=="clear":
			os.system("CLS")

		elif Command=="":
			#\Random scribble
			#Once there comes a time.. Where you hear the certain call, and the wolves, come, together as one.
			#/Random scribble
			pass

		else:
			#Lua Extension for commands here:
			Logg("Command *"+Command+"* not found",3)
	except IndexError, e:
		Logg("Command *"+Command+"* requires "+str("N/A")+" arguments, "+str(len(ComPar)-1)+" given",3)
	except ValueError, e:
		Logg("An exception occured: ValueError. Probleary you typed a number where a text were required or the opposite. Type lasterror for more information",3)
		Error=e
	except TypeError, e:
		Logg("An exception occured: TypeError. Probleary you typed a number where a text were required or the opposite. Type lasterror for more information",3)
		Error=e
	except:
		Logg("Mainloop",5)