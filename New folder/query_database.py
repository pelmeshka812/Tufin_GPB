import config

conn = config.createConnection()
sql = "select * from main_table order by pk desc limit 30"
cur = conn.cursor()
result = list(cur.execute(sql))
conn.commit()  
conn.close()
for row in result:
    print(row)
