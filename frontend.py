import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import tables
import processes  # Backend connection

root = tk.Tk()
root.title("Clothing Store Management System")
root.geometry("800x600")
root.config(bg="white")

# Function to clear the frame
def clear_frame():
    for widget in root.winfo_children():
        widget.destroy()

# Home Page
def home():
    clear_frame()
    title = tk.Label(root, text="Clothing Store Management", font=("Arial", 24, "bold"), bg="white")
    title.pack(pady=20)

    button_frame = tk.Frame(root, bg="white")
    button_frame.pack()

    options = [
        ("Add Customer", add_customer_page),
        ("Add Employee", add_employee_page),
        ("Add Supplier", add_supplier_page),
        ("Add Garment", add_garment_page),
        ("New Sale", new_sale_page),
        ("New Purchase", new_purchase_page),
        ("Net Sales", view_net_sales),
        ("Net Purchases", view_net_purchases),
        ("View All Sales", view_all_sales),
        ("View All Purchases", view_all_purchases),
        ("Remove Employee", remove_employee_page),
    ]

    for idx, (text, command) in enumerate(options):
        btn = tk.Button(button_frame, text=text, command=command, width=20, height=2, bg="lightblue", font=("Arial", 12))
        btn.grid(row=idx//2, column=idx%2, padx=20, pady=10)

# Go to Home Button
def go_home_button():
    home_btn = tk.Button(root, text="Go to Home", command=home, bg="orange", font=("Arial", 12, "bold"))
    home_btn.pack(pady=10)

# Add Customer Page
def add_customer_page():
    clear_frame()
    tk.Label(root, text="Add Customer", font=("Arial", 20), bg="white").pack(pady=20)

    name = tk.Entry(root, width=30)
    address = tk.Entry(root, width=30)
    contact = tk.Entry(root, width=30)

    tk.Label(root, text="Name", font=("Arial", 12), bg="white").pack()
    name.pack()
    tk.Label(root, text="Address", font=("Arial", 12), bg="white").pack()
    address.pack()
    tk.Label(root, text="Contact (10 digits)", font=("Arial", 12), bg="white").pack()
    contact.pack()

    def submit():
        try:
            if len(contact.get()) != 10:
                raise ValueError("Contact must be 10 digits")
            processes.addcust(name.get(), address.get(), contact.get())  # Passing collected data to backend
            messagebox.showinfo("Success", "Customer added successfully!")
            home()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    tk.Button(root, text="Submit", command=submit, bg="lightgreen", font=("Arial", 12)).pack(pady=20)
    go_home_button()

# Add Employee Page
def add_employee_page():
    clear_frame()
    tk.Label(root, text="Add Employee", font=("Arial", 20), bg="white").pack(pady=20)

    name = tk.Entry(root, width=30)
    address = tk.Entry(root, width=30)
    age = tk.Entry(root, width=30)
    salary = tk.Entry(root, width=30)
    comm = tk.Entry(root, width=30)

    fields = [("Name", name), ("Address", address), ("Age", age), ("Salary", salary), ("Commission", comm)]

    for label, entry in fields:
        tk.Label(root, text=label, font=("Arial", 12), bg="white").pack()
        entry.pack()

    def submit():
        try:
            processes.addemp(name.get(), address.get(), int(age.get()), int(salary.get()), float(comm.get()))  # Pass data to backend
            messagebox.showinfo("Success", "Employee added successfully!")
            home()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    tk.Button(root, text="Submit", command=submit, bg="lightgreen", font=("Arial", 12)).pack(pady=20)
    go_home_button()

# Add Supplier Page
def add_supplier_page():
    clear_frame()
    tk.Label(root, text="Add Supplier", font=("Arial", 20), bg="white").pack(pady=20)

    name = tk.Entry(root, width=30)
    address = tk.Entry(root, width=30)
    material = tk.Entry(root, width=30)

    for label, entry in [("Name", name), ("Address", address), ("Material Type", material)]:
        tk.Label(root, text=label, font=("Arial", 12), bg="white").pack()
        entry.pack()

    def submit():
        try:
            processes.addsupp(name.get(), address.get(), material.get())  # Pass data to backend
            messagebox.showinfo("Success", "Supplier added successfully!")
            home()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    tk.Button(root, text="Submit", command=submit, bg="lightgreen", font=("Arial", 12)).pack(pady=20)
    go_home_button()

# Add Garment Page
def add_garment_page():
    clear_frame()
    tk.Label(root, text="Add Garment", font=("Arial", 20), bg="white").pack(pady=20)

    gtype = tk.Entry(root, width=30)
    qty = tk.Entry(root, width=30)
    price = tk.Entry(root, width=30)
    sid = tk.Entry(root, width=30)

    for label, entry in [("Type", gtype), ("Quantity", qty), ("Price per Unit", price), ("Supplier ID", sid)]:
        tk.Label(root, text=label, font=("Arial", 12), bg="white").pack()
        entry.pack()

    def submit():
        try:
            processes.addgarment(gtype.get(), int(qty.get()), int(price.get()), int(sid.get()))  # Pass data to backend
            messagebox.showinfo("Success", "Garment added successfully!")
            home()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    tk.Button(root, text="Submit", command=submit, bg="lightgreen", font=("Arial", 12)).pack(pady=20)
    go_home_button()

# New Sale Page
def new_sale_page():
    clear_frame()
    tk.Label(root, text="New Sale", font=("Arial", 20), bg="white").pack(pady=20)

    gids = tk.Entry(root, width=50)
    contact = tk.Entry(root, width=30)
    empid = tk.Entry(root, width=30)

    tk.Label(root, text="Enter Garment IDs (comma separated)", font=("Arial", 12), bg="white").pack()
    gids.pack()
    tk.Label(root, text="Customer Contact No.", font=("Arial", 12), bg="white").pack()
    contact.pack()
    tk.Label(root, text="Employee ID", font=("Arial", 12), bg="white").pack()
    empid.pack()

    def submit():
        try:
            id_list = [int(i.strip()) for i in gids.get().split(",")]
            processes.newsale(id_list, contact.get(), int(empid.get()))  # Pass data to backend
            messagebox.showinfo("Success", "Sale recorded successfully!")
            home()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    tk.Button(root, text="Submit", command=submit, bg="lightgreen", font=("Arial", 12)).pack(pady=20)
    go_home_button()

# New Purchase Page
def new_purchase_page():
    clear_frame()
    tk.Label(root, text="New Purchase", font=("Arial", 20), bg="white").pack(pady=20)

    sid = tk.Entry(root, width=30)
    gid = tk.Entry(root, width=30)
    price = tk.Entry(root, width=30)
    qty = tk.Entry(root, width=30)

    for label, entry in [("Supplier ID", sid), ("Garment ID", gid), ("Total Price", price), ("Quantity", qty)]:
        tk.Label(root, text=label, font=("Arial", 12), bg="white").pack()
        entry.pack()

    def submit():
        try:
            processes.newpurchase(int(sid.get()), int(gid.get()), int(price.get()), int(qty.get()))  # Pass data to backend
            messagebox.showinfo("Success", "Purchase recorded successfully!")
            home()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    tk.Button(root, text="Submit", command=submit, bg="lightgreen", font=("Arial", 12)).pack(pady=20)
    go_home_button()

# View Net Sales
def view_net_sales():
    clear_frame()
    amt = processes.nets()
    tk.Label(root, text=f"Total Net Sales: ₹{amt}", font=("Arial", 20), bg="white").pack(pady=40)
    go_home_button()

# View Net Purchases
def view_net_purchases():
    clear_frame()
    amt = processes.netp()
    tk.Label(root, text=f"Total Net Purchases: ₹{amt}", font=("Arial", 20), bg="white").pack(pady=40)
    go_home_button()

# View All Sales
def view_all_sales():
    clear_frame()
    tk.Label(root, text="All Sales", font=("Arial", 20), bg="white").pack(pady=20)

    sales = processes.allsales()
    for sale in sales:
        tk.Label(root, text=str(sale), font=("Arial", 10), bg="white").pack()

    go_home_button()

# View All Purchases
def view_all_purchases():
    clear_frame()
    tk.Label(root, text="All Purchases", font=("Arial", 20), bg="white").pack(pady=20)

    purchases = processes.allpurchase()
    for purchase in purchases:
        tk.Label(root, text=str(purchase), font=("Arial", 10), bg="white").pack()

    go_home_button()

# Remove Employee
def remove_employee_page():
    clear_frame()
    tk.Label(root, text="Remove Employee", font=("Arial", 20), bg="white").pack(pady=20)

    empid = tk.Entry(root, width=30)
    tk.Label(root, text="Employee ID to Remove", font=("Arial", 12), bg="white").pack()
    empid.pack()

    def submit():
        try:
            processes.rememp(int(empid.get()))  # Pass data to backend
            messagebox.showinfo("Success", "Employee removed successfully!")
            home()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    tk.Button(root, text="Submit", command=submit, bg="red", font=("Arial", 12)).pack(pady=20)
    go_home_button()

# Start with Home directly
home()
root.mainloop()
