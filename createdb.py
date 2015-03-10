import sqlite3
import os
DataBaseFilePath="Anthology.db"
conn = sqlite3.connect(DataBaseFilePath)
c = conn.cursor()		
c.execute('''CREATE TABLE IF NOT EXISTS ActI (Id INTEGER PRIMARY KEY AUTOINCREMENT,Parent int,Rating int,Body text,Hits int)''')
c.execute("INSERT INTO ActI(Parent,Rating,Body,Hits) VALUES (?,0,?,0)",(0,"Their was a knock at the door",))	
print("remaking Db")
c.close()
conn.commit()