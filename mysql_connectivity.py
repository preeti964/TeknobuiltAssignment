import mysql.connector as connector
mydb = connector.connect(host='localhost',user='root',password='123456', database='tekno_movie')
# print(mydb.connection_id)

mycursor =mydb.cursor()
# mycursor.execute('show tables')
mycursor.execute("select * from imdbtop250")
for i in mycursor:
    print(i)