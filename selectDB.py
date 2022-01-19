import sqlite3


with sqlite3.connect('price.db') as conn:
    curs = conn.cursor()
    curs.execute("SELECT * FROM price")
    rows = curs.fetchall()
    for item in rows:
        print(item[0],"  ",item[1],"  ",item[2],"  ",item[3])
