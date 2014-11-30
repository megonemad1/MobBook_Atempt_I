from flask import Flask,render_template,request,redirect
import sqlite3
from MobBook import app


DataBaseFilePath ='Anthology.db';


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
	c.execute('''CREATE TABLE IF NOT EXISTS ActI (Id INTEGER PRIMARY KEY AUTOINCREMENT,Parent int,UpRating int,DownRating int,Body text,Hits int)''')
	c.execute('SELECT * FROM ActI WHERE Id=?', (NodeId,))
	LstNode =c.fetchone()
	c.close();	
	return {'Id':LstNode[0],'Parent':LstNode[1],'UpRating':LstNode[2],'DownRating':LstNode[3],'Body':LstNode[4],'Hits':LstNode[5]}
	


def GetNodeChildren(NodeId):			
	global DataBaseFilePath
	conn = sqlite3.connect(DataBaseFilePath)
	c = conn.cursor()	
	c.execute('''CREATE TABLE IF NOT EXISTS ActI (Id INTEGER PRIMARY KEY AUTOINCREMENT,Parent int,UpRating int,DownRating int,Body text,Hits int)''')
	c.execute('SELECT * FROM ActI WHERE Parent=?', (NodeId,))
	LstChild_list = c.fetchall()
	c.close();	
	Child_list =[]
	for C in LstChild_list:
		Child_list.append({'Id':C[0],'Parent':C[1],'UpRating':C[2],'DownRating':C[3],'Body':C[4],'Hits':C[5]})
	return Child_list


def InsertNodeIntoDB(Node):
	if (Node['Body'] !=""):
		global DataBaseFilePath
		conn = sqlite3.connect(DataBaseFilePath)
		c = conn.cursor()
		c.execute("INSERT INTO ActI(Parent,UpRating,DownRating,Body,Hits) VALUES (?,0,0,?,1)",(Node['Parent'],Node['Body'],))			
		NextNodeId=c.lastrowid
		c.close()
		conn.commit()
		return {'Id': NextNodeId,'Parent':Node['Parent'], 'UpRating':0, 'DownRating':0, 'Body':Node['Body'], 'Hits':1}
	else:
		return None

def IDSafeNode(NodeId):
	if (NodeId==None or not RepresentsInt(NodeId)):
		return None
	else:
		Node=GetNode(NodeId)		
		if (Node==None):
			return None
		return Node

@app.route('/About')
def About():	
	return render_template('About.html')

@app.route('/Faq')
def Faq():	
	return "Faq Page"

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
	return render_template('StorySoFar.html', book=book)




@app.route('/ID/<NodeId>',methods=['GET','POST'])
def Param(NodeId=None):
	Node=IDSafeNode(NodeId)
	if Node==None:
		return redirect('/')		
	Child_list=GetNodeChildren(NodeId)
	if (request.method=='POST'):	
		NextNode = InsertNodeIntoDB({'Parent':NodeId,'Body':request.form['TxtAddNode']})
		if NextNode != None:
			return redirect('/ID/'+str(NextNode['Id']))
	return render_template('Basic_Layout.html',	Child_list=Child_list, Node= Node)

@app.route('/',methods=['GET','POST'])
def home():	
		NodeId=1
		Node=GetNode(NodeId)
		Child_list = GetNodeChildren(NodeId)
		if (request.method=='POST'):
			NextNode= InsertNodeIntoDB({'Parent':NodeId,'Body':request.form['TxtAddNode']})
			if NextNode != None:
				return redirect('/ID/'+str(NextNode['Id']))
		return render_template('Basic_Layout.html',	Child_list=Child_list, Node= Node)