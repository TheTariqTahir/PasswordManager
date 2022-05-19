import sqlite3


con = sqlite3.connect("offline.db")
cur = con.cursor()

# cur.execute("SELECT * from theme")
cur.execute("INSERT INTO theme VALUES ('Light','Teal')")
res2 = cur.fetchall()
print(res2)



# cur.execute("SELECT * from login")
# res = cur.fetchall()
# if res ==[]:
# 	print('no login info')
# else:
#     print('exist')
#     print((res[0][1]))



con.commit()
con.close()