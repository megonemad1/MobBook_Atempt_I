from flask import Flask,render_template,request

from MobBook import app



@app.route('/ID/<username>',methods=['GET','POST'])
def Param(username="world"):
	optid=username
	if (request.method=='POST'):
		optid= (request.form['options'])
		print(request.form['options'])
	return render_template('Basic_Layout.html',	option_list=[{'optid':"Dynamic1"},{'optid':"Dynamic2"},{'optid':"spotify"},{'optid':"cheese"}], optid=optid)

@app.route('/',methods=['GET','POST'])
def home():	
	optid=""
	if (request.method=='POST'):
		optid= (request.form['options'])
		print(request.form['options'])
	return render_template('Basic_Layout.html',	option_list=[{'optid':"Dynamic1"},{'optid':"Dynamic2"},{'optid':"spotify"},{'optid':"cheese"}], optid=optid)