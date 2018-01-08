import MySQLdb

db = MySQLdb.connect(host="localhost",
                     user="root",
                     passwd="root",
                     db='projectDB')

cur = db.cursor()
cur.execute("select password from User where email = 'md';")
res = cur.fetchall()
print(type(len(res)))
