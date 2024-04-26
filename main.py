from tkinter import *
from tkinter import ttk
import sqlite3
import matplotlib.pyplot as plt

#this function contains everything to do with the set up window
def SetUp_Clicked():
    root.withdraw()
    conn = sqlite3.connect('Comp Science.db')
    cursor = conn.cursor()
    cursor.execute('SELECT email FROM Customer')
    customerid = str(cursor.fetchone())    
    conn.commit()
    conn.close()
    while customerid == 'None':
        email_window = Tk()
        email_window.resizable(False, False)
        email_window.title("email")
        email_window.geometry("200x180")
        email_window.configure(bg='grey')
        
        email_Lbl = Label(email_window, text="Enter you email: ",bg="grey")
        email_Lbl.place(x=20,y=50)
        
        email_ent = Entry(email_window,width=0)
        email_ent.place(x=20,y=70)
        def submit():
            email_val = email_ent.get()
            conn = sqlite3.connect('Comp Science.db')
            cursor = conn.cursor()

    # Create a table if it doesn't exist
            cursor.execute('''CREATE TABLE IF NOT EXISTS Customer
                    (CustomerID INTEGER PRIMARY KEY, email TEXT)''')

    # Insert data into the table
            cursor.execute('INSERT INTO customer (CustomerID, email) VALUES (?, ?)', (1, email_val,))

    # Commit changes and close the connection
            conn.commit()
            conn.close()
            email_window.destroy()
            
        submit_btn = Button(email_window, text="submit",command=submit)
        submit_btn.place(x=20,y=95)
        break
    def InventoryClicked():
        SetUp_Window.withdraw()
        Inventory_window = Tk()
        Inventory_window.resizable(False, False)
        Inventory_window.title("Inventory")
        Inventory_window.geometry("500x400")
        Inventory_window.configure(bg='grey')
        
        stock_list = Listbox(Inventory_window)
        stock_list.pack()

        def select_item():
            selected_item = str(stock_list.get(stock_list.curselection()))
            item, quantity = selected_item.split(" - ")
            item_entry.delete(0, 'end')
            quantity_entry.delete(0, 'end')
            item_entry.insert(0, item)
            quantity_entry.insert(0, quantity)
            
        def getData():
            conn = sqlite3.connect('Comp Science.db')
            cursor = conn.cursor()
            cursor.execute('''SELECT ProductName, StockQuantity FROM Product''')
            listData = cursor.fetchall()
            for row in listData:
                (ProductName, StockQuantity) = tuple(row)
                stock_list.insert(END, f"{ProductName} - {StockQuantity}")



        def addStock():
            new_stock = item_entry.get()
            new_quantity = quantity_entry.get()
            if item_entry and quantity_entry:
                if new_stock.isdigit() == True or new_quantity.isdigit() != True:
                    error_label = Label(Inventory_window, text="Check that the first field is in words and the second field is an integer", fg="red")
                    Inventory_window.after(4000, lambda: error_label.destroy())
                    error_label.pack()
                else:
                    try:
                        item_entry.delete(0, 'end')
                        quantity_entry.delete(0, 'end')
                        conn = sqlite3.connect('Comp Science.db')
                        cursor = conn.cursor()

                        # Create a table if it doesn't exist
                        cursor.execute('''CREATE TABLE IF NOT EXISTS Product
                                        (ProductID INTEGER PRIMARY KEY, ProductName TEXT, CategoryID INTEGER, StockQuantity INTEGER NOT NULL)''')
                        
                        stock_data = [
                            (new_stock, new_quantity)
                        ]
                        for user in stock_data:   
                            cursor.execute('INSERT INTO Product (ProductName, StockQuantity) VALUES (?, ?)', user)
                            
                        # Commit changes and close the connection
                        conn.commit()
                        conn.close()
                        
                        stock_list.insert(END,new_stock + " - " + new_quantity)

                    except:
                        error_label = Label(Inventory_window, text="value is already in the database", fg="red")
                        Inventory_window.after(4000, lambda: error_label.destroy())
                        error_label.pack()
                        return FALSE 

            else:
                error_label = Label(Inventory_window, text="One of the fields are empty", fg="red")
                Inventory_window.after(4000, lambda: error_label.destroy())
                error_label.pack()
                
        def editStock():
            current_stock = item_entry.get()
            update_quantity = quantity_entry.get()
            print(current_stock)
            print(update_quantity)
            if current_stock and update_quantity:
                if current_stock.isdigit() == True or update_quantity.isdigit() != True:
                    error_label = Label(Inventory_window, text="Check that the first field is in words and the second field is an integer", fg="red")
                    Inventory_window.after(4000, lambda: error_label.destroy())
                    error_label.pack()
                else:
                    conn = sqlite3.connect('Comp Science.db')
                    cursor = conn.cursor()
                    cursor.execute('UPDATE Product SET StockQuantity =? WHERE ProductName =?', (int(update_quantity), current_stock))
                    conn.commit()
                    conn.close()
                    stock_list.delete(0, END)
                    getData()
                    item_entry.delete(0, 'end')
                    quantity_entry.delete(0, 'end')
            else:
                error_label = Label(Inventory_window, text="One of the fields are empty", fg="red")
                Inventory_window.after(4000, lambda: error_label.destroy())
                error_label.pack()
                
        def deleteStock():
            delete_name = item_entry.get()
            if delete_name:
                conn = sqlite3.connect('Comp Science.db')
                cursor = conn.cursor()
                cursor.execute('DELETE FROM Product WHERE ProductName = ?', (delete_name,))
                conn.commit()
                conn.close()
                stock_list.delete(0, END)
                getData()
                item_entry.delete(0, 'end')
                quantity_entry.delete(0, 'end')
            else:
                error_label = Label(Inventory_window, text="One of the fields are empty", fg="red")
                Inventory_window.after(4000, lambda: error_label.destroy())
                error_label.pack()
        def back():
            Inventory_window.destroy()
            root.deiconify()

        item_label = Label(Inventory_window, text="Item:", bg="grey")
        item_label.pack()

        item_entry = Entry(Inventory_window)
        item_entry.pack()

        quantity_label = Label(Inventory_window, text="Quantity:", bg="grey")
        quantity_label.pack()

        quantity_entry = Entry(Inventory_window)
        quantity_entry.pack()

        select_button = Button(Inventory_window, text="Select Item", width=10, height=2, command=select_item)
        select_button.place(x=260, y=260)

        add_btn = Button(Inventory_window, text="Add Stock", width=10, height=2, command=addStock)
        add_btn.place(x=160, y=260)

        Edit_btn = Button(Inventory_window, text="Edit Stock", width=10, height=2, command=editStock)
        Edit_btn.place(x=260, y=320)

        Delete_btn = Button(Inventory_window, text="Delete Stock", width=10, height=2, command=deleteStock)
        Delete_btn.place(x=160, y=320)

        back_btn = Button(Inventory_window, text="Back", width=10, height=2, command=back)
        back_btn.place(x=410, y=355)

        getData()

    def EmployeeClicked():
        SetUp_Window.withdraw()
        # Create the employees window
        employees_window = Tk()
        employees_window.title('Employees')
        employees_window.geometry("600x400")

        # Create input fields for the user to enter employee details
        name_label = Label(employees_window, text="Name:")
        name_label.pack()
        name_entry = Entry(employees_window)
        name_entry.pack()

        salary_label = Label(employees_window, text="Salary:")
        salary_label.pack()
        salary_entry = Entry(employees_window)
        salary_entry.pack()

        Days_label = Label(employees_window, text="Days:")
        Days_label.pack()
        Days_entry = Entry(employees_window)
        Days_entry.pack()
        myFrame = Frame(employees_window)
        myScrollbar = Scrollbar(myFrame, orient=VERTICAL)
        # Create a Listbox to display the employees
        employees_list = Listbox(myFrame, width=0,height=8, yscrollcommand=myScrollbar.set)

        myScrollbar.config(command=employees_list.yview)
        myScrollbar.pack(side=RIGHT, fill=Y)
        myFrame.pack()

        employees = []
        for employee in employees:
            employees_list.insert(END, employee)
        employees_list.pack()

        # Function to insert the user input as a new employee
        def insert_employee():
            name = name_entry.get()
            salary = salary_entry.get()
            Days = Days_entry.get()
            if name and salary:  # Check if both name and salary fields are not empty
                new_employee = name + " - " + salary + " - " + Days
                employees_list.insert(END, new_employee)
                conn = sqlite3.connect('Comp Science.db')
                cursor = conn.cursor()

                # Create a table if it doesn't exist
                cursor.execute('''CREATE TABLE IF NOT EXISTS Product
                                (EmployeeID INTEGER PRIMARY KEY, EmployeeName TEXT, EmployeePay INTEGER, EmployeeDays INTEGER NOT NULL)''')
                
                stock_data = [
                    (name, salary, Days)
                ]
                for user in stock_data:   
                    cursor.execute('INSERT INTO Employee (EmployeeName, EmployeePay, EmployeeDays) VALUES (?, ?, ?)', user)
                    
                # Commit changes and close the connection
                conn.commit()
                conn.close()

                # Clear the input fields after adding an employee
                name_entry.delete(0, 'end')
                salary_entry.delete(0, 'end')
                Days_entry.delete(0, 'end')
            else:
                # Display an error message if either name or salary field is empty
                error_label = Label(employees_window, text="Both name and salary fields are required", fg="red")
                employees_window.after(2000, lambda: error_label.destroy())
                error_label.pack()
        # Create the "Add Employee" button to add the input to the Listbox
        def select_item():
            selected_item = str(employees_list.get(employees_list.curselection()))
            name, salary, days = selected_item.split(" - ")
            name_entry.delete(0, 'end')
            salary_entry.delete(0, 'end')
            Days_entry.delete(0, 'end')
            name_entry.insert(0, name)
            salary_entry.insert(0, salary)
            Days_entry.insert(0, days)
        def getData():
            conn = sqlite3.connect('Comp Science.db')
            cursor = conn.cursor()
            cursor.execute('''SELECT EmployeeName, EmployeePay, EmployeeDays FROM Employee''')
            listData = cursor.fetchall()
            for row in listData:
                (EmployeeName, EmployeePay, EmployeeDays) = tuple(row)
                employees_list.insert(END, f"{EmployeeName} - {EmployeePay} - {EmployeeDays}")

        def editStock():
            current_employee = name_entry.get()
            update_salary = salary_entry.get()
            update_days = Days_entry.get()
            
            if name_entry.index("end") == 0 and salary_entry.index("end") == 0 and Days_entry.index("end"):
                error_label = Label(employees_window, text="at least one of the fields are empty", fg="red")
                employees_window.after(2000, lambda: error_label.destroy())
                error_label.pack()
            else:
                conn = sqlite3.connect('Comp Science.db')
                cursor = conn.cursor()
                cursor.execute('UPDATE Employee SET (EmployeePay, EmployeeDays) =(?, ?) WHERE EmployeeName =?', (update_salary,int(update_days), current_employee))
                conn.commit()
                conn.close()
                employees_list.delete(0, END)
                getData()
                name_entry.delete(0, 'end')
                salary_entry.delete(0, 'end')
                Days_entry.delete(0,'end')

        def deleteStock():
            delete_name = name_entry.get()
            if name_entry.index("end") == 0 and salary_entry.index("end") == 0 and Days_entry.index("end"):
                error_label = Label(employees_window, text="at least one of the fields are empty", fg="red")
                employees_window.after(2000, lambda: error_label.destroy())
                error_label.pack()
            else:
                conn = sqlite3.connect('Comp Science.db')
                cursor = conn.cursor()
                cursor.execute('DELETE FROM Product WHERE ProductName = ?', (delete_name,))
                conn.commit()
                conn.close()
                employees_list.delete(0, END)
                getData()
                name_entry.delete(0, 'end')
                salary_entry.delete(0, 'end')
                Days_entry.delete(0, 'end')
        def back():
            employees_window.destroy()
            SetUp_Window.deiconify()

        select_button = Button(employees_window, text="Select Employee", width=12, height=2, command=select_item)
        select_button.place(x=300, y=260)

        add_employee_btn = Button(employees_window, text="Add Employee", width=12, height=2, command=insert_employee)
        add_employee_btn.place(x=200, y=260)

        Edit_btn = Button(employees_window, text="Edit Employee", width=12, height=2, command=editStock)
        Edit_btn.place(x=300, y=320)

        Delete_btn = Button(employees_window, text="Delete Employee", width=12, height=2, command=deleteStock)
        Delete_btn.place(x=200, y=320)

        back_button = Button(employees_window, text="Back", command=back)
        back_button.place(x=280, y=370)

        getData()
#this function destroys the Set Up window and unhides the root window
    def BackClicked():
        SetUp_Window.destroy()
        root.deiconify()

#this creates the tkinter window called Set Up with a geometry of 500x400
    SetUp_Window = Tk()
    SetUp_Window.resizable(False, False)
    SetUp_Window.title("Set Up")
    SetUp_Window.geometry("500x400")
    SetUp_Window.configure(bg='grey')
#this creates a button with a name of inventory
    Inventory_btn = Button(SetUp_Window, text="Inventory", height=5, width=25, command=InventoryClicked)
    Inventory_btn.place(x=50,y=150)
#this creates a button with a name of employee
    Employee_btn = Button(SetUp_Window, text="Employee", height=5, width=25, command=EmployeeClicked)
    Employee_btn.place(x=250,y=150)
#this creates a button with a name of back
    Back_btn = Button(SetUp_Window, text="Back", height=2, width=15,command=BackClicked)
    Back_btn.pack()
    
#function that holds everything to do with the dashboard window
def ContinueClicked():
    root.withdraw()
    def dashboard_sales():
        sales_window = Tk()
        sales_window.resizable(False, False)
        sales_window.title('Employees')
        sales_window.geometry("200x150")

        startDate_lbl = Label(sales_window, text="enter the start month: ",)
        startDate_lbl.pack()
        startDate_entry = Entry(sales_window)
        startDate_entry.pack()
        endDate_lbl = Label(sales_window, text="enter the end month: ",)
        endDate_lbl.pack()
        endDate_entry = Entry(sales_window)
        endDate_entry.pack()

        def generateGraph():
            sales_window.withdraw()
            dic = {}
            date = []
            cost = []
            edit_date = []
            edit_cost = []
            start_date = startDate_entry.get()
            end_date = endDate_entry.get()

            conn = sqlite3.connect('Comp Science.db')
            cursor = conn.cursor()
            cursor.execute('''SELECT OrderID FROM Orders WHERE OrderDate = (?)''', (start_date,))
            first = cursor.fetchone()[0]
            cursor.execute('''SELECT OrderID FROM Orders WHERE OrderDate = (?)''', (end_date,))
            last = cursor.fetchone()[0]
            cursor.execute('''SELECT OrderDate, TotalBill FROM Orders WHERE OrderID >= (?) and OrderID <= (?) ''',(first, last))
            order_data = cursor.fetchall()
            print(order_data)
            n=0
            for i in order_data:
                a, b = tuple(i)
                date.append(a)
                cost.append(b)
                
            while n < len(date)-1:
                if date[n] == date[n+1]:
                    first_date = date.pop(n)
                    first_cost = cost.pop(n)
                    second_cost = cost.pop(n)
                    total_cost = (first_cost + second_cost)
                    print(total_cost)
                    cost = [total_cost] + cost
                    edit_date.append(first_date)
                    edit_cost.append(total_cost)
                    dic.update({edit_date[n]: edit_cost[n]})
                else:
                    print("no")
                n = n+1
                dic.update({date[n] : cost[n]})
            print(dic)

                
            dates = list(dic.keys())
            bills = list(dic.values())
            print(dates)
            print(bills)
            plt.bar(dates, bills, 0.6)
            plt.show()


        gen_btn = Button(sales_window, text="generate it", width=10, height=2, command=generateGraph)
        gen_btn.pack()


    def dashboard_orders():
        dashboard.withdraw()

        order_window = Tk()
        order_window.resizable(False, False)
        order_window.title('Employees')
        order_window.geometry("600x500")

        date_label = Label(order_window, text="Date:")
        date_label.place(x=10,y=30)
        date_entry = Entry(order_window)
        date_entry.place(x=10,y=60)

        customer_label = Label(order_window, text="Customer Name:")
        customer_label.place(x=10,y=80)
        customer_entry = Entry(order_window)
        customer_entry.place(x=10,y=100)

        total_amount_label = Label(order_window, text="Total Amount:")
        total_amount_label.place(x=150,y=80)
        total_amount_entry = Entry(order_window)
        total_amount_entry.place(x=150,y=100)

        cost_label = Label(order_window, text="Total Bill:")
        cost_label.place(x=300,y=30)
        cost_entry = Entry(order_window)
        cost_entry.place(x=300,y=60)

        order_tree = ttk.Treeview(order_window, columns=['orderID', 'Date', 'Customer Name', 'Total Amount','Items'])
        order_tree.heading('#0',text="")
        order_tree.column('#0', width=0)
        order_tree.heading('orderID', text='Order ID')
        order_tree.column('orderID', width=100)
        order_tree.heading('Date', text='Date')
        order_tree.column('Date', width=100)
        order_tree.heading('Customer Name', text='Customer Name')
        order_tree.column('Customer Name', width=100)
        order_tree.heading('Total Amount', text='Total Bills')
        order_tree.column('Total Amount', width=150) 
        order_tree.heading('Items', text='Items')
        order_tree.column('Items', width=100)

        def getTreeData():
            conn = sqlite3.connect('Comp Science.db')
            cursor = conn.cursor()
            
            cursor.execute('''SELECT * FROM Orders''')
            orderData = cursor.fetchall()
            for rows in orderData:
                (OrderID, OrderDate, TotalBill, CustomerName, Items) = tuple(rows)
                order_tree.insert('',END, values=(OrderID, OrderDate, CustomerName, TotalBill, Items))
            conn.commit()
            conn.close()
        getTreeData()

        def select_item():
            global amount
            selected_item = order_tree.focus()
            details = order_tree.item(selected_item)
            productname = details.get('values')
            data = []
            for item in productname:
                print(item)
                data.append(item)
                
            items = data[4]
            bought, amount = items.split("-")
            amount =int(amount)
            date_entry.delete(0, 'end')
            customer_entry.delete(0, 'end')
            total_amount_entry.delete(0, 'end')
            cost_entry.delete(0, 'end')
            box.delete(0, 'end')
            date_entry.insert(0, data[1])
            customer_entry.insert(0, data[2])
            total_amount_entry.insert(0, amount)
            cost_entry.insert(0, data[3])
            box.insert(0, bought)
            
        def insert():
            date = date_entry.get()
            cost = cost_entry.get()
            customer = customer_entry.get()
            item_name = box.get()
            total_amount = int(total_amount_entry.get())
            item = f"{item_name}-{total_amount}"
            if date and customer and total_amount:  # Check if both date, customer and total amount fields are not empty 
                conn = sqlite3.connect('Comp Science.db')
                cursor = conn.cursor()
                
                cursor.execute('''SELECT StockQuantity FROM  Product WHERE ProductName = ?''', (item_name,))
                currentStock = int(cursor.fetchone()[0])
                newStock = int(currentStock-total_amount)
                while newStock > 0:
                    cursor.execute('''UPDATE Product SET (StockQuantity) = (?) WHERE ProductName = ?''', (newStock, item_name))
                    # Create a table if it doesn't exist
                    cursor.execute('''CREATE TABLE IF NOT EXISTS Orders (OrderID INTEGER PRIMARY KEY, OrderDate INTEGER, TotalBill REAL, CustomerName TEXT, Items TEXT)''')
                    
                    stock_data = [
                        (date, cost, customer, item)
                    ]
                    for user in stock_data:   
                        cursor.execute('INSERT INTO Orders (OrderDate, TotalBill, CustomerName, Items) VALUES (?, ?, ?, ?)', user)
                        
                    # Commit changes and close the connection
                    conn.commit()
                    conn.close()
                    
                    conn = sqlite3.connect('Comp Science.db')
                    cursor = conn.cursor()
                
                    cursor.execute('''SELECT * FROM Orders WHERE OrderID=(SELECT max(OrderID) FROM Orders)''')
                    lastOrder = cursor.fetchone()
                    (OrderID, OrderDate, TotalBill, CustomerName, Items) = lastOrder
                    order_tree.insert('',END, values=(OrderID, OrderDate, CustomerName, TotalBill, Items)) 
                    conn.commit()
                    conn.close()
                    break 
                else:
                    print("you have not got enough of those left in stock")
                # Clear the input fields after adding an employee
                date_entry.delete(0, 'end')
                customer_entry.delete(0, 'end')
                total_amount_entry.delete(0, 'end')
                cost_entry.delete(0, 'end')
                box.delete(0, 'end')
                
        def edit():
            global nam
            global amount
            date = str(date_entry.get())
            cost = float(cost_entry.get())
            customer = str(customer_entry.get())
            item_name = box.get()
            total_amount = int(total_amount_entry.get())
            item = f"{item_name}-{total_amount}"

            conn = sqlite3.connect('Comp Science.db')
            cursor = conn.cursor()

            cursor.execute('''SELECT StockQuantity FROM  Product WHERE ProductName = ?''', (item_name,))
            oldstock = int(cursor.fetchone()[0])
            stock = (oldstock + amount)
            cursor.execute('''UPDATE Product SET (StockQuantity) = (?) WHERE ProductName = ?''', (stock, item_name))
            cursor.execute('''SELECT StockQuantity FROM  Product WHERE ProductName = ?''', (item_name,))
            currentStock = int(cursor.fetchone()[0])
            newStock = int(currentStock-total_amount)

            
            while newStock > 0:
                cursor.execute('''UPDATE Product SET (StockQuantity) = (?) WHERE ProductName = ?''', (newStock, item_name))
                
                cursor.execute('''SELECT OrderID FROM Orders WHERE CustomerName = (?) ''', (nam,))
                orderID = int(cursor.fetchone()[0])
                
                cursor.execute('''UPDATE Orders SET (OrderDate, TotalBill, CustomerName, Items) =(?,?,?,?) WHERE OrderID = ?''', (date, cost, customer, item, orderID))
                
                conn.commit()
                conn.close()
                

                
                order_tree.delete(*order_tree.get_children())
                getTreeData()
                date_entry.delete(0, 'end')
                customer_entry.delete(0, 'end')
                total_amount_entry.delete(0, 'end')
                cost_entry.delete(0, 'end')
                box.delete(0, 'end')    
                break
            else:
                error_label = Label(order_window, text="There is not that much stock left", fg="red")
                error_label.pack()
                order_window.after(2000, lambda: error_label.destroy())
                conn.close()
            
        def deleteStock():
            global nam
            conn = sqlite3.connect('Comp Science.db')
            cursor = conn.cursor()
            
            cursor.execute('''SELECT OrderID FROM Orders WHERE CustomerName = (?) ''', (nam,))
            orderID = int(cursor.fetchone()[0])
            
            cursor.execute('''DELETE FROM Orders WHERE OrderID = ?''', (orderID,))
            
            conn.commit()
            conn.close()
            
            order_tree.delete(*order_tree.get_children())
            getTreeData()
            date_entry.delete(0, 'end')
            customer_entry.delete(0, 'end')
            total_amount_entry.delete(0, 'end')
            cost_entry.delete(0, 'end')
            box.delete(0, 'end')
            
        def getName():
            global nam
            nam = customer_entry.get()
            print(nam)

        def back():
            order_window.destroy()
            dashboard.deiconify()
            
            
        order_tree.place(x=8, y=200)

        add_order = Button(order_window, text="add order", width=12, height=2,command=insert)
        add_order.place(x=310,y=90)

        select_button = Button(order_window, text="Select Item", width=10, height=2,command=lambda:(select_item(), getName()))
        select_button.place(x=440, y=20)

        Edit_btn = Button(order_window, text="Edit Stock", width=10, height=2,command=edit)
        Edit_btn.place(x=440, y=60)

        Delete_btn = Button(order_window, text="Delete Stock", width=10, height=2, command=lambda:(deleteStock(), getName()))
        Delete_btn.place(x=440, y=100)

        back_btn = Button(order_window, text="back", width=12, height=2, command=back)
        back_btn.place(x=450, y=450)
        #gets the data from the product table to fill up the combobox with options  
        conn = sqlite3.connect('Comp Science.db')
        cursor = conn.cursor()
        cursor.execute('''SELECT ProductName FROM Product''')

        options =[]

        for i in cursor.fetchall():
            options.append(i[0])

        select_lbl = Label(order_window, text="item bought: ")
        select_lbl.place(x=150,y=30)

        box = ttk.Combobox(order_window, values=options)
        box.place(x=150,y=60)
        conn.commit()
        conn.close()


    def dashboard_employees():
        dashboard.withdraw()

        # Create the employees window
        employees_window = Tk()
        employees_window.title('Employees')
        employees_window.geometry("600x400")

        # Create input fields for the user to enter employee details
        name_label = Label(employees_window, text="Name:")
        name_label.pack()
        name_entry = Entry(employees_window)
        name_entry.pack()

        salary_label = Label(employees_window, text="Salary:")
        salary_label.pack()
        salary_entry = Entry(employees_window)
        salary_entry.pack()

        Days_label = Label(employees_window, text="Days:")
        Days_label.pack()
        Days_entry = Entry(employees_window)
        Days_entry.pack()
        myFrame = Frame(employees_window)
        myScrollbar = Scrollbar(myFrame, orient=VERTICAL)
        # Create a Listbox to display the employees
        employees_list = Listbox(myFrame, width=0,height=8, yscrollcommand=myScrollbar.set)

        myScrollbar.config(command=employees_list.yview)
        myScrollbar.pack(side=RIGHT, fill=Y)
        myFrame.pack()

        employees = []
        for employee in employees:
            employees_list.insert(END, employee)
        employees_list.pack()

        # Function to insert the user input as a new employee
        def insert_employee():
            name = name_entry.get()
            salary = salary_entry.get()
            Days = Days_entry.get()
            if name and salary:  # Check if both name and salary fields are not empty
                new_employee = name + " - " + salary + " - " + Days
                employees_list.insert(END, new_employee)
                conn = sqlite3.connect('Comp Science.db')
                cursor = conn.cursor()

                # Create a table if it doesn't exist
                cursor.execute('''CREATE TABLE IF NOT EXISTS Product
                                (EmployeeID INTEGER PRIMARY KEY, EmployeeName TEXT, EmployeePay INTEGER, EmployeeDays INTEGER NOT NULL)''')
                
                stock_data = [
                    (name, salary, Days)
                ]
                for user in stock_data:   
                    cursor.execute('INSERT INTO Employee (EmployeeName, EmployeePay, EmployeeDays) VALUES (?, ?, ?)', user)
                    
                # Commit changes and close the connection
                conn.commit()
                conn.close()

                # Clear the input fields after adding an employee
                name_entry.delete(0, 'end')
                salary_entry.delete(0, 'end')
                Days_entry.delete(0, 'end')
            else:
                # Display an error message if either name or salary field is empty
                error_label = Label(employees_window, text="Both name and salary fields are required", fg="red")
                employees_window.after(2000, lambda: error_label.destroy())
                error_label.pack()
        # Create the "Add Employee" button to add the input to the Listbox
        def select_item():
            selected_item = str(employees_list.get(employees_list.curselection()))
            name, salary, days = selected_item.split(" - ")
            name_entry.delete(0, 'end')
            salary_entry.delete(0, 'end')
            Days_entry.delete(0, 'end')
            name_entry.insert(0, name)
            salary_entry.insert(0, salary)
            Days_entry.insert(0, days)
        def getData():
            conn = sqlite3.connect('Comp Science.db')
            cursor = conn.cursor()
            cursor.execute('''SELECT EmployeeName, EmployeePay, EmployeeDays FROM Employee''')
            listData = cursor.fetchall()
            for row in listData:
                (EmployeeName, EmployeePay, EmployeeDays) = tuple(row)
                employees_list.insert(END, f"{EmployeeName} - {EmployeePay} - {EmployeeDays}")

        def editStock():
            current_employee = name_entry.get()
            update_salary = salary_entry.get()
            update_days = Days_entry.get()
            
            if name_entry.index("end") == 0 and salary_entry.index("end") == 0 and Days_entry.index("end"):
                error_label = Label(employees_window, text="at least one of the fields are empty", fg="red")
                employees_window.after(2000, lambda: error_label.destroy())
                error_label.pack()
            else:
                conn = sqlite3.connect('Comp Science.db')
                cursor = conn.cursor()
                cursor.execute('UPDATE Employee SET (EmployeePay, EmployeeDays) =(?, ?) WHERE EmployeeName =?', (update_salary,int(update_days), current_employee))
                conn.commit()
                conn.close()
                employees_list.delete(0, END)
                getData()
                name_entry.delete(0, 'end')
                salary_entry.delete(0, 'end')
                Days_entry.delete(0,'end')

        def deleteStock():
            delete_name = name_entry.get()
            if name_entry.index("end") == 0 and salary_entry.index("end") == 0 and Days_entry.index("end"):
                error_label = Label(employees_window, text="at least one of the fields are empty", fg="red")
                employees_window.after(2000, lambda: error_label.destroy())
                error_label.pack()
            else:
                conn = sqlite3.connect('Comp Science.db')
                cursor = conn.cursor()
                cursor.execute('DELETE FROM Product WHERE ProductName = ?', (delete_name,))
                conn.commit()
                conn.close()
                employees_list.delete(0, END)
                getData()
                name_entry.delete(0, 'end')
                salary_entry.delete(0, 'end')
                Days_entry.delete(0, 'end')
        def back():
            employees_window.destroy()
            dashboard.deiconify()

        select_button = Button(employees_window, text="Select Employee", width=12, height=2, command=select_item)
        select_button.place(x=300, y=260)

        add_employee_btn = Button(employees_window, text="Add Employee", width=12, height=2, command=insert_employee)
        add_employee_btn.place(x=200, y=260)

        Edit_btn = Button(employees_window, text="Edit Employee", width=12, height=2, command=editStock)
        Edit_btn.place(x=300, y=320)

        Delete_btn = Button(employees_window, text="Delete Employee", width=12, height=2, command=deleteStock)
        Delete_btn.place(x=200, y=320)

        back_button = Button(employees_window, text="Back", command=back)
        back_button.place(x=280, y=370)

        getData()
    def dashboard_inventory():
        dashboard.withdraw()
        Inventory_window = Tk()
        Inventory_window.resizable(False, False)
        Inventory_window.title("Inventory")
        Inventory_window.geometry("500x400")
        Inventory_window.configure(bg='grey')

        def select_item():
            selected_item = str(stock_list.get(stock_list.curselection()))
            item, quantity = selected_item.split(" - ")
            item_entry.delete(0, 'end')
            quantity_entry.delete(0, 'end')
            item_entry.insert(0, item)
            quantity_entry.insert(0, quantity)
            
        def getData():
            conn = sqlite3.connect('Comp Science.db')
            cursor = conn.cursor()
            cursor.execute('''SELECT ProductName, StockQuantity FROM Product''')
            listData = cursor.fetchall()
            for row in listData:
                (ProductName, StockQuantity) = tuple(row)
                stock_list.insert(END, f"{ProductName} - {StockQuantity}")

        stock_list = Listbox(Inventory_window)
        stock_list.pack()

        def addStock():
            new_stock = item_entry.get()
            new_quantity = quantity_entry.get()
            if item_entry.index("end") == 0 and quantity_entry.index("end") == 0:
                error_label = Label(Inventory_window, text="at least one of the fields are empty", fg="red")
                Inventory_window.after(2000, lambda: error_label.destroy())
                error_label.pack()
            else:
                stock_list.insert(END,new_stock + " - " + new_quantity)
                item_entry.delete(0, 'end')
                quantity_entry.delete(0, 'end')

                conn = sqlite3.connect('Comp Science.db')
                cursor = conn.cursor()

                # Create a table if it doesn't exist
                cursor.execute('''CREATE TABLE IF NOT EXISTS Product
                                (ProductID INTEGER PRIMARY KEY, ProductName TEXT, CategoryID INTEGER, StockQuantity INTEGER NOT NULL)''')
                
                stock_data = [
                    (new_stock, new_quantity)
                ]
                for user in stock_data:   
                    cursor.execute('INSERT INTO Product (ProductName, StockQuantity) VALUES (?, ?)', user)
                    
                # Commit changes and close the connection
                conn.commit()
                conn.close()

        def editStock():
            current_stock = item_entry.get()
            update_quantity = quantity_entry.get()
            if item_entry.index("end") == 0 and quantity_entry.index("end") == 0:
                error_label = Label(Inventory_window, text="at least one of the fields are empty", fg="red")
                Inventory_window.after(2000, lambda: error_label.destroy())
                error_label.pack()
            else:
                conn = sqlite3.connect('Comp Science.db')
                cursor = conn.cursor()
                cursor.execute('UPDATE Product SET StockQuantity =? WHERE ProductName =?', (int(update_quantity), current_stock))
                conn.commit()
                conn.close()
                stock_list.delete(0, END)
                getData()
                item_entry.delete(0, 'end')
                quantity_entry.delete(0, 'end')

        def deleteStock():
            delete_name = item_entry.get()
            if item_entry.index("end") == 0 and quantity_entry.index("end") == 0:
                error_label = Label(Inventory_window, text="at least one of the fields are empty", fg="red")
                Inventory_window.after(2000, lambda: error_label.destroy())
                error_label.pack()
            else:
                conn = sqlite3.connect('Comp Science.db')
                cursor = conn.cursor()
                cursor.execute('DELETE FROM Product WHERE ProductName = ?', (delete_name,))
                conn.commit()
                conn.close()
                stock_list.delete(0, END)
                getData()
                item_entry.delete(0, 'end')
                quantity_entry.delete(0, 'end')
        def back():
            Inventory_window.destroy()
            dashboard.deiconify()

        item_label = Label(Inventory_window, text="Item:", bg="grey")
        item_label.pack()

        item_entry = Entry(Inventory_window)
        item_entry.pack()

        quantity_label = Label(Inventory_window, text="Quantity:", bg="grey")
        quantity_label.pack()

        quantity_entry = Entry(Inventory_window)
        quantity_entry.pack()

        select_button = Button(Inventory_window, text="Select Item", width=10, height=2, command=select_item)
        select_button.place(x=260, y=260)

        add_btn = Button(Inventory_window, text="Add Stock", width=10, height=2, command=addStock)
        add_btn.place(x=160, y=260)

        Edit_btn = Button(Inventory_window, text="Edit Stock", width=10, height=2, command=editStock)
        Edit_btn.place(x=260, y=320)

        Delete_btn = Button(Inventory_window, text="Delete Stock", width=10, height=2, command=deleteStock)
        Delete_btn.place(x=160, y=320)

        back_btn = Button(Inventory_window, text="Back", width=10, height=2, command=back)
        back_btn.place(x=410, y=355)

        getData()
    #function that runs when the back button widget is pressed
    def backPressed():
        dashboard.destroy()
        root.deiconify()
 #this creates the tkinter window called Set Up with a geometry of 500x400       
    dashboard = Tk()
    dashboard.resizable(False,False)
    dashboard.title("dashboard")
    dashboard.geometry("500x400")
    dashboard.configure(bg='grey')
    
    sales = Button(dashboard, text="  Sales  ", bg='#8bc1f7', height=2, width=15, command=dashboard_sales)
    sales.place(x=90, y=100)
    
    orders = Button(dashboard, text=" Orders ", bg='#8bc1f7', height=2, width=15, command=dashboard_orders)
    orders.place(x=300, y=100)
    
    Employees = Button(dashboard, text="Employees", bg='#8bc1f7', height=2, width=15, command=dashboard_employees)
    Employees.place(x=90, y=200)
    
    Inventory = Button(dashboard, text="Inventory", bg='#8bc1f7', height=2, width=15, command=dashboard_inventory)
    Inventory.place(x=300, y=200)
    
    back_btn = Button(dashboard, text="back",height=2, width=15, command=backPressed)
    back_btn.place(x=120, y=350)
    
    Exit_btn = Button(dashboard, text="Exit", height=2, width=15, command=root.quit)
    Exit_btn.place(x=270, y=350)

    
#creates the root window(main window)
root = Tk()
root.resizable(False,False)
root.title('WelcomePage')
root.geometry("500x400")
root.configure(bg='grey')

Welcome_Lbl = Label(root, text="This is the Welcome Page please choose Set Up if this is your first use \n If not then Continue: ")
Welcome_Lbl.place(x=56,y=100)

SetUp_Btn = Button(root, text="Set Up", height=5, width=25,command=SetUp_Clicked)
SetUp_Btn.place(x=50,y=150)

Continue_Btn = Button(root, text="continue", height=5, width=25, command=ContinueClicked)
Continue_Btn.place(x=250,y=150)

exit_btn = Button(root, text="Exit", height=2, width=15, command=quit)
exit_btn.place(x=190, y=350)



mainloop()


