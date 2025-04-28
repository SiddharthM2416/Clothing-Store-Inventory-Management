import mysql.connector
mydb=mysql.connector.connect(host='localhost',user='root',passwd='admin',auth_plugin="mysql_native_password")
mycursor=mydb.cursor()
mycursor.execute('Create database if not exists cltstr;')
mycursor.execute('use cltstr;')

customer="CREATE TABLE if not exists CUSTOMER(\
custid INT AUTO_INCREMENT PRIMARY KEY,\
name VARCHAR(20),\
address VARCHAR(15),\
contact CHAR(10));"

supplier="CREATE TABLE if not exists SUPPLIER(\
sid int auto_increment primary key,\
sname varchar(20),\
address varchar(15),\
material varchar(10));"

garments="CREATE TABLE if not exists GARMENTS(\
gid int auto_increment primary key,\
type varchar(20),\
qty int,\
price int,\
sid int references supplier.sid);"

employee="CREATE TABLE if not exists EMPLOYEE(\
empid int auto_increment primary key,\
ename varchar(20),\
address varchar(15),\
age int,\
salary int,\
comm decimal(2,2));"

sales="CREATE TABLE if not exists SALES(\
salid int auto_increment primary key,\
custid int references customer.custid,\
empid int references employee.empid,\
amt int);"

purchase="CREATE TABLE if not exists PURCHASE(\
pid int auto_increment primary key,\
sid int references supplier.sid,\
gid int references garments.gid,\
price int,\
qty int);"

l1=[customer,supplier,garments,employee,sales,purchase]
def create():
    for i in l1:
        mycursor.execute(i)

create()

