import mysql.connector
mydb=mysql.connector.connect(host='localhost',user='root'\
                             ,passwd='admin',auth_plugin="mysql_native_password")
mycursor=mydb.cursor()
mycursor.execute("USE cltstr;")

#To Add a new customer
def addcust():
    name=input("Enter Customer name: ")
    address=input("Enter Customer address: ")
    while True:
        contact=input("Enter phone no.: ")
        if len(contact)!=10:
            print("INVALID NUMBER TRY AGAIN")
        else:
            break
    val=(name,address,contact)
    ins="INSERT INTO customer(name,address,contact) VALUES (%s,%s,%s);"
    mycursor.execute(ins,val)
    mydb.commit()

#To add a new supplier
def addsupp():
    name=input("Enter supplier name: ")
    address=input("Enter supplier address: ")
    material=input("Enter material type: ")
    val=(name, address, material)
    ins="INSERT INTO supplier(sname,address,material) VALUES (%s,%s,%s);"
    mycursor.execute(ins, val)
    mydb.commit()

#To add a new type of Garment
def addgarment():
    t=input("Enter type of garment: ")
    qty=int(input("Enter quantity of garment: "))
    price=int(input("Enter Price per unit garment: "))
    mycursor.execute("SELECT sid FROM supplier;")
    supp=mycursor.fetchall()
    while True:#To check for valid supplier
        sid=int(input("Enter supplier id: "))
        if (sid,) in supp:
            a=(t,qty,price,sid)
            mycursor.execute("INSERT INTO garments(type,qty,price,sid) VALUES(%s,%s,%s,%s);", a)
            mydb.commit()
            mycursor.nextset()
            break
        else:
            print("Invalid supplier id")


#To add a new employee
def addemp():
    name=input("Enter Employee name: ")
    address=input("Enter Employee address: ")
    age=int(input("Enter Employee age: "))
    sal=int(input("Enter Employee salary: "))
    comm=float(input("Enter Employee commission: "))
    ins="INSERT INTO employee(ename,address,age,salary,comm) VALUES(%s,%s,%s,%s,%s);"
    val=(name, address, age, sal, comm)
    mycursor.execute(ins, val)
    mydb.commit()

#To record new sales
def newsale(l1):
    mycursor.execute("SELECT empid FROM employee;")
    e=mycursor.fetchall()
    
    mycursor.execute("SELECT gid FROM garments;")
    l2=mycursor.fetchall()
    l1=[i for i in l1 if (i,) in l2]#To check if items bought are valid

    mycursor.execute("SELECT contact from customer;")
    c=mycursor.fetchall()
    contact=input("Enter Customer Phone no.: ")
    if (contact,) not in c:
        print("No customer found, adding new customer")
        addcust()#If no customer found add new

    mycursor.execute("SELECT custid FROM customer WHERE contact = %s;", (contact,))
    cid=mycursor.fetchall()[0][0]

    while True:#To check if employee id is valid
        empid=int(input("Enter Employee ID: "))
        if (empid,) not in e:
            print("Invalid Employee ID")
        else:
            break

    amt=0
    for i in l1:#To calculate total amount
        mycursor.execute("SELECT price FROM garments WHERE gid = %s;", (i,))
        p=mycursor.fetchone()[0]
        amt+=p
        mycursor.execute("UPDATE garments SET qty = qty - 1 WHERE gid = %s;", (i,))
        mydb.commit()    
    
    vals=(cid, empid, amt)
    q="INSERT INTO sales(custid, empid, amt) VALUES (%s, %s, %s);"
    mycursor.execute(q, vals)
    mydb.commit()
    print("Sale recorded successfully!")



    
#To record a new purchase from suppliers to store            
def newpurchase():
    mycursor.execute("Select * from supplier;")
    s=mycursor.fetchall()
    for i in s:
        print(i)

    mycursor.execute("select sid from supplier;")
    s=mycursor.fetchall()
    
    while True:#To check if supplier is valid
        sid=int(input("Enter Supplier id: "))
        if (sid,) not in s:
            print("No current Supplier found try again")
        else:
            break

    mycursor.execute("Select gid from garments where sid=(%s)",(sid,))
    g=mycursor.fetchall()# to check if garment bought from supplier is valid
    for i in g:
        print(i)

    
    while True:
        gid=int(input("Enter Garment ID: "))
        if (gid,) not in g:
            print("Invalid garment try again")
        else:
            break

    price=int(input("Enter Total price: "))
    qty=int(input("Enter Quantity of garments purchased: "))

    ins="Insert into purchase(sid,gid,price,qty) values(%s,%s,%s,%s);"
    val=(sid,gid,price,qty)
    mycursor.execute(ins,val)
    mydb.commit()
    #To update the quantity of garment in stock
    mycursor.execute("Update garments set qty=qty+(%s) where gid=(%s);",(qty,gid))


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
    for i in s:
        print(i)

def allpurchase(): #To open a list of all purchases
    mycursor.execute("Select purchase.*, supplier.sname from purchase \
JOIN supplier ON purchase.sid=supplier.sid;")
    s=mycursor.fetchall()
    for i in s:
        print(i)

        
def rememp(): #To remove an employee
    mycursor.execute("Select empid from employee;")
    emp = mycursor.fetchall()
    for i in emp:
        print(i)
    empid=int(input("Enter empid: "))
    if (empid,) in emp:
        mycursor.execute("delete from employee where empid=(%s);",(empid,))
        mydb.commit()
    else:
        menu()

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
            


    
