import sqlite3


con = sqlite3.connect("offline.db")
cur = con.cursor()
cur.execute("SELECT * from login")
res = cur.fetchall()


if res ==[]:
	print('no login info')
	
else:
    print('exist')
    print((res[0][1]))
con.commit()
con.close()