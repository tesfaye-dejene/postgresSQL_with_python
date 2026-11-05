
import psycopg2


def create_table():
    conn = psycopg2.connect(dbname ="studentdb", user="postgres", password="admin123",host="localhost", port="5432")
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS students(student_id serial primary key, name varchar(50), age int,adress varchar(100) ,phonenumber text);")
    print("Table created successfully")
    conn.commit()
    conn.close()

def insert_data():
    #accepting data from user
    name = input("Enter student name: ")
    age = input("Enter student age: ")
    address = input("Enter student address: ")
    phonenumber = input("Enter student phonenumber: ")
    conn = psycopg2.connect(dbname ="studentdb", user="postgres", password="admin123",host="localhost", port="5432")
    cur = conn.cursor()
    cur.execute("INSERT INTO students(name, age, adress, phonenumber) VALUES(%s, %s, %s, %s)", (name, age, address, phonenumber))
    print("Data inserted successfully")
    conn.commit()
    conn.close()

def delete_data():
    student_id = input("Enter student id to delete: ")
    conn = psycopg2.connect(dbname ="studentdb", user="postgres", password="admin123",host="localhost", port="5432")
    cur = conn.cursor()
    cur.execute("select * from students where student_id=%s", (student_id,))

    student = cur.fetchone()
    if student:
        print(f"Student to be deleted: ID {student[0]}, Name: {student[1]}, Age: {student[2]}, Address: {student[3]}, Phone Number: {student[4]}")
        confirm = input("Are you sure you want to delete this student? (y/n): ")
        if confirm.lower() == "y":
            cur.execute("DELETE FROM students WHERE student_id=%s", (student_id,))
            print("Data deleted successfully")
        else:
            print("Deletion canceled")
    else:
        print("Student not found")

    conn.commit()
    conn.close()

def update_data():
    student_id = input("Enter student id to update: ")
    conn = psycopg2.connect(dbname ="studentdb", user="postgres", password="admin123",host="localhost", port="5432")
    cur = conn.cursor()
    fields = {"1":("name", "Enter the new name: "),
              "2":("age", "Enter the new age: "),
              "3":("adress", "Enter the new address: "),
              "4":("phonenumber", "Enter the new phonenumber: ")
             }
    print("Select the field to update:")
    for key in fields:
        print(f"{key}. {fields[key][1]}")
    field_choice = input("Enter your choice: ")

    if field_choice in fields:
        field_name, promt = fields[field_choice]
        new_value = input(promt)
        sql = f"UPDATE students SET {field_name}=%s WHERE student_id=%s"
        cur.execute(sql, (new_value, student_id))
        print(f"{field_name} updated successfully")
    else:
        print("Invalid choice")

    conn.commit()
    conn.close()

def read_data():
    conn = psycopg2.connect(dbname ="studentdb", user="postgres", password="admin123",host="localhost", port="5432")
    cur = conn.cursor()
    cur.execute("SELECT * FROM students;")
    students = cur.fetchall()
    for student in students:
        print(f"ID: {student[0]}, Name: {student[1]}, Age: {student[2]}, Address: {student[3]}, Phone Number: {student[4]}")
    conn.close()

#create_table()
#insert_data()
#update_data()
#delete_data()

while True:
    print("\n welcom to student database management system")
    print("1. Create Table")
    print("2. Insert Data")
    print("3. Update Data")
    print("4. Delete Data")
    print("5. read Data")
    print("6. Exit")
    choice = input("Enter your choice: ")

    if choice == "1":
        create_table()
    elif choice == "2":
        insert_data()
    elif choice == "3":
        update_data()
    elif choice == "4":
        delete_data()
    elif choice == "5":
        read_data()
    elif choice == "6":
        print("Exiting...")
        break
    else:
        print("Invalid choice. Please try again.")


        