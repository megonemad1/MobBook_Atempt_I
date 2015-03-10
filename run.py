import sqlite3
DataBaseFilePath="Anthology.db"
conn = sqlite3.connect(DataBaseFilePath)
c = conn.cursor()		
c.execute('''CREATE TABLE IF NOT EXISTS ActI (Id INTEGER PRIMARY KEY AUTOINCREMENT,Parent int,Rating int,Body text,Hits int)''')
c.execute('''SELECT Id from ActI''')
if (c.fetchall()==0):
	c.execute("INSERT INTO ActI(Parent,Rating,Body,Hits) VALUES (?,0,?,0)",(0,"Their was a knock at the door",))	
	print("remaking Db")
c.close()
conn.commit()

#!flask/bin/python
from MobBook import app

app.run(debug=True,host="0.0.0.0")


#import os.path
#os.path.isfile(fname) test for data base
# if not exsist make one