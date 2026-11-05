from tkinter import *
from tkinter import ttk
from tkinter import messagebox

import psycopg2

def  run_query(query,parameters=()):
     conn = psycopg2.connect(dbname ="studentdb", user="postgres", password="admin123",host="localhost", port="5432")
     cur = conn.cursor()
     query_result = None
     try:
        cur.execute(query,parameters)
        if query.lower().startswith("select"):
            query_result = cur.fetchall()
        conn.commit()
     except psycopg2.Error as e:
        print(f"Error executing query:",str(e))
     finally:
        cur.close()
        conn.close()
     return query_result


def refresh_treeview():
    for item in tree.get_children():
        tree.delete(item)
    records = run_query("SELECT * FROM students;")
    for record in records:
         tree.insert('', END, values=record)
         

def insert_data():
    query = "INSERT INTO students(name, age, adress, phonenumber) VALUES(%s, %s, %s, %s)"
    parameters = (name_entry.get(), age_entry.get(), address_entry.get(), phone_entry.get())
    run_query(query, parameters)
    messagebox.showinfo("Success", "Data inserted successfully")
    refresh_treeview() 

def delete_data():
    selected_item = tree.selection()[0]
    print(selected_item)
    student_id = tree.item(selected_item)['values'][0]
    query = "DELETE FROM students WHERE student_id=%s"
    parameters = (student_id,)
    run_query(query, parameters)
    messagebox.showinfo("Success", "Data deleted successfully")
    refresh_treeview()

def update_data():
    selected_item = tree.selection()[0]
    student_id = tree.item(selected_item)['values'][0]
    query = "UPDATE students SET name=%s, age=%s, adress=%s, phonenumber=%s WHERE student_id=%s"
    parameters = (name_entry.get(), age_entry.get(), address_entry.get(), phone_entry.get(), student_id)
    run_query(query, parameters)
    messagebox.showinfo("Success", "Data updated successfully")
    refresh_treeview()

def create_table():
    query = """  
    CREATE TABLE IF NOT EXISTS students (
        student_id SERIAL PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        age INTEGER NOT NULL,
        adress VARCHAR(255) NOT NULL,
        phonenumber VARCHAR(15) NOT NULL
    );
    """

    run_query(query)
    messagebox.showinfo("Success", "Table created successfully")



root = Tk()
root.title("student management system")

frame = LabelFrame(root, text="Student Management System", padx=20, pady=20)
frame.grid(row=0, column=0, padx=10, pady=10,sticky="ew")

Label(frame, text="Name:").grid(row=0, column=0,padx=10, pady=10, sticky="w")
name_entry = Entry(frame)
name_entry.grid(row=0, column=1,padx=10, pady=10, sticky="ew")

Label(frame, text="Address:").grid(row=1, column=0,padx=10, pady=10, sticky="w")
address_entry = Entry(frame)
address_entry.grid(row=1, column=1,padx=10, pady=10, sticky="ew")

Label(frame, text="Age:").grid(row=2, column=0,padx=10, pady=10, sticky="w")
age_entry = Entry(frame)
age_entry.grid(row=2, column=1,padx=10, pady=10, sticky="ew")

Label(frame, text="Phone Number:").grid(row=3, column=0,padx=10, pady=10, sticky="w")
phone_entry = Entry(frame)
phone_entry.grid(row=3, column=1,padx=10, pady=10, sticky="ew")


button_frame = Frame(root)
button_frame.grid(row=1, column=0, pady=5 ,sticky="ew")
Button(button_frame, text="Create Table", command=create_table).grid(row=0, column=0, padx=10, pady=10)

Button(button_frame, text="Add data", command=insert_data).grid(row=0, column=1, padx=10, pady=10)
Button(button_frame, text="Update Data", command=update_data).grid(row=0, column=2, padx=10, pady=10)
Button(button_frame, text="Delete Data", command=delete_data).grid(row=0, column=3, padx=10, pady=10)


tree_frame = Frame(root)
tree_frame.grid(row=2, column=0, padx=10, pady=10,sticky="nsew")

tree_scroll = Scrollbar(tree_frame)
tree_scroll.pack(side=RIGHT, fill=Y)

tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set, selectmode="browse")
tree.pack()



tree_scroll.config(command=tree.yview)

tree['columns']=("student_id","name","address","age","phone Number")

tree.column("#0", width=0, stretch=NO)
tree.column("student_id", anchor=CENTER, width=100)
tree.column("name", anchor=CENTER, width=100)
tree.column("address", anchor=CENTER, width=100)
tree.column("age", anchor=CENTER, width=100)
tree.column("phone Number", anchor=CENTER, width=100)

tree.heading("#0", text="", anchor=CENTER)
tree.heading("student_id", text="student_id", anchor=CENTER)
tree.heading("name", text="name", anchor=CENTER)
tree.heading("address", text="address", anchor=CENTER)
tree.heading("age", text="age", anchor=CENTER)
tree.heading("phone Number", text="phone Number", anchor=CENTER)






refresh_treeview()
root.mainloop()