from flask import Flask,render_template,request

from MobBook import app

@app.route('/')
@app.route('/index')
def index():
	return render_template('Basic_Layout.html')