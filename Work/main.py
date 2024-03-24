from tkinter import *
import sqlite3

#this function contains everything to do with the set up window
def SetUp_Clicked():
    root.withdraw()
    conn = sqlite3.connect('Comp Science.db')
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT Email FROM Customer')
    conn.commit()
    conn.close()

    def submit(email_ent, email_window):
        Email = email_ent
        print(Email)
        conn = sqlite3.connect('Comp Science.db')
        cursor = conn.cursor()

# Create a table if it doesn't exist
        cursor.execute('''CREATE TABLE IF NOT EXISTS Customer
                (Customerid INTEGER PRIMARY KEY, email TEXT)''')

# Insert data into the table
        cursor.execute('INSERT INTO customer (email) VALUES (?)', (Email,))

# Commit changes and close the connection
        conn.commit()
        conn.close()
        email_window.destroy()
    def getEmail():
        email_window = Tk()
        email_window.title("email")
        email_window.geometry("500x400")
        email_window.configure(bg='grey')
        
        email_Lbl = Label(email_window, text="Enter you email: ",bg="grey")
        email_Lbl.place(x=56,y=100)
        
        email_ent = Entry(email_window)
        email_ent.place(x=56,y=125)
        
        submit_btn = Button(email_window, text="submit",command=lambda: submit(email_ent.get(), email_window))
        submit_btn.place(x=56,y=165)
        
    getEmail()

    def InventoryClicked():
        SetUp_Window.withdraw()
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
                print("at least one of the fields are empty")
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
            print(current_stock)
            print(update_quantity)
            if item_entry.index("end") == 0 and quantity_entry.index("end") == 0:
                print("at least one of the fields are empty")
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
                print("at least one of the fields are empty")
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
        back_btn.place(x=420, y=350)

        getData()

    def EmployeeClicked():
        pass
#this function destroys the Set Up window and unhides the root window
    def BackClicked():
        SetUp_Window.destroy()
        root.deiconify()

#this creates the tkinter window called Set Up with a geometry of 500x400
    SetUp_Window = Tk()
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
    
    sales = Button(dashboard, text="  Sales  ", bg='#8bc1f7', height=2, width=15)
    sales.place(x=90, y=100)
    
    orders = Button(dashboard, text=" Orders ", bg='#8bc1f7', height=2, width=15)
    orders.place(x=300, y=100)
    
    Employees = Button(dashboard, text="Employees", bg='#8bc1f7', height=2, width=15)
    Employees.place(x=90, y=200)
    
    Inventory = Button(dashboard, text="Inventory", bg='#8bc1f7', height=2, width=15,)
    Inventory.place(x=300, y=200)
    
    back_btn = Button(dashboard, text="back",height=2, width=15, command=backPressed)
    back_btn.place(x=120, y=350)
    
    Exit_btn = Button(dashboard, text="Exit", height=2, width=15, command=quit)
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


