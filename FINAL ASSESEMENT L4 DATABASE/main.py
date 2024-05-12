import sqlite3 as db
from datetime import datetime


connection = db.connect("h2.db")
cursor = connection.cursor()

#this will delete a table if it already exists in the database #
cursor.execute("""
DROP TABLE IF EXISTS Customers
""")
cursor.execute("""
DROP TABLE IF EXISTS Rooms
""")

cursor.execute("""
DROP TABLE IF EXISTS Bookings
""")

#This created the tables#

cursor.execute("""
CREATE TABLE IF NOT EXISTS Customers (
    CustomerID INTEGER PRIMARY KEY AUTOINCREMENT,
    FirstName TEXT,
    Surname TEXT,
    Postcode TEXT,
    HouseNumber INTEGER
    
)
               
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Rooms (
    RoomID INTEGER PRIMARY KEY AUTOINCREMENT,
    RoomReference TEXT UNIQUE,
    Capacity INTEGER,
    Facilities TEXT,
    HirePrice REAL
    
)
               
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Bookings (
    BookingID INTEGER PRIMARY KEY AUTOINCREMENT,
    RoomID INTEGER,
    CustomerID INTEGER,
    BookingDate TEXT,
    Notes TEXT,
    FOREIGN KEY(RoomID) REFERENCES Rooms(RoomID),
    FOREIGN KEY(CustomerID) REFERENCES Customers(CustomerID)
    
)
               
""")

connection.commit()



class HotelBookingSystem:
    def __init__(self, db_file ):
        self.connection = db.connect(db_file)
        self.cursor = self.connection.cursor()

#function to create the customer#

    def create_customer(self, first_name, surname, postcode, house_number):
        self.cursor.execute("""
        INSERT INTO Customers (FirstName, Surname, Postcode, HouseNumber) 
        VALUES (?, ?, ?, ?)
        """, (first_name, surname, postcode, house_number))
        self.connection.commit()
        return self.cursor.lastrowid

#fucntion to view customers#

    def view_all_customers(self):
        self.cursor.execute("SELECT * FROM Customers")
        return self.cursor.fetchall()

#Function to update customers#

    def update_customer(self, customer_id, first_name, surname, postcode, house_number):
        self.cursor.execute("""
        UPDATE Customers 
        SET FirstName=?, Surname=?, Postcode=?, HouseNumber=? 
        WHERE CustomerID=?
        """, (first_name, surname, postcode, house_number, customer_id))
        self.connection.commit()

#fucntion to delete customer#

    def delete_customer(self, customer_id):
        self.cursor.execute("""
        DELETE FROM Customers WHERE CustomerID=?
        """, (customer_id,))
        self.connection.commit()

#Function to create a room#

    def create_room(self, room_reference, capacity, facilities, hire_price):
        self.cursor.execute("""
        INSERT INTO Rooms (RoomReference, Capacity, Facilities, HirePrice) 
        VALUES (?, ?, ?, ?)
        """, (room_reference, capacity, facilities, hire_price))
        self.connection.commit()
        return self.cursor.lastrowid

    def view_all_rooms(self):
        self.cursor.execute("SELECT * FROM Rooms")
        return self.cursor.fetchall()

    def update_room(self, room_id, room_reference, capacity, facilities, hire_price):
        self.cursor.execute("""
        UPDATE Rooms 
        SET RoomReference=?, Capacity=?, Facilities=?, HirePrice=? 
        WHERE RoomID=?
        """, (room_reference, capacity, facilities, hire_price, room_id))
        self.connection.commit()

    def delete_room(self, room_id):
        self.cursor.execute("""
        DELETE FROM Rooms WHERE RoomID=?
        """, (room_id,))
        self.connection.commit()

    def make_booking(self, room_id, customer_id, booking_date, notes=""):
        self.cursor.execute("""
        INSERT INTO Bookings (RoomID, CustomerID, BookingDate, Notes) 
        VALUES (?, ?, ?, ?)
        """, (room_id, customer_id, booking_date, notes))
        self.connection.commit()
        return self.cursor.lastrowid

    def search_booking_by_customer_name(self, customer_name):
        self.cursor.execute("""
        SELECT * FROM Bookings 
        WHERE CustomerID IN (SELECT CustomerID FROM Customers WHERE FirstName LIKE ? OR Surname LIKE ?)
        """, ('%' + customer_name + '%', '%' + customer_name + '%'))
        return self.cursor.fetchall()

    def search_booking_by_date(self, booking_date):
        self.cursor.execute("""
        SELECT * FROM Bookings WHERE BookingDate = ?
        """, (booking_date,))
        return self.cursor.fetchall()

    def search_booking_by_group_name(self, group_name):
        self.cursor.execute("""
        SELECT * FROM Bookings 
        WHERE CustomerID IN (SELECT CustomerID FROM Customers WHERE GroupName LIKE ?)
        """, ('%' + group_name + '%',))
        return self.cursor.fetchall()

    def close_connection(self):
        self.connection.close()


if __name__ == "__main__":
    system = HotelBookingSystem("h2.db")

    while True:
        print("\nHotel Booking System Menu:")
        print("1. Create a new customer")
        print("2. View all customers")
        print("3. Update a customer")
        print("4. Delete a customer")
        print("5. Create a new room")
        print("6. View all rooms")
        print("7. Update a room")
        print("8. Delete a room")
        print("9. Make a booking")
        print("10. Search bookings by customer name")
        print("11. Search bookings by date")
        print("12. Search bookings by group name")
        print("13. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            first_name = input("First name: ")
            surname = input("Surname: ")
            postcode = input("Postcode: ")
            house_number = input("House number: ")
            system.create_customer(first_name, surname, postcode, house_number)
            print("Customer created successfully.")
        elif choice == "2":
            customers = system.view_all_customers()
            for customer in customers:
                print(customer)
        elif choice == "3":
            customer_id = input("Enter customer ID to update: ")
            first_name = input("First name: ")
            surname = input("Surname: ")
            postcode = input("Postcode: ")
            house_number = input("House number: ")
            system.update_customer(customer_id, first_name, surname, postcode, house_number)
            print("Customer updated successfully.")
        elif choice == "4":
            customer_id = input("Enter customer ID to delete: ")
            system.delete_customer(customer_id)
            print("Customer deleted successfully.")
        elif choice == "5":
            room_reference = input("Room reference: ")
            capacity = int(input("Capacity: "))
            facilities = input("Facilities: ")
            hire_price = float(input("Hire price: "))
            system.create_room(room_reference, capacity, facilities, hire_price)
            print("Room created successfully.")
        elif choice == "6":
            rooms = system.view_all_rooms()
            for room in rooms:
                print(room)
        elif choice == "7":
            room_id = input("Enter room ID to update: ")
            room_reference = input("Room reference: ")
            capacity = int(input("Capacity: "))
            facilities = input("Facilities: ")
            hire_price = float(input("Hire price: "))
            system.update_room(room_id, room_reference, capacity, facilities, hire_price)
            print("Room updated successfully.")
        elif choice == "8":
            room_id = input("Enter room ID to delete: ")
            system.delete_room(room_id)
            print("Room deleted successfully.")
        elif choice == "9":
            room_id = input("Enter room ID for booking: ")
            customer_id = input("Enter customer ID for booking: ")
            booking_date = input("Enter booking date (DD-MM-YYYY): ")
            booking_date = datetime.strptime(booking_date, "%Y-%m-%d")
            notes = input("Enter notes: ")
            system.make_booking(room_id, customer_id, booking_date, notes)
            print("Booking created successfully.")
        elif choice == "10":
            customer_name = input("Enter customer name: ")
            bookings = system.search_booking_by_customer_name(customer_name)
            for booking in bookings:
                print(booking)
        elif choice == "11":
            booking_date = input("Enter booking date (DD-MM-YYYY): ")
            bookings = system.search_booking_by_date(booking_date)
            for booking in bookings:
                print(booking)
        elif choice == "12":
            group_name = input("Enter group name: ")
            bookings = system.search_booking_by_group_name(group_name)
            for booking in bookings:
                print(booking)
        elif choice == "13":
            print("Exiting...")
            system.close_connection()
            break
        else:
            print("Invalid choice. Please enter a number from 1 to 13.")

connection.close()
