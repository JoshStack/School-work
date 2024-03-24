from tkinter import *
import sqlite3

conn = sqlite3.connect('Comp Science.db')
cursor = conn.cursor()
count = cursor.execute('SELECT COUNT(*) FROM Customer')

conn.commit()
if count is :
    print("yay")
else:
    print("cry")
conn.close()

