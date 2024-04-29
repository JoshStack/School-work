#imports all of the python liberys I will need
from tkinter import *
from tkinter import ttk
import sqlite3
import matplotlib.pyplot as plt
import re

#this function contains everything to do with the set up window
def SetUp_Clicked():
    # Hide the root window
    root.withdraw()
    # Connect to the SQLite database
    conn = sqlite3.connect('Comp Science.db')
    cursor = conn.cursor()
    # Retrieve email from the Customer table
    cursor.execute('SELECT email FROM Customer')
    customerid = str(cursor.fetchone())    
    # Commit changes and close the connection
    conn.commit()
    conn.close()
    # Loop to check if customer email exists
    while customerid == 'None':
        # Create a new window for email entry
        email_window = Tk()
        email_window.resizable(False, False)
        email_window.title("email")
        email_window.geometry("200x180")
        email_window.configure(bg='grey')
        
        # Label and entry field for email input
        email_Lbl = Label(email_window, text="Enter you email: ", bg="grey")
        email_Lbl.place(x=20,y=50)
        email_ent = Entry(email_window,width=0)
        email_ent.place(x=20,y=70)
        # Function to submit email
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
        # Button to submit email
        submit_btn = Button(email_window, text="submit", command=submit)
        submit_btn.place(x=20,y=95)
        # Break the loop
        break

    # Function to open Inventory window
    def InventoryClicked():
        SetUp_Window.withdraw()
        
        # Create the Inventory window
        Inventory_window = Tk()
        Inventory_window.resizable(False, False)
        Inventory_window.title("Inventory")
        Inventory_window.geometry("500x400")
        Inventory_window.configure(bg='grey')
        
        # Create a Listbox to display inventory items
        stock_list = Listbox(Inventory_window)
        stock_list.pack()

        # Function to select item from inventory
        def select_item():
            try:
                selected_item = str(stock_list.get(stock_list.curselection()))
                item, quantity = selected_item.split(" - ")
                item_entry.delete(0, 'end')
                quantity_entry.delete(0, 'end')
                item_entry.insert(0, item)
                quantity_entry.insert(0, quantity)
            except:
                error_label = Label(Inventory_window, text="nothing is being selected", fg="red")
                Inventory_window.after(4000, lambda: error_label.destroy())
                error_label.pack()
        # Function to get data from the database and populate the Listbox
        def getData():
            conn = sqlite3.connect('Comp Science.db')
            cursor = conn.cursor()
            cursor.execute('''SELECT ProductName, StockQuantity FROM Product''')
            listData = cursor.fetchall()
            for row in listData:
                (ProductName, StockQuantity) = tuple(row)
                stock_list.insert(END, f"{ProductName} - {StockQuantity}")

        # Function to add new stock
        def addStock():
            new_stock = item_entry.get()
            new_quantity = quantity_entry.get()
            if new_stock and new_quantity:
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
                        
                        stock_data = [(new_stock, new_quantity)]
                        for user in stock_data:   
                            cursor.execute('INSERT INTO Product (ProductName, StockQuantity) VALUES (?, ?)', user)
                        
                        # Commit changes and close the connection
                        conn.commit()
                        conn.close()
                        
                        stock_list.insert(END,new_stock + " - " + new_quantity)

                    except:
                        error_label = Label(Inventory_window, text="Value is already in the database", fg="red")
                        Inventory_window.after(4000, lambda: error_label.destroy())
                        error_label.pack()
            else:
                error_label = Label(Inventory_window, text="One of the fields are empty", fg="red")
                Inventory_window.after(4000, lambda: error_label.destroy())
                error_label.pack()
        
        # Function to edit existing stock
        def editStock():
            current_stock = item_entry.get()
            update_quantity = quantity_entry.get()
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
        
        # Function to delete existing stock
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
        
        # Function to navigate back to the main window
        def back():
            Inventory_window.destroy()
            SetUp_Window.deiconify()

        # Labels and entry fields for item and quantity
        item_label = Label(Inventory_window, text="Item:", bg="grey")
        item_label.pack()

        item_entry = Entry(Inventory_window)
        item_entry.pack()

        quantity_label = Label(Inventory_window, text="Quantity:", bg="grey")
        quantity_label.pack()

        quantity_entry = Entry(Inventory_window)
        quantity_entry.pack()

        # Buttons for selecting, adding, editing, and deleting stock
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

        # Get data from database and populate Listbox
        getData()

    # Function to handle Employee button click
    def EmployeeClicked():
        SetUp_Window.withdraw()

        # Create the employees window
        employees_window = Tk()
        employees_window.resizable(False, False)
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
                if name.isdigit() or salary.isdigit() == False or (Days.isdigit() == False or (int(Days) < 0 or 7 < int(Days))) :
                    error_label = Label(employees_window, text="One of the fields is inputted incorrectly", fg="red")
                    employees_window.after(2000, lambda: error_label.destroy())
                    error_label.pack()
                else:
                    try:
                        conn = sqlite3.connect('Comp Science.db')
                        cursor = conn.cursor()

                        # Create a table if it doesn't exist
                        cursor.execute('''CREATE TABLE IF NOT EXISTS Product
                                        (EmployeeID INTEGER PRIMARY KEY, EmployeeName TEXT, EmployeePay INTEGER, EmployeeDays INTEGER NOT NULL)''')
                        
                        stock_data = [(name, salary, Days)]
                        for user in stock_data:   
                            cursor.execute('INSERT INTO Employee (EmployeeName, EmployeePay, EmployeeDays) VALUES (?, ?, ?)', user)
                        
                        # Commit changes and close the connection
                        conn.commit()
                        conn.close()
                        
                        new_employee = name + " - " + salary + " - " + Days
                        employees_list.insert(END, new_employee)
                        # Clear the input fields after adding an employee
                        name_entry.delete(0, 'end')
                        salary_entry.delete(0, 'end')
                        Days_entry.delete(0, 'end')
                    except:
                        error_label = Label(employees_window, text="There is a duplicate", fg="red")
                        employees_window.after(2000, lambda: error_label.destroy())
                        error_label.pack()                              
            else:
                # Display an error message if either name or salary field is empty
                error_label = Label(employees_window, text="One of the fields are missing", fg="red")
                employees_window.after(2000, lambda: error_label.destroy())
                error_label.pack()

        # Create the "select" button to add the data to the entry boxes
        def select_item():
            try:
                selected_item = str(employees_list.get(employees_list.curselection()))
                name, salary, days = selected_item.split(" - ")
                name_entry.delete(0, 'end')
                salary_entry.delete(0, 'end')
                Days_entry.delete(0, 'end')
                name_entry.insert(0, name)
                salary_entry.insert(0, salary)
                Days_entry.insert(0, days)
            except:
                error_label = Label(employees_window, text="Nothing is being selected", fg="red")
                employees_window.after(2000, lambda: error_label.destroy())
                error_label.pack()
        
        # Function to get data from the database and populate the Listbox
        def getData():
            conn = sqlite3.connect('Comp Science.db')
            cursor = conn.cursor()
            cursor.execute('''SELECT EmployeeName, EmployeePay, EmployeeDays FROM Employee''')
            listData = cursor.fetchall()
            for row in listData:
                (EmployeeName, EmployeePay, EmployeeDays) = tuple(row)
                employees_list.insert(END, f"{EmployeeName} - {EmployeePay} - {EmployeeDays}")

        # Function to edit existing employee
        def edit_employee():
            current_employee = name_entry.get()
            update_salary = salary_entry.get()
            update_days = Days_entry.get()
            
            if current_employee or update_days or update_salary:
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
            else:
                error_label = Label(employees_window, text="At least one of the fields are empty", fg="red")
                employees_window.after(2000, lambda: error_label.destroy())
                error_label.pack()

        # Function to delete existing employee
        def delete_Employee():
            delete_name = name_entry.get()
            if delete_name:
                conn = sqlite3.connect('Comp Science.db')
                cursor = conn.cursor()
                cursor.execute('DELETE FROM Employee WHERE EmployeeName = ?', (delete_name,))
                conn.commit()
                conn.close()
                employees_list.delete(0, END)
                getData()
                name_entry.delete(0, 'end')
                salary_entry.delete(0, 'end')
                Days_entry.delete(0, 'end')
            else:
                error_label = Label(employees_window, text="At least one of the fields are empty", fg="red")
                employees_window.after(2000, lambda: error_label.destroy())
                error_label.pack()

        # Function to navigate back to the main window
        def back():
            employees_window.destroy()
            SetUp_Window.deiconify()

        # Buttons for selecting, adding, editing, and deleting employees
        select_button = Button(employees_window, text="Select Employee", width=12, height=2, command=select_item)
        select_button.place(x=300, y=260)

        add_employee_btn = Button(employees_window, text="Add Employee", width=12, height=2, command=insert_employee)
        add_employee_btn.place(x=200, y=260)

        Edit_btn = Button(employees_window, text="Edit Employee", width=12, height=2, command=edit_employee)
        Edit_btn.place(x=300, y=320)

        Delete_btn = Button(employees_window, text="Delete Employee", width=12, height=2, command=delete_Employee)
        Delete_btn.place(x=200, y=320)

        back_button = Button(employees_window, text="Back", command=back)
        back_button.place(x=280, y=370)

        # Get data from database and populate Listbox
        getData()

    # Function to handle Back button click
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
        # Create a Tkinter window
        sales_window = Tk()
        # Prevent the window from being resizable
        sales_window.resizable(False, False)
        # Set the title of the window
        sales_window.title('Employees')
        # Set the dimensions of the window
        sales_window.geometry("200x150")
        # Connect to the SQLite database
        conn = sqlite3.connect("Comp Science.db")
        # Create a cursor object to execute SQL queries
        cursor = conn.cursor()
        # Retrieve all OrderDates from the Orders table
        cursor.execute('''SELECT OrderDate From Orders''')
        all_dates = cursor.fetchall()

        # Create labels and comboboxes for start and end dates
        startDate_lbl = Label(sales_window, text="enter the start month: ")
        startDate_lbl.pack()
        startDate_entry = ttk.Combobox(sales_window, values=all_dates, state="readonly")
        startDate_entry.pack()
        endDate_lbl = Label(sales_window, text="enter the end month: ")
        endDate_lbl.pack()
        endDate_entry = ttk.Combobox(sales_window, values=all_dates, state="readonly")
        endDate_entry.pack()

        # Define a function to generate a graph
        def generateGraph():
            # Hide the sales window
            sales_window.withdraw()
            
            # Initialize dictionaries and lists
            dic = {}
            date = []
            cost = []
            edit_date = []
            edit_cost = []
            
            # Get start and end dates from the comboboxes
            start_date = startDate_entry.get()
            end_date = endDate_entry.get()
            
            try:
                # Connect to the SQLite database
                conn = sqlite3.connect('Comp Science.db')
                
                # Create a cursor object to execute SQL queries
                cursor = conn.cursor()
                
                # Retrieve the first OrderID corresponding to the start date
                cursor.execute('''SELECT OrderID FROM Orders WHERE OrderDate = (?)''', (start_date,))
                first = cursor.fetchone()[0]
                
                # Retrieve the last OrderID corresponding to the end date
                cursor.execute('''SELECT OrderID FROM Orders WHERE OrderDate = (?)''', (end_date,))
                last = cursor.fetchone()[0]
                
                # Retrieve OrderDates and TotalBill from Orders within the specified range
                cursor.execute('''SELECT OrderDate, TotalBill FROM Orders WHERE OrderID >= (?) and OrderID <= (?) ''',(first, last))
                order_data = cursor.fetchall()
                print(order_data)
                
                # Extract OrderDates and TotalBills into separate lists
                for i in order_data:
                    a, b = tuple(i)
                    date.append(a)
                    cost.append(b)
                print(len(date)-1)
                
                # Merge TotalBills for orders on the same date
                n=0
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
                        dic.update({date[n] : cost[n]})
                    n = n+1
                
                # Update the dictionary with the remaining data
                dic.update({date[n] : cost[n]})
                
                # Separate dates and bills into lists
                dates = list(dic.keys())
                bills = list(dic.values())
                print(dates)
                print(bills)
                
                # Plot the graph
                plt.bar(dates, bills, 0.6)
                plt.show()
                
            except:
                # Show the sales window if an error occurs
                sales_window.deiconify()
                
                # Create an error message window
                error_window = Tk()
                error_window.resizable(False, False)
                error_window.geometry("200x50")
                error_window.title("Error Message")
                
                # Display error message
                error_label = Label(error_window, text="check the order of the dates", fg="red")
                error_window.after(4000, lambda: error_window.destroy())
                error_label.pack()

        # Create a button to trigger graph generation
        gen_btn = Button(sales_window, text="generate it", width=10, height=2, command=generateGraph)
        gen_btn.pack()


    def dashboard_orders():
        # Hide the dashboard window
        dashboard.withdraw()

        # Create the order window
        order_window = Tk()
        order_window.resizable(False, False)
        order_window.title('Employees')
        order_window.geometry("600x500")

        # Function to clear default text in the date entry field when focused
        def temptext(e):
            date_entry.delete(0,"end")

        # Date entry and label
        date_label = Label(order_window, text="Date:")
        date_label.place(x=10,y=30)
        date_entry = Entry(order_window)
        date_entry.insert(0, "dd/mm/yyyy")  # Default text for date entry
        date_entry.bind("<FocusIn>", temptext)  # Bind the function to clear default text
        date_entry.place(x=10,y=60)

        # Customer name entry and label
        customer_label = Label(order_window, text="Customer Name:")
        customer_label.place(x=10,y=80)
        customer_entry = Entry(order_window)
        customer_entry.place(x=10,y=100)

        # Total amount entry and label
        total_amount_label = Label(order_window, text="Total Amount:")
        total_amount_label.place(x=150,y=80)
        total_amount_entry = Entry(order_window)
        total_amount_entry.place(x=150,y=100)

        # Cost entry and label
        cost_label = Label(order_window, text="Total Bill:")
        cost_label.place(x=300,y=30)
        cost_entry = Entry(order_window)
        cost_entry.place(x=300,y=60)

        # Treeview to display orders
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

        # Function to fetch order data from the database and populate the Treeview
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

        getTreeData()  # Populate the Treeview with order data

        # Function to handle selecting an item from the Treeview
        def select_item():
            global amount
            selected_item = order_tree.focus()
            details = order_tree.item(selected_item)
            productname = details.get('values')
            data = []
            for item in productname:
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
            
        # Function to insert a new order into the database
        def insert():
            date = str(date_entry.get())
            cost = cost_entry.get()
            customer = customer_entry.get()
            item_name = box.get()
            total_amount = total_amount_entry.get()
            item = f"{item_name}-{total_amount}"
            pattern_str = r'^(?:(?:31(\/|-|\.)(?:0?[13578]|1[02]|(?:Jan|Mar|May|Jul|Aug|Oct|Dec)))\1|(?:(?:29|30)(\/|-|\.)(?:0?[1,3-9]|1[0-2]|(?:Jan|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec))\2))(?:(?:1[6-9]|[2-9]\d)?\d{2})$|^(?:29(\/|-|\.)(?:0?2|(?:Feb))\3(?:(?:(?:1[6-9]|[2-9]\d)?(?:0[48]|[2468][048]|[13579][26])|(?:(?:16|[2468][048]|[3579][26])00))))$|^(?:0?[1-9]|1\d|2[0-8])(\/|-|\.)(?:(?:0?[1-9]|(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep))|(?:1[0-2]|(?:Oct|Nov|Dec)))\4(?:(?:1[6-9]|[2-9]\d)?\d{2})$'

            if re.search(pattern_str, date) and cost.isdigit() and customer.isdigit() == False and total_amount.isdigit():
                if date and customer and total_amount and item_name and cost:  # Check if all fields are filled
                    conn = sqlite3.connect('Comp Science.db')
                    cursor = conn.cursor()
                    
                    # Retrieve current stock quantity for the item
                    cursor.execute('''SELECT StockQuantity FROM  Product WHERE ProductName = ?''', (item_name,))
                    currentStock = int(cursor.fetchone()[0])
                    total_amount = int(total_amount)
                    newStock = int(currentStock-total_amount)
                    while newStock > 0:
                        # Update stock quantity for the item
                        cursor.execute('''UPDATE Product SET (StockQuantity) = (?) WHERE ProductName = ?''', (newStock, item_name))
                        # Create Orders table if not exists
                        cursor.execute('''CREATE TABLE IF NOT EXISTS Orders (OrderID INTEGER PRIMARY KEY, OrderDate INTEGER, TotalBill REAL, CustomerName TEXT, Items TEXT)''')
                        
                        # Insert new order into Orders table
                        stock_data = [
                            (date, cost, customer, item)
                        ]
                        for user in stock_data:   
                            cursor.execute('INSERT INTO Orders (OrderDate, TotalBill, CustomerName, Items) VALUES (?, ?, ?, ?)', user)
                            
                        # Commit changes and close the connection
                        conn.commit()
                        conn.close()
                        
                        # Retrieve and display the latest order in the Treeview
                        conn = sqlite3.connect('Comp Science.db')
                        cursor = conn.cursor()
                        cursor.execute('''SELECT * FROM Orders WHERE OrderID=(SELECT max(OrderID) FROM Orders)''')
                        lastOrder = cursor.fetchone()
                        (OrderID, OrderDate, TotalBill, CustomerName, Items) = lastOrder
                        order_tree.insert('',END, values=(OrderID, OrderDate, CustomerName, TotalBill, Items)) 
                        conn.commit()
                        conn.close()
                        
                        # Clear input fields
                        date_entry.delete(0, 'end')
                        customer_entry.delete(0, 'end')
                        total_amount_entry.delete(0, 'end')
                        cost_entry.delete(0, 'end')
                        box.delete(0, 'end')
                        break
                else:
                    print("You have not got enough of those left in stock")
            else:
                # Display error message for invalid input values
                error_label = Label(order_window, text="Please check all input values", fg="red")
                order_window.after(2000, lambda: error_label.destroy())
                error_label.pack()

        # Function to edit an existing order
        def edit():
            global nam
            global amount
            date = date_entry.get()
            cost = cost_entry.get()
            customer = customer_entry.get()
            item_name = box.get()
            total_amount = total_amount_entry.get()
            item = f"{item_name}-{total_amount}" 
            pattern_str = r'^(?:(?:31(\/|-|\.)(?:0?[13578]|1[02]|(?:Jan|Mar|May|Jul|Aug|Oct|Dec)))\1|(?:(?:29|30)(\/|-|\.)(?:0?[1,3-9]|1[0-2]|(?:Jan|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec))\2))(?:(?:1[6-9]|[2-9]\d)?\d{2})$|^(?:29(\/|-|\.)(?:0?2|(?:Feb))\3(?:(?:(?:1[6-9]|[2-9]\d)?(?:0[48]|[2468][048]|[13579][26])|(?:(?:16|[2468][048]|[3579][26])00))))$|^(?:0?[1-9]|1\d|2[0-8])(\/|-|\.)(?:(?:0?[1-9]|(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep))|(?:1[0-2]|(?:Oct|Nov|Dec)))\4(?:(?:1[6-9]|[2-9]\d)?\d{2})$'

            if re.search(pattern_str, date) and cost.isdigit() and customer.isdigit() == False and total_amount.isdigit():
                if date and cost and customer and item_name and total_amount:
                    conn = sqlite3.connect('Comp Science.db')
                    cursor = conn.cursor()

                    # Retrieve old stock quantity for the item
                    cursor.execute('''SELECT StockQuantity FROM  Product WHERE ProductName = ?''', (item_name,))
                    oldstock = int(cursor.fetchone()[0])
                    stock = (oldstock + amount)
                    # Update stock quantity with new amount
                    cursor.execute('''UPDATE Product SET (StockQuantity) = (?) WHERE ProductName = ?''', (stock, item_name))
                    cursor.execute('''SELECT StockQuantity FROM  Product WHERE ProductName = ?''', (item_name,))
                    currentStock = int(cursor.fetchone()[0])
                    newStock = int(currentStock-total_amount)

                    while newStock > 0:
                        # Update stock quantity for the item
                        cursor.execute('''UPDATE Product SET (StockQuantity) = (?) WHERE ProductName = ?''', (newStock, item_name))
                        
                        # Retrieve OrderID associated with customer name
                        cursor.execute('''SELECT OrderID FROM Orders WHERE CustomerName = (?) ''', (nam,))
                        orderID = int(cursor.fetchone()[0])
                        
                        # Update order details in the database
                        cursor.execute('''UPDATE Orders SET (OrderDate, TotalBill, CustomerName, Items) =(?,?,?,?) WHERE OrderID = ?''', (date, cost, customer, item, orderID))
                        
                        # Commit changes and close the connection
                        conn.commit()
                        conn.close()

                        # Update Treeview with edited order
                        order_tree.delete(*order_tree.get_children())
                        getTreeData()
                        date_entry.delete(0, 'end')
                        customer_entry.delete(0, 'end')
                        total_amount_entry.delete(0, 'end')
                        cost_entry.delete(0, 'end')
                        box.delete(0, 'end')    
                        break
                    else:
                        # Display error message if there is not enough stock left
                        error_label = Label(order_window, text="There is not that much stock left", fg="red")
                        error_label.pack()
                        order_window.after(2000, lambda: error_label.destroy())
                        conn.close()
                else:
                    # Display error message if any field is missing
                    error_label = Label(order_window, text="One of the fields is missing", fg="red")
                    order_window.after(2000, lambda: error_label.destroy())
                    error_label.pack()
            else:
                # Display error message for invalid input values
                error_label = Label(order_window, text="Please check all input values", fg="red")
                order_window.after(2000, lambda: error_label.destroy())
                error_label.pack()   

        # Function to delete a selected order from the database
        def deleteStock():
            global nam
            conn = sqlite3.connect('Comp Science.db')
            cursor = conn.cursor()
            
            # Retrieve OrderID associated with customer name
            cursor.execute('''SELECT OrderID FROM Orders WHERE CustomerName = (?) ''', (nam,))
            orderID = int(cursor.fetchone()[0])
            
            # Delete order from Orders table
            cursor.execute('''DELETE FROM Orders WHERE OrderID = ?''', (orderID,))
            
            # Commit changes and close the connection
            conn.commit()
            conn.close()
            
            # Update Treeview after deleting order
            order_tree.delete(*order_tree.get_children())
            getTreeData()
            date_entry.delete(0, 'end')
            customer_entry.delete(0, 'end')
            total_amount_entry.delete(0, 'end')
            cost_entry.delete(0, 'end')
            box.delete(0, 'end')
            
        # Function to get the name of the customer
        def getName():
            global nam
            nam = customer_entry.get()
            print(nam)

        # Function to go back to the dashboard window
        def back():
            order_window.destroy()
            dashboard.deiconify()
            
        # Buttons and labels
        order_tree.place(x=8, y=200)
        add_order = Button(order_window, text="Add Order", width=12, height=2,command=insert)
        add_order.place(x=310,y=90)
        select_button = Button(order_window, text="Select Item", width=10, height=2,command=lambda:(select_item(), getName()))
        select_button.place(x=440, y=20)
        Edit_btn = Button(order_window, text="Edit Stock", width=10, height=2,command=edit)
        Edit_btn.place(x=440, y=60)
        Delete_btn = Button(order_window, text="Delete Stock", width=10, height=2, command=lambda:(deleteStock(), getName()))
        Delete_btn.place(x=440, y=100)
        back_btn = Button(order_window, text="Back", width=12, height=2, command=back)
        back_btn.place(x=450, y=450)
        
        #gets the data from the product table to fill up the combobox with options  
        conn = sqlite3.connect('Comp Science.db')
        cursor = conn.cursor()
        cursor.execute('''SELECT ProductName FROM Product''')

        options =[]

        for i in cursor.fetchall():
            options.append(i[0])
        conn.close()
        
        # Combobox to select items
        select_lbl = Label(order_window, text="Item bought: ")
        select_lbl.place(x=150,y=30)
        box = ttk.Combobox(order_window, values=options, state="readonly")
        box.place(x=150,y=60)
        

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
                if name.isdigit() or salary.isdigit() == False or Days.isdigit() == False and int(Days) in range(1,7):
                    error_label = Label(employees_window, text="One of the fields is inputted incorrectly", fg="red")
                    employees_window.after(2000, lambda: error_label.destroy())
                    error_label.pack()
                else:
                    try:
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
                    except:
                        error_label = Label(employees_window, text="There is a duplicate", fg="red")
                        employees_window.after(2000, lambda: error_label.destroy())
                        error_label.pack()                              
            else:
                # Display an error message if either name or salary field is empty
                error_label = Label(employees_window, text="One of the fields are missing", fg="red")
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
        # Gets all the data from the database
        def getData():
            conn = sqlite3.connect('Comp Science.db')
            cursor = conn.cursor()
            cursor.execute('''SELECT EmployeeName, EmployeePay, EmployeeDays FROM Employee''')
            listData = cursor.fetchall()
            for row in listData:
                (EmployeeName, EmployeePay, EmployeeDays) = tuple(row)
                employees_list.insert(END, f"{EmployeeName} - {EmployeePay} - {EmployeeDays}")
                
        def edit_employee():
            # Retrieve data from entry fields
            current_employee = name_entry.get()
            update_salary = salary_entry.get()
            update_days = Days_entry.get()
            
            # Check if any field is not empty
            if current_employee or update_days or update_salary:
                conn = sqlite3.connect('Comp Science.db')
                cursor = conn.cursor()
                
                # Update employee's salary and working days in the database
                cursor.execute('UPDATE Employee SET (EmployeePay, EmployeeDays) =(?, ?) WHERE EmployeeName =?', (update_salary,int(update_days), current_employee))
                conn.commit()
                conn.close()
                
                # Update employee list in the GUI
                employees_list.delete(0, END)
                getData()
                name_entry.delete(0, 'end')
                salary_entry.delete(0, 'end')
                Days_entry.delete(0,'end')                
            else:
                # Display error message if all fields are empty
                error_label = Label(employees_window, text="At least one of the fields is empty", fg="red")
                employees_window.after(2000, lambda: error_label.destroy())
                error_label.pack()

        def deleteStock():
            # Retrieve the name of the employee to delete
            delete_name = name_entry.get()
            
            # Check if the name field is not empty
            if delete_name:
                conn = sqlite3.connect('Comp Science.db')
                cursor = conn.cursor()
                
                # Delete employee from the database
                cursor.execute('DELETE FROM Employee WHERE EmployeeName = ?', (delete_name,))
                conn.commit()
                conn.close()
                
                # Update employee list in the GUI
                employees_list.delete(0, END)
                getData()
                name_entry.delete(0, 'end')
                salary_entry.delete(0, 'end')
                Days_entry.delete(0, 'end')
            else:
                # Display error message if the name field is empty
                error_label = Label(employees_window, text="At least one of the fields is empty", fg="red")
                employees_window.after(2000, lambda: error_label.destroy())
                error_label.pack()

        def back():
            # Destroy the current window and show the dashboard window
            employees_window.destroy()
            dashboard.deiconify()

        # Buttons and labels
        select_button = Button(employees_window, text="Select Employee", width=12, height=2, command=select_item)
        select_button.place(x=300, y=260)

        add_employee_btn = Button(employees_window, text="Add Employee", width=12, height=2, command=insert_employee)
        add_employee_btn.place(x=200, y=260)

        Edit_btn = Button(employees_window, text="Edit Employee", width=12, height=2, command=edit_employee)
        Edit_btn.place(x=300, y=320)

        Delete_btn = Button(employees_window, text="Delete Employee", width=12, height=2, command=deleteStock)
        Delete_btn.place(x=200, y=320)

        back_button = Button(employees_window, text="Back", command=back)
        back_button.place(x=280, y=370)

        getData()

    def dashboard_inventory():
        # Hide the dashboard window and create the inventory window
        dashboard.withdraw()
        Inventory_window = Tk()
        Inventory_window.resizable(False, False)
        Inventory_window.title("Inventory")
        Inventory_window.geometry("500x400")
        Inventory_window.configure(bg='grey')

        def select_item():
            # Retrieve and display selected item in entry fields
            selected_item = str(stock_list.get(stock_list.curselection()))
            item, quantity = selected_item.split(" - ")
            item_entry.delete(0, 'end')
            quantity_entry.delete(0, 'end')
            item_entry.insert(0, item)
            quantity_entry.insert(0, quantity)
            
        def getData():
            # Retrieve data from the database and populate the listbox
            conn = sqlite3.connect('Comp Science.db')
            cursor = conn.cursor()
            cursor.execute('''SELECT ProductName, StockQuantity FROM Product''')
            listData = cursor.fetchall()
            for row in listData:
                (ProductName, StockQuantity) = tuple(row)
                stock_list.insert(END, f"{ProductName} - {StockQuantity}")

        # Create listbox to display inventory items
        stock_list = Listbox(Inventory_window)
        stock_list.pack()

        def addStock():
            # Add new stock to the database and listbox
            new_stock = item_entry.get()
            new_quantity = quantity_entry.get()
            if item_entry.index("end") == 0 and quantity_entry.index("end") == 0:
                error_label = Label(Inventory_window, text="At least one of the fields is empty", fg="red")
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
            # Edit stock quantity in the database
            current_stock = item_entry.get()
            update_quantity = quantity_entry.get()
            if item_entry.index("end") == 0 and quantity_entry.index("end") == 0:
                error_label = Label(Inventory_window, text="At least one of the fields is empty", fg="red")
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
            # Delete stock from the database and listbox
            delete_name = item_entry.get()
            if item_entry.index("end") == 0 and quantity_entry.index("end") == 0:
                error_label = Label(Inventory_window, text="At least one of the fields is empty", fg="red")
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
            # Destroy the current window and show the dashboard window
            Inventory_window.destroy()
            dashboard.deiconify()

        # Labels and entry fields
        item_label = Label(Inventory_window, text="Item:", bg="grey")
        item_label.pack()

        item_entry = Entry(Inventory_window)
        item_entry.pack()

        quantity_label = Label(Inventory_window, text="Quantity:", bg="grey")
        quantity_label.pack()

        quantity_entry = Entry(Inventory_window)
        quantity_entry.pack()

        # Buttons for actions
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


