import sqlite3

connection=sqlite3.connect('sqldb.db')
cursor=connection.cursor()

cursor.execute("SELECT * from events")
rows =cursor.fetchall()
print(rows)


new_rows= [('Rock&Roll', 'Tbilisi', '02.02.2049'),
           ('LP', 'Moscow', '02.03.2093')]

cursor.executemany("Insert into events values (?,?,?) ", new_rows)

connection.commit()


