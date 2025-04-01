# -*- coding: utf-8 -*-
"""
Created on Tue Dec  5 21:50:04 2023

@author: Admin
"""
#%%
import mysql.connector

# Function to create a MySQL connection
conn = mysql.connector.connect(host='localhost', user='root', password='1234')

if conn.is_connected():
    print("Connected to MySQL Server version")

# Connect to the database
cursor = conn.cursor()

O='drop database IF EXISTS flight_management'
cursor.execute(O)
conn.commit()

Q='create database IF NOT EXISTS flight_management'
cursor.execute(Q)
conn.commit()

M = 'use flight_management'
cursor.execute(M)
conn.commit()

# Database setup
cursor.execute("""
    CREATE TABLE IF NOT EXISTS flights (
        flight_id INT AUTO_INCREMENT PRIMARY KEY,
        flight_number VARCHAR(255),
        source VARCHAR(255),
        destination VARCHAR(255),
        departure_date DATE,
        departure_time TIME,
        seats_available INT
    )
""")
conn.commit()

cursor.execute("""insert into flights values(1,'AL089', 'Mumbai','Delhi','2024-01-24','12:00', 49)""")
conn.commit()
cursor.execute("""insert into flights values(2,'FL095', 'Kharagpur','Dehradun','2024-01-21','20:00', 12)""")
conn.commit()
cursor.execute("""insert into flights values(3,'GM921', 'Banglore','Roorkee','2024-01-27','19:00', 23)""")
conn.commit()
cursor.execute("""insert into flights values(4,'QX323', 'Hyderabad','Pune','2024-01-29','17:00', 37)""")
conn.commit()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS passengers (
        passenger_id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255),
        age INT,
        email VARCHAR(255),
        phone varchar (11)
    )
""")
conn.commit()

cursor.execute("""insert into passengers values(1,'Aryan Agarwal',17,'aryanag219@gmail.com',8930475610)""")
conn.commit()
cursor.execute("""insert into passengers values(2,'Aditya Patil',16,'adityap23@gmail.com',9981038572)""")
conn.commit()
cursor.execute("""insert into passengers values(3,'Krish Varma',18,'vkrish01@gmail.com',8301849270)""")
conn.commit()
cursor.execute("""insert into passengers values(4,'Sakshi Sinha',17,'sakshis910@gmail.com',9381029381)""")
conn.commit()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS bookings (
        booking_id INT AUTO_INCREMENT PRIMARY KEY,
        flight_id INT,
        passenger_id INT,
        FOREIGN KEY (flight_id) REFERENCES flights(flight_id),
        FOREIGN KEY (passenger_id) REFERENCES passengers(passenger_id)
    )
""")
conn.commit()

# Function to add a new flight
def add_flight(flight_number, source, destination, departure_date, departure_time, seats_available):
    cursor.execute("""
        INSERT INTO flights (flight_number, source, destination, departure_date, departure_time, seats_available)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (flight_number, source, destination, departure_date, departure_time, seats_available))
    conn.commit()
    print("Flight added successfully!")

# Function to view all flights
def view_flights():
    cursor.execute("SELECT * FROM flights")
    flights = cursor.fetchall()
    print("\nList of Flights:")
    for flight in flights:
        print(flight)

# Function to add a new passenger
def add_passenger(name, age, email, phone):
    cursor.execute("""
        INSERT INTO passengers (name, age, email, phone)
        VALUES (%s, %s, %s, %s)
    """, (name, age, email, phone))
    conn.commit()
    print("Passenger added successfully!")

# Function to view all passengers
def view_passengers():
    cursor.execute("SELECT * FROM passengers")
    passengers = cursor.fetchall()
    print("\nList of Passengers:")
    for passenger in passengers:
        print(passenger)

# Function to book a flight for a passenger
def book_flight(passenger_id, flight_id):
    cursor.execute("""
        INSERT INTO bookings (passenger_id, flight_id)
        VALUES (%s, %s)
    """, (passenger_id, flight_id))
    # Decrease the available seats for the booked flight
    cursor.execute("UPDATE flights SET seats_available = seats_available - 1 WHERE flight_id = %s", (flight_id,))
    conn.commit()
    print("Booking successful!")

# Function to view all bookings
def view_bookings():
    cursor.execute("""
        SELECT passengers.name, flights.flight_number, flights.source, flights.destination, flights.departure_date, flights.departure_time
        FROM bookings
        INNER JOIN passengers ON bookings.passenger_id = passengers.passenger_id
        INNER JOIN flights ON bookings.flight_id = flights.flight_id
    """)
    bookings = cursor.fetchall()
    print("\nList of Bookings:")
    for booking in bookings:
        print(booking)


def update_flight(flight_id):
    cursor.execute("SELECT * from flights WHERE flight_id = %s", (flight_id,))
    flight = cursor.fetchone()
    if flight:
        print(f"\nFlight Details:\n{flight}")
        print("Enter new details:")
        flight_number = input("Flight Number: ")
        source = input("Source: ")
        destination = input("Destination: ")
        departure_date = input("Departure Date (YYYY-MM-DD): ")
        departure_time = input("Departure Time: ")
        seats_available = int(input("Seats Available: "))

        cursor.execute("""
            UPDATE flights
            SET flight_number = %s, source = %s, destination = %s,
                departure_date = %s, departure_time = %s, seats_available = %s
            WHERE flight_id = %s
        """, (flight_number, source, destination, departure_date, departure_time, seats_available, flight_id))
        conn.commit()
        print("Flight updated successfully!")
    else:
        print("Flight not found.")

# Function to delete a flight
def delete_flight(flight_id):
    cursor.execute("DELETE FROM flights WHERE flight_id = %s", (flight_id,))
    conn.commit()
    print("Flight deleted successfully!")

# Function to update passenger details
def update_passenger(passenger_id):
    cursor.execute("SELECT * FROM passengers WHERE passenger_id = %s", (passenger_id,))
    passenger = cursor.fetchone()
    if passenger:
        print(f"\nPassenger Details:\n{passenger}")
        print("Enter new details:")
        name = input("Name: ")
        age = int(input("Age: "))
        email = input("Email: ")
        phone = input("Phone: ")

        cursor.execute("""
            UPDATE passengers
            SET name = %s, age = %s, email = %s, phone = %s
            WHERE passenger_id = %s
        """, (name, age, email, phone, passenger_id))
        conn.commit()
        print("Passenger updated successfully!")
    else:
        print("Passenger not found.")

# Function to delete a passenger
def delete_passenger(passenger_id):
    cursor.execute("DELETE FROM passengers WHERE passenger_id = %s", (passenger_id,))
    conn.commit()
    print("Passenger deleted successfully!")

# Function to view available seats for a specific flight
def view_available_seats(flight_id):
    cursor.execute("SELECT seats_available FROM flights WHERE flight_id = %s", (flight_id,))
    seats = cursor.fetchone()
    if seats:
        print(f"\nAvailable Seats for Flight {flight_id}: {seats[0]}")
    else:
        print("Flight not found.")

# Function to view booked seats for a specific flight
def view_booked_seats(flight_id):
    cursor.execute("""
        SELECT COUNT(*) FROM bookings
        WHERE flight_id = %s
    """, (flight_id,))
    booked_seats = cursor.fetchone()[0]
    cursor.execute("SELECT seats_available FROM flights WHERE flight_id = %s", (flight_id,))
    total_seats = cursor.fetchone()[0]
    if booked_seats is not None and total_seats is not None:
        print(f"\nBooked Seats for Flight {flight_id}: {booked_seats}")
        print(f"Available Seats: {total_seats - booked_seats}")
    else:
        print("Flight not found.")

# Main User Interface (extended)
while True:
    print("\nFlight Management System:")
    print("1. Add Flight")
    print("2. View Flights")
    print("3. Update Flight")
    print("4. Delete Flight")
    print("5. Add Passenger")
    print("6. View Passengers")
    print("7. Update Passenger")
    print("8. Delete Passenger")
    print("9. Book Flight")
    print("10. View Bookings")
    print("11. View Available Seats")
    print("12. View Booked Seats")
    print("13. Exit")

    choice = input("Enter your choice: ")

    if choice == '1':
        flight_number = input("Enter Flight Number: ")
        source = input("Enter Source: ")
        destination = input("Enter Destination: ")
        departure_date = input("Enter Departure Date (YYYY-MM-DD): ")
        departure_time = input("Enter Departure Time: ")
        seats_available = int(input("Enter Seats Available: "))
        add_flight(flight_number, source, destination, departure_date, departure_time, seats_available)
    
    elif choice == '2':
        view_flights()

    elif choice == '3':
        flight_id = int(input("Enter Flight ID to update: "))
        update_flight(flight_id)

    elif choice == '4':
        flight_id = int(input("Enter Flight ID to delete: "))
        delete_flight(flight_id)

    elif choice == '5':
        name = input("Enter Passenger Name: ")
        age = int(input("Enter Passenger Age: "))
        email = input("Enter Passenger Email: ")
        phone = input("Enter Passenger Phone: ")
        add_passenger(name, age, email, phone)

    elif choice == '6':
        view_passengers()

    elif choice == '7':
        passenger_id = int(input("Enter Passenger ID to update: "))
        update_passenger(passenger_id)

    elif choice == '8':
        passenger_id = int(input("Enter Passenger ID to delete: "))
        delete_passenger(passenger_id)

    elif choice == '9':
        view_passengers()
        passenger_id = int(input("Enter Passenger ID: "))
        view_flights()
        flight_id = int(input("Enter Flight ID to book: "))
        book_flight(passenger_id, flight_id)

    elif choice == '10':
        view_bookings()

    elif choice == '11':
        flight_id = int(input("Enter Flight ID to view available seats: "))
        view_available_seats(flight_id)

    elif choice == '12':
        flight_id = int(input("Enter Flight ID to view booked seats: "))
        view_booked_seats(flight_id)

    elif choice == '13':
        print("Exiting the Flight Management System. Goodbye!")
        cursor.close()
        conn.close()
        break

    else:
        print("Invalid choice. Try again.")
