from tkinter import *
import sqlite3

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
    pass

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

getData()
mainloop()