import mysql.connector
mydb=mysql.connector.connect(host='localhost',user='root',\
                             passwd='admin',auth_plugin="mysql_native_password")
mycursor=mydb.cursor()
import tables
import processes
tables.create()
mycursor.execute("USE cltstr;")
processes.menu()
