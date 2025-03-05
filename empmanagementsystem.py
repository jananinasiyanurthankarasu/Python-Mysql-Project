import mysql.connector

def connect_to_db():
    return mysql.connector.connect(
        host = "localhost",
        username = "root",
        password = "Janani_95",
        database = "employee_db"
    )

def add_employee(name,age,department,salary):
    conn = connect_to_db()
    cursor = conn.cursor()
    sql = "INSERT INTO employees(name,age,department,salary) VALUES (%s,%s,%s,%s)"
    values = (name,age,department,salary)
    cursor.execute(sql,values)
    conn.commit()
    print("Employee added succesfully")
    cursor.close()
    conn.close()

def view_employees():
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM employees")
    rows = cursor.fetchall()
    print("Employee List")
    for row in rows:
        print(row)
    cursor.close()
    conn.close()

def update_employee(id,name,age,department,salary):
    conn = connect_to_db()
    cursor = conn.cursor()
    sql = "UPDATE employees SET name=%s, age=%s, department=%s, salary=%s WHERE id=%s"
    values = (name, age, department, salary, id)
    cursor.execute(sql,values)
    conn.commit()
    print("Employees updated successfully")
    cursor.close()
    conn.close()

def delete_employee(id):
    conn = connect_to_db()
    cursor = conn.cursor()
    sql = "DELETE FROM employees WHERE id = %s"
    values = (id,)
    cursor.execute(sql,values)
    conn.commit()
    print("Employees deleted successfully")
    cursor.close()
    conn.close()

def main_menu():
    while True:
        print("======EMPLOYEE MANAGEMENT SYSTEM======")
        print("1.Add Employee")
        print("2.View Employee")
        print("3.Update Employee")
        print("4.Delete Employee")
        print("5.Exit")
        choice = (input("Enter your choice"))
        if choice == '1':
            name = input("Enter your name: ")
            age = int(input("Enter your age: "))
            department = input("Enter your department: ")
            salary = float(input("Enter your salary: "))
            add_employee(name,age,department,salary)
        
        elif choice == '2':
            view_employees()
        
        elif choice == '3':
            id = input("Enter employee id to update: ")
            name = input("Enter new name: ")
            age = int(input("Enter new age: "))
            department = input("Enter the new department: ")
            salary = float(input("Enter the salary: "))
            update_employee(id,name,age,department,salary)
        
        elif choice == '4':
            id =int(input("Enter the employee ID to delete"))
            delete_employee(id)
        
        elif choice == '5':
            print("Exiting the system")
            break

        else:
            print("Invalid choice")
        
if __name__ == "__main__":
    main_menu()