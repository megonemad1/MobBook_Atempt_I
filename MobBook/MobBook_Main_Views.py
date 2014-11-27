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



@app.route('/ID/<NodeId>',methods=['GET','POST'])
def Param(NodeId=None):
	if (NodeId==None or not RepresentsInt(NodeId)):
		return redirect('/')
	else:
		conn = sqlite3.connect(DataBaseFilePath)
		c = conn.cursor()		
		c.execute('''CREATE TABLE IF NOT EXISTS ActI (Id INTEGER PRIMARY KEY AUTOINCREMENT,Parent int,UpRating int,DownRating int,Body text)''')
		c.execute('SELECT * FROM ActI WHERE Id=?', (NodeId,))
		Node =c.fetchone()		
		#cursor.close();
		c.execute('SELECT * FROM ActI WHERE Parent=?', (NodeId,))
		Child_list = c.fetchall()
		c.close();
		print(Node)
		print(Child_list)
		if (Node==None):
			return redirect('/')
		if (request.method=='POST'):			
			StoryText = request.form['TxtAddNode']
			if(StoryText != ""):
				conn = sqlite3.connect(DataBaseFilePath)
				c = conn.cursor()
				c.execute("INSERT INTO ActI(Parent,UpRating,DownRating,Body) VALUES (?,0,0,?)",(NodeId,StoryText,))			
				NextNodeId=c.lastrowid
				c.close()
				conn.commit()
				return redirect('/ID/'+str(NextNodeId))
		return render_template('Basic_Layout.html',	Child_list=Child_list, Node= Node)

@app.route('/About')
def About():	
	return "about Page"

@app.route('/Faq')
def Faq():	
	return "Faq Page"

@app.route('/<test>')
def Test(test= None):	
	return redirect('/')

@app.route('/',methods=['GET','POST'])
def home():	
		NodeId=1
		conn = sqlite3.connect(DataBaseFilePath)
		c = conn.cursor()		
		c.execute('''CREATE TABLE IF NOT EXISTS ActI (Id INTEGER PRIMARY KEY AUTOINCREMENT,Parent int,UpRating int,DownRating int,Body text)''')
		c.execute('SELECT * FROM ActI WHERE Id=?', (NodeId,))
		Node =c.fetchone()		
		#cursor.close();
		print(Node)
		c.execute('SELECT * FROM ActI WHERE Parent=?',(NodeId,))
		Child_list = c.fetchall()
		#c.execute("INSERT INTO ActI(Parent,UpRating,DownRating,Body) VALUES (0,0,0,'there was a knock at the door')")
		#conn.commit()
		print(Child_list)
		c.close();
		if (request.method=='POST'):
			StoryText = request.form['TxtAddNode']
			if(StoryText != ""):
				conn = sqlite3.connect(DataBaseFilePath)
				c = conn.cursor()			
				c.execute("INSERT INTO ActI(Parent,UpRating,DownRating,Body) VALUES (?,0,0,?)",(NodeId,StoryText,))			
				NextNodeId=c.lastrowid
				c.close()
				conn.commit()
				return redirect('/ID/'+str(NextNodeId))
		return render_template('Basic_Layout.html',	Child_list=Child_list, Node= Node)



#	optid=""
	#if (request.method=='POST'):
#		optid= (request.form['options'])
#		print(request.form['options'])
#	return render_template('Basic_Layout.html',	option_list=[{'optid':"Dynamic1"},{'optid':"Dynamic2"},{'optid':"spotify"},{'optid':"cheese"}], optid=optid)

	#optid=username
	#if (request.method=='POST'):
	#	optid= (request.form['options'])
	#	print(request.form['options'])