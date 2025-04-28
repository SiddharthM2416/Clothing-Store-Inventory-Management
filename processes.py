import mysql.connector
mydb=mysql.connector.connect(host='localhost',user='root'\
                             ,passwd='admin',auth_plugin="mysql_native_password")
mycursor=mydb.cursor()
mycursor.execute("USE cltstr;")

#To Add a new customer
def addcust(name,address,contact):
    val=(name,address,contact)
    ins="INSERT INTO customer(name,address,contact) VALUES (%s,%s,%s);"
    mycursor.execute(ins,val)
    mydb.commit()

#To add a new supplier
def addsupp(name,address,material):
    val=(name, address, material)
    ins="INSERT INTO supplier(sname,address,material) VALUES (%s,%s,%s);"
    mycursor.execute(ins, val)
    mydb.commit()

#To add a new type of Garment
def addgarment(t,qty,price,sid):
    a=(t,qty,price,sid)
    mycursor.execute("INSERT INTO garments(type,qty,price,sid) VALUES(%s,%s,%s,%s);", a)
    mydb.commit()

#To add a new employee
def addemp(name,address,age,sal,comm):
    ins="INSERT INTO employee(ename,address,age,salary,comm) VALUES(%s,%s,%s,%s,%s);"
    val=(name, address, age, sal, comm)
    mycursor.execute(ins, val)
    mydb.commit()

#To record new sales
def newsale(l1, contact, empid):
    mycursor.execute("SELECT gid FROM garments;")
    l2 = mycursor.fetchall()
    l1 = [i for i in l1 if (i,) in l2]  # Validate garment IDs

    mycursor.execute("SELECT contact FROM customer;")
    c = mycursor.fetchall()
    if (contact,) not in c:
        raise Exception("Customer not found. Please add customer first.")

    mycursor.execute("SELECT empid FROM employee;")
    e = mycursor.fetchall()
    if (empid,) not in e:
        raise Exception("Invalid Employee ID.")

    mycursor.execute("SELECT custid FROM customer WHERE contact = %s;", (contact,))
    cid = mycursor.fetchone()[0]

    amt = 0
    for i in l1:
        mycursor.execute("SELECT price FROM garments WHERE gid = %s;", (i,))
        p = mycursor.fetchone()[0]
        amt += p
        mycursor.execute("UPDATE garments SET qty = qty - 1 WHERE gid = %s;", (i,))
        mydb.commit()

    vals = (cid, empid, amt)
    q = "INSERT INTO sales(custid, empid, amt) VALUES (%s, %s, %s);"
    mycursor.execute(q, vals)
    mydb.commit()



    
#To record a new purchase from suppliers to store            
def newpurchase(sid, gid, price, qty):
    mycursor.execute("SELECT sid FROM supplier;")
    s = mycursor.fetchall()
    if (sid,) not in s:
        raise Exception("Invalid Supplier ID.")

    mycursor.execute("SELECT gid FROM garments WHERE sid = %s;", (sid,))
    g = mycursor.fetchall()
    if (gid,) not in g:
        raise Exception("Invalid Garment ID for given Supplier.")

    ins = "INSERT INTO purchase(sid, gid, price, qty) VALUES (%s, %s, %s, %s);"
    val = (sid, gid, price, qty)
    mycursor.execute(ins, val)
    mydb.commit()

    mycursor.execute("UPDATE garments SET qty = qty + (%s) WHERE gid = (%s);", (qty, gid))
    mydb.commit()


def nets():#To check Total sales
    mycursor.execute("select sum(amt) from sales;")
    amt=mycursor.fetchone()[0]
    return amt

def netp():#To check Total purchases
    mycursor.execute("select sum(price) from purchase;")
    amt=mycursor.fetchone()[0]
    return amt

def allsales(): #To open a list of all sales
    mycursor.execute("Select sales.*, employee.ename from sales JOIN \
employee ON sales.empid=employee.empid;")
    s=mycursor.fetchall()
    return s

def allpurchase(): #To open a list of all purchases
    mycursor.execute("Select purchase.*, supplier.sname from purchase \
JOIN supplier ON purchase.sid=supplier.sid;")
    s=mycursor.fetchall()
    return s

        
def rememp(empid): #To remove an employee
    mycursor.execute("delete from employee where empid=(%s);",(empid,))
    mydb.commit()

def menu():
    while True:
        x=int(input('''
    Choose an option:
    1. Add Customer
    2. Add Employee
    3. Add Supplier
    4. Add Garment
    5. New Sale
    6. New Purchase
    7. Net Sales
    8. Net Purchases
    9. View all Sales
    10. View all Purchases
    11. Remove Employee
    12. Exit
    -->'''))

        if x==1:
            addcust()
        elif x==2:
            addemp()
        elif x==3:
            addsupp()
        elif x==4:
            addgarment()
        elif x==5:
            l1=[]
            b=1
            while b==1:
                a=int(input("Enter GID of product: "))
                if a not in l1:
                    l1.append(a)
                b=int(input("Add another product?(0/1): "))
            newsale(l1)
        elif x==6:
            newpurchase()
        elif x==7:
            print("Total Sales: ",nets())
        elif x==8:
            print("Total Purchases: ",netp())
        elif x==9:
            allsales()
        elif x==10:
            allpurchase()
        elif x==11:
            rememp()
        elif x==12:
            break
        else:
            print("Invalid input")
            


    
