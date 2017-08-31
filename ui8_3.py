from flask import Flask, render_template, request,session, redirect, url_for, escape
app = Flask(__name__)
app.secret_key = "aezakmi"
import serial
import time
import subprocess, sys
import socket
import webbrowser
import serial.tools.list_ports
ip=[]
ip.append(socket.gethostbyname(socket.gethostname()))
print ip
global ser
# port=""
# ports = list(serial.tools.list_ports.comports())
# for p in ports:
	# if "Arduino" in p:
		# port=str(p[0])
# if len(port)==0:
	# p=ports[0]
	# port=p[0]
# print port
# global ser
# ser=serial.Serial(port,115200)
global c
c=0
global rob
rob=0
global inp
global s
global value
global f
f=0
global mo
mo=1
global x
x=1
global pa
pa=2
global pau
pau=1
global wait
wait=1
global plc
plc=0
global flag
flag=0
global stop
stop=1
global pause
pause=0
global start
start=0
webbrowser.open("http://"+ip[0]+":5000", new=1, autoraise=True)
#plc (1-live,0-offline)
#mo (1=Auto, 0=Manual)

@app.route('/mode1',methods = ['POST', 'GET']) # Path For Auto Mode 
def mode1(): # Function For Auto Mode
	global plc   
	global flag
	try:
		port=""
		ports = list(serial.tools.list_ports.comports())
		for p in ports:
			if "Arduino" in p:
				port=str(p[0])
		if len(port)==0:
			p=ports[0]
			port=p[0]
		print port
	except IndexError:
		plc=1
		flag=0
		return redirect(url_for('index'))
	else:
		plc=0
		if session['login']==1:
			print "mode1"
			global mo
			global x
			x=1
			mo=1
			print mo
			print "leaving mode1"
			return redirect(url_for('index'))
		else:
			redirect(url_for('login'))
		
@app.route('/mode0',methods = ['POST', 'GET'])
def mode0():
	global plc
	global flag
	try:
		port=""
		ports = list(serial.tools.list_ports.comports())
		for p in ports:
			if "Arduino" in p:
				port=str(p[0])
		if len(port)==0:
			p=ports[0]
			port=p[0]
		print port
	except IndexError:
		plc=1
		flag=0
		return redirect(url_for('index'))
	else:
		plc=0
		if session['login']==1:
			print "mode0"
			global x
			x=1
			global mo
			mo=0
			print mo
			print "leaving mode0"
			return redirect(url_for('index'))
		else:
			return redirect(url_for('login'))
		
@app.route('/',methods = ['POST', 'GET'])
def login():
	global plc
	global flag
	try:
		port=""
		ports = list(serial.tools.list_ports.comports())
		for p in ports:
			if "Arduino" in p:
				port=str(p[0])
		if len(port)==0:
			p=ports[0]
			port=p[0]
		print port
		#global ser
		#ser=serial.Serial(port,115200)
	except IndexError:
		plc=1
		flag=0
		return render_template("login.html",ip=ip)
	else:
		plc=0
		return render_template("login.html",ip=ip)
	
@app.route('/login',methods = ['POST', 'GET'])
def login1():
	global plc
	global flag
	try:
		port=""
		ports = list(serial.tools.list_ports.comports())
		for p in ports:
			if "Arduino" in p:
				port=str(p[0])
		if len(port)==0:
			p=ports[0]
			port=p[0]
		print port
		#global ser
		#ser=serial.Serial(port,115200)
	except IndexError:
		plc=1
		flag=0
		return redirect(url_for('index'))
	else:
		plc=0
		l=request.form
		if l['user']=="admin" and l['pass']=="god":
			session['login']=1
			return redirect(url_for('index'))
		else:
			session['login']=0
			return redirect(url_for('login'))
 
@app.route('/index',methods = ['POST', 'GET'])
def index():
	r=0
	global plc
	global flag
	try:
		port=""
		ports = list(serial.tools.list_ports.comports())
		for p in ports:
			if "Arduino" in p:
				port=str(p[0])
		if len(port)==0:
			p=ports[0]
			port=p[0]
		print port
	except IndexError:
		plc=1
		flag=0
		value=[" "," "," "," "]
		color=["red","red"]
		spec=["--","--"]
		coi=0
		robo=0
		return render_template('ui6_2.html',value=value,ip=ip,color=color,spec=spec,port=port,r=r,mo=mo,coi=coi,pa=pa,robo=robo,plc=plc)
		#return redirect(url_for('index'))
	else:
		if flag==0:
			global ser
			ser=serial.Serial(port,115200)
			flag=1
		plc=0
		if session['login']==1:
			global x
			if x==1:
				print "------------------------"
				#time.sleep(10)
				global wait
				incomming=ser.inWaiting()
				print incomming
				if incomming!=0:
					wait=1
				else:
					wait=0
				if wait==1:
					global inp
					global s
					i=list(ser.readline().strip('').split('|'))
					print i
					coil=i[0]
					robot=i[1]
					inp=i[2]
					print inp
					specifi=i[3]
					global spec
					if specifi!=" ":
						s=list(specifi.split(','))
						s1=s[0]
						s2=s[1]
						spec=[s1,s2]
					global value
					if inp!=" ":
						inp=list(inp.strip('').split(" "))
						print inp
						v1=""
						v2=""
						v3=""
						v4=""
						v1=inp[0]
						v2=inp[7]+" "+inp[8]
						v3=inp[18]+" "+inp[19]+" "+inp[20]
						v4=inp[30]+" "+ inp[31]
						value=[v1,v2,v3,v4]
					color1=""
					color2=""
					global coi
					coi=0
					if coil=="0":
						coi=0
						color1="red"
						#color2="green"
					if coil=="1":
						coi=1
						color1="green"
						#color2="red"	
					global robo
					robo=0
					if robot=="0":
						robo=0
						#color1="red"
						color2="red"
					if robot=="1":
						robo=1
						#color1="green"
						color2="green"
					global color
					if color1!="" or color2!="":
						color=[color1,color2]
					print color
					ser.flush()
					print mo
					print coi
					print robo
					print "leaving index"
					return render_template('ui6_2.html',value=value,ip=ip,color=color,spec=spec,port=port,r=r,mo=mo,coi=coi,pa=pa,robo=robo,plc=plc)
				else:
					try:
						wait=1
						return render_template('ui6_2.html',value=value,ip=ip,color=color,spec=spec,port=port,r=r,mo=mo,coi=coi,pa=pa,robo=robo,plc=plc)
					except:
						wait=0
						value=[" "," "," "," "]
						color=["red","red"]
						spec=["--","--"]
						coi=0
						robo=0
						return render_template('ui6_2.html',value=value,ip=ip,color=color,spec=spec,port=port,r=r,mo=mo,coi=coi,pa=pa,robo=robo,plc=plc)
			else:
				return render_template('ui6_2.html',value=value,ip=ip,color=color,spec=spec,port=port,r=r,mo=mo,coi=coi,pa=pa,robo=robo,plc=plc)
		else:
			return redirect(url_for('login'))
	
@app.route('/overide',methods=['POST','GET'])	
def overide():
	global plc
	global flag
	global stop
	try:
		port=""
		ports = list(serial.tools.list_ports.comports())
		for p in ports:
			if "Arduino" in p:
				port=str(p[0])
		if len(port)==0:
			p=ports[0]
			port=p[0]
		print port
	except IndexError:
		plc=1
		flag=0
		return redirect(url_for('index'))
	else:
		plc=0
		if session['login']==1:
			print "override"
			global x
			x=1
			r=0
			global f
			if f==0:
				global wait
				if wait==1:
					result=request.form
					global value
					value=[]
					value.append(result['line1'])
					value.append(result['line2'])
					value.append(result['line3'])
					value.append(result['line4'])
					v1=value[0]
					v2=value[1]
					v3=value[2]
					v4=value[3]
					value2=value
					output=v1+"       "+v2+"          "+v3+"          "+v4
					output=str(output)
					output=output+"\n"
					if stop==0:
						if flag==1:
							print "sending to arduino"
							print output
							ser.write(output)
					if mo==1:
						return redirect(url_for('index'))
					else:
						return render_template('ui6_2.html',value=value,ip=ip,color=color,spec=spec,port=port,r=r,mo=mo,coi=coi,pa=pa,robo=robo,plc=plc)
				else:
					return redirect(url_for('index'))
				f=1
			else:
				f=0
		else:
			return redirect(url_for('login'))

@app.route('/pause',methods=['POST','GET'])	
def pause1():
	global plc
	global flag
	try:
		port=""
		ports = list(serial.tools.list_ports.comports())
		for p in ports:
			if "Arduino" in p:
				port=str(p[0])
		if len(port)==0:
			p=ports[0]
			port=p[0]
		print port
	except IndexError:
		flag=0
		plc=1
		return redirect(url_for('index'))
	else:
		plc=0
		if session['login']==1:
			global x
			x=0
			print "pause function"
			r=0
			global robo
			global pau
			global pa
			global c
			global rob
			global color
			global coi
			global stop
			if pau==1:
					if pa==1:
						ser.write("2,0")
						print "resume"
						color1="green"
						color[1]=color1
						pa=0
					elif pa==2:
						ser.write("1,0")
						print "start"
						color1="green"
						color[1]=color1
						stop=0
						pa=0
					elif pa==0:
						ser.write("3,0")
						print "pause"
						color1="red"
						color[1]=color1
						pa=1
					global inp
					global s
					i=list(ser.readline().strip('').split('|'))
					print i
					coil=i[0]
					robot=i[1]
					inp=i[2]
					print inp
					specifi=i[3]
					global spec
					if specifi!=" ":
						s=list(specifi.split(','))
						s1=s[0]
						s2=s[1]
						spec=[s1,s2]
					global value
					if inp!=" ":
						inp=list(inp.strip('').split(" "))
						print inp
						v1=""
						v2=""
						v3=""
						v4=""
						v1=inp[0]
						v2=inp[7]+" "+inp[8]
						v3=inp[18]+" "+inp[19]+" "+inp[20]
						v4=inp[30]+" "+ inp[31]
						value=[v1,v2,v3,v4]
					color1=""
					color2=""
					global coi
					coi=0
					if coil=="0":
						coi=0
						color1="red"
						#color2="green"
					if coil=="1":
						coi=1
						color1="green"
						#color2="red"	
					global robo
					robo=0
					if robot=="0":
						robo=0
						#color1="red"
						color2="red"
					if robot=="1":
						robo=1
						#color1="green"
						color2="green"
					if color1!="" or color2!="":
						color=[color1,color2]
					print color
					ser.flush()
					print mo
					print coi
					print robo
					print "leaving pause"
					return redirect(url_for('index'))
			elif pau==0:
					if pa==1:
						ser.write("2,0")
						print "resume"
						pa=0
					elif pa==2:
						ser.write("1,0")
						print "start"
						stop=0
						pa=0
					elif pa==0:
						ser.write("3,0")
						print "pause"
						pa=1
					i=list(ser.readline().strip('').split('|'))
					print i
					coil=i[0]
					robot=i[1]
					inp=i[2]
					print inp
					specifi=i[3]
					if specifi!=" ":
						s=list(specifi.split(','))
						s1=s[0]
						s2=s[1]
						spec=[s1,s2]
					if inp!=" ":
						inp=list(inp.strip('').split(" "))
						print inp
						v1=""
						v2=""
						v3=""
						v4=""
						v1=inp[0]
						v2=inp[7]+" "+inp[8]
						v3=inp[18]+" "+inp[19]+" "+inp[20]
						v4=inp[30]+" "+ inp[31]
						value=[v1,v2,v3,v4]
					color1=""
					color2=""
					coi=0
					if coil=="0":
						coi=0
						color1="red"
						#color2="green"
					if coil=="1":
						coi=1
						color1="green"
						#color2="red"	
					robo=0
					if robot=="0":
						robo=0
						#color1="red"
						color2="red"
					if robot=="1":
						robo=1
						#color1="green"
						color2="green"
					if color1!="" or color2!="":
						color=[color1,color2]
					print color
					ser.flush()
					print mo
					print coi
					print robo
					print "leaving pause"
					return redirect(url_for('index'))
		else:
			return redirect(url_for('login'))

@app.route('/next',methods=['POST','GET'])	
def next():
	global plc
	global flag
	try:
		port=""
		ports = list(serial.tools.list_ports.comports())
		for p in ports:
			if "Arduino" in p:
				port=str(p[0])
		if len(port)==0:
			p=ports[0]
			port=p[0]
		print port
	except IndexError:
		plc=1
		flag=0
		return redirect(url_for('index'))
	else:
		plc=0
		if session['login']==1:
			global x
			x=0
			r=0
			ser.write("4,0")
			print "next"
			return redirect(url_for('index'))
		else:
			return redirect(url_for('login'))
			
@app.route('/stop',methods=['POST','GET'])	
def stop():
	global plc
	global flag
	global stop
	stop=1
	try:
		port=""
		ports = list(serial.tools.list_ports.comports())
		for p in ports:
			if "Arduino" in p:
				port=str(p[0])
		if len(port)==0:
			p=ports[0]
			port=p[0]
		print port
	except IndexError:
		plc=1
		flag=0
		return redirect(url_for('index'))
	else:
		plc=0
		if session['login']==1:
			global x
			global robo
			global pau
			global pa
			global c
			global rob
			global color
			global coi
			x=0
			r=0
			ser.write("0,0")
			print "stop"
			global pa
			global pau
			pa=2
			pau=1
			global inp
			global s
			i=list(ser.readline().strip('').split('|'))
			print i
			coil=i[0]
			robot=i[1]
			inp=i[2]
			print inp
			specifi=i[3]
			global spec
			if specifi!=" ":
				s=list(specifi.split(','))
				s1=s[0]
				s2=s[1]
				spec=[s1,s2]
			global value
			if inp!=" ":
				inp=list(inp.strip('').split(" "))
				print inp
				v1=""
				v2=""
				v3=""
				v4=""
				v1=inp[0]
				v2=inp[7]+" "+inp[8]
				v3=inp[18]+" "+inp[19]+" "+inp[20]
				v4=inp[30]+" "+ inp[31]
				value=[v1,v2,v3,v4]
			color1=""
			color2=""
			global coi
			coi=0
			if coil=="0":
				coi=0
				color1="red"
				#color2="green"
			if coil=="1":
				coi=1
				color1="green"
				#color2="red"	
			global robo
			robo=0
			if robot=="0":
				robo=0
				#color1="red"
				color2="red"
			if robot=="1":
				robo=1
				#color1="green"
				color2="green"
			global color
			if color1!="" or color2!="":
				color=[color1,color2]
			print color
			ser.flush()
			print mo
			print coi
			print robo
			#color=["red","red"]
			#ser.flush()
			return redirect(url_for('index'))
		else:
			return redirect(url_for('login'))
		
if __name__ == '__main__':
   app.run(host='0.0.0.0')