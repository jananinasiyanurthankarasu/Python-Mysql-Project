import mysql.connector

def connect_to_db():
    return mysql.connector.connect(
        host = "localhost",
        username = "root",
        password = "Janani_95",
        database = "airline_system"
    )

def register_user(name,email,password):
    conn = connect_to_db()
    cursor = conn.cursor()
    sql = "INSERT INTO users(name,email,password) VALUES (%s,%s,%s)"
    values = (name,email,password)
    try:
        cursor.execute(sql,values)
        conn.commit()
        print("Users added successfully")
    except mysql.connector.Error as err:
        print(f"Error:{err}")
    finally:
        conn.close()


def login_user():
    conn = connect_to_db()
    cursor = conn.cursor(dictionary=True)
    email = input("Enter your email: ")
    password = input("Enter your password: ")
    sql = "SELECT * FROM users WHERE email=%s and password=%s"
    values = (email,password)
    conn.execute(sql,values)
    user = cursor.fetchone()
    if user:
        print(f"Welcome, {user['name']}!")
        return user
    else:
        print("Invalid Credentials")
        return None

def search_flights():
    conn = connect_to_db()
    cursor = conn.cursor(dictionary=True)
    origin = input("Enter Origin: ")
    destination = input("Enter Destination: ")
    date = input("Enter depature date (yyyy-mm-dd): ")
    sql = "SELECT * FROM flights WHERE origin = %s and destination = %s and date(depature_time = %s)"
    values = (origin,destination,date)
    cursor.execute(sql,values)
    flights = cursor.fetchall()
    if flights:
        print("Available Flights")
        for flight in flights:
            print(flight)
    else:
        print("No flights found")
    conn.close()

def book_tickets(user_id):
    conn = connect_to_db()
    cursor = conn.cursor()
    flight_id = int(input("Enter flight id to book: "))
    num_passengers = int(input("Enter the number of passengers: "))
    sql = "select seats_available FROM flights WHERE flight_id = %s"
    values =(flight_id,num_passengers)
    cursor.execute(sql,values)
    seats = cursor.fetchone()[0]
    if seats < num_passengers:
        print("There are not enough seats available")
        return
    
    try:
        reservation_query = "INSERT INTO reservations(user_id,flight_id) VALUES(%s,%s)"
        cursor.execute(reservation_query,(user_id,flight_id))
        reservation_id = cursor.lastrowid

        for _ in range(num_passengers):
            name = input("Enter passenger name: ")
            age = int(input("enter the age: "))
            passport_number = input("Enter the passport number: ")
            passenger_query = "INSERT INTO passengers(reservation_id,name,age,passport_number) VALUES (%s,%s,%s,%s)"
            cursor.execute(passenger_query,(reservation_id,name,age,passport_number))
        
        update_query = "UPDATE flights SET seats_available = seats_available -%s WHERE flight_id = %s"
        cursor.execute(update_query,(num_passengers,flight_id))
        conn.commit()
        print("Booking Successfull!")
    
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        conn.rollback()
    finally:
        conn.close()


def cancel_reservation():
    conn = connect_to_db()
    cursor = conn.cursor()
    reservation_id = int(input("Enter the reservation id to cancel"))
    try:
        cancel_query = "UPDATE reservations SET status = 'cancelled' WHERE reservation_id = %s"
        cursor.execute(cancel_query,(reservation_id))
        seats_query = "UPDATE flights JOIN reservations ON flights.flight_id = reservations.flight_id SET flights.seats_availabe = flights.seats_available + (SELECT COUNT(*) from passengers WHERE reservation_id = %s) WHERE reservations.reservation_id = %s"
        cursor.execute(seats_query,(reservation_id, reservation_id))
        conn.commit()
        print("Reservation cancelled successfully")
    except mysql.connector.Error as Err:
        print(f"Error: {Err}")
        conn.rollback()
    finally:
        conn.close()

def main_menu():
    while True:
        print("\n Airline Reservation System")
        print("1. Resgister")
        print("2. Login")
        print("3. Search Flights")
        print("4. Book Tickets")
        print("5. Cancell Reservation")
        print("6. Exit")

        choice = int(input("Enter the choice: "))

        if choice == 1:
            register_user()
        elif choice == 2:
            user = login_user()
        elif choice == 3:
            search_flights()
        elif choice == 4:
            if user:
                book_tickets(user['user_id'])
            else:
                print("Please Login first")
        elif choice == 5:
            cancel_reservation()
        elif choice == 6:
            print("Exiting the system")
            break
        else:
            print("Invalid Choice")

main_menu()