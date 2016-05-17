import sqlite3
 
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d
 
connection = sqlite3.connect("Reddit2.db")
connection.row_factory = dict_factory
 
cursor = connection.cursor()
 
cursor.execute("select * from Comments")
 
# fetch all or one we'll go for all.
 
results = cursor.fetchall()
 
print results
 
connection.close()