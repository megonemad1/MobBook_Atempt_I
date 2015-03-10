from flask import Flask,render_template,request,redirect,make_response
import sqlite3
import hashlib
from datetime import datetime
from MobBook import app
from MobBook import Secret
import json
from collections import deque

DataBaseFilePath="Anthology.db"
DebugString =""
AlowDBUG=True
RecentList= deque([])
_webname="SnipiTree"
def RepresentsInt(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False
def GetNode(NodeId):
	global DataBaseFilePath
	conn = sqlite3.connect(DataBaseFilePath)
	c = conn.cursor()		
	c.execute('''CREATE TABLE IF NOT EXISTS ActI (Id INTEGER PRIMARY KEY AUTOINCREMENT,Parent int,Rating int,Body text,Hits int)''')
	c.execute('SELECT * FROM ActI WHERE Id=?', (NodeId,))
	LstNode =c.fetchone()
	c.close();	
	return {'Id':LstNode[0],'Parent':LstNode[1],'Rating':LstNode[2],'Body':LstNode[3],'Hits':LstNode[4]}
def GetNodeChildren(NodeId):			
	global DataBaseFilePath
	conn = sqlite3.connect(DataBaseFilePath)
	c = conn.cursor()	
	c.execute('''CREATE TABLE IF NOT EXISTS ActI (Id INTEGER PRIMARY KEY AUTOINCREMENT,Parent int,Rating int,Body text,Hits int)''')
	c.execute('SELECT * FROM ActI WHERE Parent=? ORDER BY Rating DESC', (NodeId,))
	LstChild_list = c.fetchall()
	c.close();	
	Child_list =[]
	for C in LstChild_list:
		Child_list.append({'Id':C[0],'Parent':C[1],'Rating':C[2],'Body':C[3],'Hits':C[4]})
	return Child_list
def SubGetDuplicate(Node):
	global DataBaseFilePath
	conn = sqlite3.connect(DataBaseFilePath)
	c = conn.cursor()
	c.execute('SELECT * FROM ActI WHERE Parent=? AND Body=? ORDER BY Rating DESC', (Node['Parent'],Node['Body']))
	Vals = c.fetchall()
	c.close()
	if len(Vals)==0:
		return None
	else:
		match=Vals[0]
		return {'Id':match[0],'Parent':match[1],'Rating':match[2],'Body':match[3],'Hits':match[4]}
def InsertNodeIntoDB(Node):
	if (Node['Body'] !=""):
		dupe = SubGetDuplicate(Node)
		if dupe!=None:
			return dupe
		global DataBaseFilePath
		conn = sqlite3.connect(DataBaseFilePath)
		c = conn.cursor()
		c.execute("INSERT INTO ActI(Parent,Rating,Body,Hits) VALUES (?,0,?,0)",(Node['Parent'],Node['Body'],))			
		NextNodeId=c.lastrowid
		c.close()
		conn.commit()
		RNode= {'Id': NextNodeId,'Parent':Node['Parent'],'Rating':0, 'Body':Node['Body'], 'Hits':0}
		RecentList.append(RNode)
		if len(RecentList)>=10:
			RecentList.popleft()
		return RNode	
	return None
def IDSafeNode(NodeId=None):
	if (NodeId==None or not RepresentsInt(NodeId)):
		return None
	else:
		Node=GetNode(NodeId)		
		if (Node==None):
			return None
		return Node
def CreateHash(IP = None):
	if (IP != None):
		Hash =hashlib.md5()
		Hash.update(IP.encode('utf-8'))
		Hash.update(datetime.now().replace(second=0, microsecond=0).ctime().encode('utf-8'))
		Hash.update(Secret.SecretText.encode('utf-8'))
		return str(Hash.digest()).encode("hex")
	return None
def UpRateNode(NodeId= None):
	if (IDSafeNode(NodeId)!=None):
		global DataBaseFilePath
		conn = sqlite3.connect(DataBaseFilePath)
		c = conn.cursor()
		c.execute("UPDATE ActI SET Rating=Rating+1 WHERE Id=?;",(NodeId,))	
		c.close()
		conn.commit()
def DownRateNode(NodeId= None):
	if (IDSafeNode(NodeId)!=None):
		global DataBaseFilePath
		conn = sqlite3.connect(DataBaseFilePath)
		c = conn.cursor()
		c.execute("UPDATE ActI SET Rating=Rating-1 WHERE Id=?;",(NodeId,))	
		c.close()
		conn.commit()	
def AddHit(NodeId= None):
	if (IDSafeNode(NodeId)!=None):
		global DataBaseFilePath
		conn = sqlite3.connect(DataBaseFilePath)
		c = conn.cursor()
		c.execute("UPDATE ActI SET Hits=Hits+1 WHERE Id=?;",(NodeId,))	
		c.close()
		conn.commit()	
		
@app.route('/About')
def About():	
	return render_template('About.html',WebName=_webname)

@app.route('/Faq')
def Faq():	
	return render_template('Faq.html',WebName=_webname)

@app.route('/<test>')
def Test(test= None):	
	return redirect('/')

@app.route('/StorySoFar/<NodeId>')
def CompileStory(NodeId):
	Node= IDSafeNode(NodeId)
	if (Node==None):
		return redirect('/')
	book = [Node,]
	while (Node['Parent'] !=0):
		Node=GetNode(Node['Parent'])	
		book.append(Node)
	book.reverse()
	return render_template('StorySoFar.html', book=book,WebName=_webname)

def CompileResponce(_request=None,NodeId=None):
	global _webname
	Node=IDSafeNode(NodeId)
	if (Node !=None and _request !=None):
		cookie= request.cookies.get('Btn'+str(NodeId))
		Rated=cookie=="True"
		Child_list=GetNodeChildren(NodeId)
		if (_request.method=='POST'):			
			if ('TxtAddNode' in request.form):
				NextNode= InsertNodeIntoDB({'Parent':NodeId,'Body':request.form['TxtAddNode']})
				if NextNode != None:
					return make_response(redirect('/ID/'+str(NextNode['Id'])))
			if (_request.cookies.get('TimeOut')==CreateHash(_request.remote_addr)):	
				if ('voteUp' in _request.form):
					UpRateNode(NodeId)
					Resp=make_response(redirect('/ID/'+str(Node['Id'])))
					Resp.set_cookie('Btn'+str(NodeId), "True")
					return Resp
				if ('voteDown' in _request.form):
					DownRateNode(NodeId)
					Resp=make_response(redirect('/ID/'+str(Node['Id'])))
					Resp.set_cookie('Btn'+str(NodeId), "True")
					return Resp
		Resp=make_response(render_template('Basic_Layout.html',Child_list=Child_list, Node= Node, Rated=Rated, WebName=_webname))
		if (request.method=="GET"):
			Resp.set_cookie('TimeOut', CreateHash(request.remote_addr))
		if cookie==None:
			AddHit(NodeId)
			Resp.set_cookie('Btn'+str(NodeId),"False")
		return Resp
	return None
def Dbug(O):
	global DebugString
	try:
		DebugString+=json.dumps(O) +'<< >>'
	except Exception(e):
		DebugString+=O
@app.route('/debug',methods=['GET','POST'])
def Debug():
	global DebugString
	global AlowDBUG
	if (AlowDBUG == True):
		DebugString+="------------------------------------------------"
		return DebugString
	else:
		return redirect('/')
@app.route('/new')
def NewPosts():
	global RecentList
	global _webname
	lst =list(RecentList)
	lst.reverse()
	return render_template('TopTen.html',RecentList=lst,WebName=_webname)
@app.route('/ID/<NodeId>',methods=['GET','POST'])
def NodePage(NodeId=None):
	Resp=CompileResponce(request,NodeId)
	if Resp==None:
		return redirect('/')
	return Resp
@app.route('/',methods=['GET','POST'])
def home():	
		NodeId=1
		Resp=CompileResponce(request,NodeId)
		if Resp==None:
			return "error"
		return Resp
