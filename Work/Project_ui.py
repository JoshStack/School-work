'''import tkinter as tk
from tkinter import ttk

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import sqlite3

x = []
y = []
#creates the sales window
def salesClicked():
  sales_window = tk.Tk()
  sales_window.title('Sales')
  sales_window.geometry("600x500")
  sales_window.configure(bg='grey')
  backButton = tk.Button(sales_window, text="Back", command=sales_window.destroy)
  backButton.pack()


  startYear = int(input("Enter the start year: "))

  numYears = int(input("Enter the number of years: "))

  for _i in range(numYears):
    year = startYear
    sales_amount = int(input(f"Enter the sales amount for year {year}: "))
    x.append(year)
    y.append(sales_amount)

    startYear += 1

  # Create a sample graph

  fig, ax = plt.subplots()
  ax.plot(x, y)

  canvas = FigureCanvasTkAgg(fig, master=sales_window)
  canvas.draw()
  canvas.get_tk_widget().place(x = 20, y = 50, width=450, height=300)  
  # Set the size for the graph canvas

  sales_window.mainloop()




def ordersClicked():
    # Create the orders window
    orders_window = tk.Tk()
    orders_window.title('Orders')
    orders_window.geometry("800x600")

    # Create input fields for the user to enter the order details
    date_label = tk.Label(orders_window, text="Date:")
    date_label.pack()
    date_entry = tk.Entry(orders_window)
    date_entry.pack()

    customer_label = tk.Label(orders_window, text="Customer:")
    customer_label.pack()
    customer_entry = tk.Entry(orders_window)
    customer_entry.pack()

    total_amount_label = tk.Label(orders_window, text="Total Amount:")
    total_amount_label.pack()
    total_amount_entry = tk.Entry(orders_window)
    total_amount_entry.pack()

    # Create a Treeview widget to display the previous orders
    order_tree = ttk.Treeview(orders_window, columns=('Date', 'Customer', 'Total Amount'))
    order_tree.heading('#0', text='Order ID')
    order_tree.column('#0', width=100)
    order_tree.heading('Date', text='Date')
    order_tree.column('Date', width=100)
    order_tree.heading('Customer', text='Customer')
    order_tree.column('Customer', width=100)
    order_tree.heading('Total Amount', text='Total Amount')
    order_tree.column('Total Amount', width=150) 

    # Function to insert the user input into the Treeview
    def insert_order():
        # Get the order details from the input fields
        date = date_entry.get()
        customer = customer_entry.get()
        total_amount = total_amount_entry.get()

        if date and customer and total_amount:  # Check if all fields are not empty
            # Get the last order ID from the database and increment it to generate a new order ID
            conn = sqlite3.connect('orders.db')
            c = conn.cursor()
            c.execute('CREATE TABLE IF NOT EXISTS orders (order_id INTEGER PRIMARY KEY AUTOINCREMENT, date TEXT, customer TEXT, total_amount REAL)')

            # Insert the order details into the database
            c.execute('INSERT INTO orders (date, customer, total_amount) VALUES (?,?,?)', (date, customer, total_amount))
            conn.commit()

            # Get the auto-generated order ID
            order_id = c.lastrowid
            # Insert the order details into the Treeview
            order_tree.insert('', 'end', text=order_id, values=(date, customer, total_amount))

            # Clear the input fields after adding an order
            date_entry.delete(0, 'end')
            customer_entry.delete(0, 'end')
            total_amount_entry.delete(0, 'end')

            # Close the database connection
            conn.close()

        else:
            # Display an error message if any field is empty
            error_label = tk.Label(orders_window, text="All fields are required", fg="red")
            error_label.pack()

    # Create the "Add Order" button to add the input to the Treeview and database
    add_order_button = tk.Button(orders_window, text="Add Order", command=insert_order)
    add_order_button.pack()

    # Pack the Treeview widget
    order_tree.pack(fill='both', expand=True)

    # Add a back button to close the window
    back_button = tk.Button(orders_window, text="Back", command=orders_window.destroy)
    back_button.place(x=350, y=450)

    orders_window.mainloop()

def employeesClicked():
    # Create the employees window
    employees_window = tk.Tk()
    employees_window.title('Employees')
    employees_window.geometry("600x400")

    # Create input fields for the user to enter employee details
    name_label = tk.Label(employees_window, text="Name:")
    name_label.pack()
    name_entry = tk.Entry(employees_window)
    name_entry.pack()

    salary_label = tk.Label(employees_window, text="Salary:")
    salary_label.pack()
    salary_entry = tk.Entry(employees_window)
    salary_entry.pack()

    # Create a Listbox to display the employees
    employees_list = tk.Listbox(employees_window)
    employees = [""]
    for employee in employees:
        employees_list.insert(tk.END, employee)
    employees_list.pack()

  # Function to insert the user input as a new employee
    def insert_employee():
      name = name_entry.get()
      salary = salary_entry.get()
      if name and salary:  # Check if both name and salary fields are not empty
          new_employee = name + " - £" + salary
          employees_list.insert(tk.END, new_employee)

          # Clear the input fields after adding an employee
          name_entry.delete(0, 'end')
          salary_entry.delete(0, 'end')
      else:
          # Display an error message if either name or salary field is empty
          error_label = tk.Label(employees_window, text="Both name and salary fields are required", fg="red")
          error_label.pack()
    # Create the "Add Employee" button to add the input to the Listbox
    add_employee_button = tk.Button(employees_window, text="Add Employee", command=insert_employee)
    add_employee_button.pack()

    # Add a back button to close the window
    back_button = tk.Button(employees_window, text="Back", command=employees_window.destroy)
    back_button.place(x=250, y=350)

    employees_window.mainloop()

def inventoryClicked():
  # Create the inventory window
  inventory_window = tk.Tk()
  inventory_window.title('Inventory')
  inventory_window.geometry("600x400")
  # Create a Listbox to display the current stock
  stock_list = tk.Listbox(inventory_window)
  current_stock = ["Item A - 10", "Item B - 20", "Item C - 15"]  # Example current stock
  for stock in current_stock:
      stock_list.insert(tk.END, stock)
  stock_list.pack()
  # Function to handle selecting an item from the stock list
  def select_item():
      selected_item = stock_list.get(stock_list.curselection())
      item, quantity = selected_item.split(" - ")
      item_entry.delete(0, 'end')
      quantity_entry.delete(0, 'end')
      item_entry.insert(0, item)
      quantity_entry.insert(0, quantity)

    # Create the "Select Item" button to select an item for editing
  select_button = tk.Button(inventory_window, text="Select Item", command=select_item)
  select_button.pack()

  # Create input fields for the user to edit the stock
  item_label = tk.Label(inventory_window, text="Item:")
  item_label.pack()
  item_entry = tk.Entry(inventory_window)
  item_entry.pack()
  quantity_label = tk.Label(inventory_window, text="Quantity:")
  quantity_label.pack()
  quantity_entry = tk.Entry(inventory_window)
  quantity_entry.pack()

  # Function to edit the stock
  def edit_stock():
      selected_index = stock_list.curselection()
      if selected_index:
          selected_item = stock_list.get(selected_index)
          item, _ = selected_item.split(" - ")
          new_quantity = quantity_entry.get()
          if new_quantity:  # Check if the new quantity field is not empty
              updated_stock = item + " - " + new_quantity
              stock_list.delete(selected_index)
              stock_list.insert(selected_index, updated_stock)
              item_entry.delete(0, 'end')
              quantity_entry.delete(0, 'end')
          else:
              # Display an error message if the new quantity field is empty
              error_label = tk.Label(inventory_window, text="New quantity field is required", fg="red")
              error_label.pack()
      else:
          # Display an error message if no item is selected
          error_label = tk.Label(inventory_window, text="Please select an item from the list", fg="red")
          error_label.pack()

  # Create the "Edit Stock" button to edit the selected stock in the Listbox
  edit_stock_button = tk.Button(inventory_window, text="Edit Stock", command=edit_stock)
  edit_stock_button.pack()
  
  # Function to add new stock
  def add_stock():
      new_item = item_entry.get()
      new_quantity = quantity_entry.get()
      if new_item and new_quantity:  # Check if both new item and quantity fields are not empty
          new_stock = new_item + " - " + new_quantity
          stock_list.insert(tk.END, new_stock)

          # Clear the input fields after adding new stock
          item_entry.delete(0, 'end')
          quantity_entry.delete(0, 'end')
      else:
          # Display an error message if either new item or quantity field is empty
          error_label = tk.Label(inventory_window, text="Both new item and quantity fields are required", fg="red")
          error_label.pack()

  # Create the "Add Stock" button to add new stock to the Listbox
  add_stock_button = tk.Button(inventory_window, text="Add Stock", command=add_stock)
  add_stock_button.pack()

    # Add a back button to close the window
  back_button = tk.Button(inventory_window, text="Back", command=inventory_window.destroy)
  back_button.place(x=250, y=350)

  inventory_window.mainloop()

#creates a the mainscreen
root = tk.Tk()
root.title('Dashboard')
root.geometry("500x400")
root.configure(bg='grey')


#creates a button

sales = tk.Button(root, text="  Sales  ", bg='#8bc1f7', command=salesClicked)
sales.place(x=90, y=100)
orders = tk.Button(root, text=" Orders ", bg='#8bc1f7', command=ordersClicked)
orders.place(x=300, y=100)
Employees = tk.Button(root, text="Employees", bg='#8bc1f7', command=employeesClicked)
Employees.place(x=90, y=300)
Inventory = tk.Button(root, text="Inventory", bg='#8bc1f7', command=inventoryClicked)
Inventory.place(x=300, y=300)

root.mainloop()'''