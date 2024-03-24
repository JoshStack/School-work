from tkinter import *
import sqlite3

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
# Create a Listbox to display the employees
employees_list = Listbox(employees_window, width=0)
employees = [""]
for employee in employees:
    employees_list.insert(END, employee)
employees_list.pack()

# Function to insert the user input as a new employee
def insert_employee():
    name = name_entry.get()
    salary = salary_entry.get()
    Days = Days_entry.get()
    if name and salary:  # Check if both name and salary fields are not empty
        new_employee = name + " - £" + salary + " - days/week: " + Days
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
        error_label.pack()
# Create the "Add Employee" button to add the input to the Listbox
add_employee_button = Button(employees_window, text="Add Employee", command=insert_employee)
add_employee_button.pack()

# Add a back button to close the window
back_button = Button(employees_window, text="Back", command=employees_window.destroy)
back_button.place(x=250, y=350)


employees_window.mainloop()
