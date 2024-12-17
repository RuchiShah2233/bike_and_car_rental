import datetime
import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox


class VehicleRental:
    def __init__(self, vehicle_type):
        self.vehicle_type = vehicle_type
        self.conn = sqlite3.connect('rental-1.db')
        self.cursor = self.conn.cursor()

    def rentalAdd(self, vehicle_id, rental_type):
        rental_time = datetime.datetime.now().strftime('%H:%M %d-%m-%Y ')
        self.cursor.execute(
            "INSERT INTO rental (vehicle_id, vehicle_type, rental_type, rental_time) VALUES (?, ?, ?, ?)",
            (vehicle_id, self.vehicle_type, rental_type, rental_time)
        )
        self.conn.commit()

        # Mark the vehicle as rented
        self.cursor.execute(f"UPDATE {self.vehicle_type} SET status='rented' WHERE {self.vehicle_type}_id=?", (vehicle_id,))
        self.conn.commit()

        message = f"{self.vehicle_type.capitalize()} ID={vehicle_id} {rental_type} as rented."
        self.show_message("Successful", message)

    def show_message(self, title, message):
        messagebox.showinfo(title, message)

    def stokGoster(self):
        stock_window = tk.Toplevel(self.root)
        stock_window.title(f"{self.vehicle_type.capitalize()} Stock Display")
        stock_window.geometry("500x300")

        label_frame = tk.LabelFrame(stock_window, text="", font=("Arial", 12, "bold"))
        label_frame.pack(pady=20)

        columns = ("ID", "Status")
        tree = ttk.Treeview(label_frame, columns=columns, show="headings")
        for col in columns:
            tree.heading(col, text=col)
        tree.pack()

        self.cursor.execute(f"SELECT {self.vehicle_type}_id, status FROM {self.vehicle_type}")
        result = self.cursor.fetchall()

        if result:
            for row in result:
                tree.insert("", "end", values=(row[0], row[1]))

    def hourlyRental(self, vehicle_id):
        if vehicle_id is None:
            return None
        else:
            self.cursor.execute("SELECT status FROM bike WHERE bike_id=?", (vehicle_id,))
            result = self.cursor.fetchone()

            print(f"Bike ID={vehicle_id} rented by hour.")
            self.rentalAdd(vehicle_id, 'hourly')
            self.conn.commit()  # Fix bike as vehicle type


    def dailyRental(self, vehicle_id):
        if vehicle_id is None:
            return None
        else:
            self.now = datetime.datetime.now()
            return_date = self.now + datetime.timedelta(days=1)
            return_date = return_date.strftime("%d-%m-%Y")
            self.cursor.execute(
                f"SELECT {self.vehicle_type}_id FROM {self.vehicle_type} WHERE status='free' AND {self.vehicle_type}_id=? LIMIT 1",
                (vehicle_id,))
            result = self.cursor.fetchone()

            print(f"{self.vehicle_type.capitalize()} ID={vehicle_id} rented daily.")
            self.rentalAdd(vehicle_id, 'daily')
            self.conn.commit()

    def weeklyRental(self, vehicle_id):
        if vehicle_id is None:
            return None
        else:
            self.now = datetime.datetime.now()
            return_date = self.now + datetime.timedelta(days=7)
            return_date = return_date.strftime("%d-%m-%Y")
            self.cursor.execute(
                f"SELECT {self.vehicle_type}_id FROM {self.vehicle_type} WHERE status='free' AND {self.vehicle_type}_id=? LIMIT 1",
                (vehicle_id,))
            result = self.cursor.fetchone()
            print(f"{self.vehicle_type.capitalize()} ID={vehicle_id} rented weekly.")
            self.rentalAdd(vehicle_id, 'weekly')
            self.conn.commit()


class BikeRental(VehicleRental):
    def __init__(self, root):
        super().__init__("bike")
        self.root = root
        self.connection = self.conn  # Add this line


class CarRental(VehicleRental):
    def __init__(self, root):
        super().__init__("car")
        self.root = root
        self.connection = self.conn

class Customer:
    def __init__(self):
        self.bikes = 0
        self.rentalTime_b = None
        self.cars = 0
        self.rentalTime_c = None

    def vehicleRequest(self, vehicle_type):
        conn = sqlite3.connect('rental-1.db')
        cursor = conn.cursor()
        if vehicle_type == "bike":
            cursor.execute(f"SELECT bike_id FROM bike WHERE status='free'")
            result = cursor.fetchall()
            if result:
                print(f"ID of available bikes: ")
                for row in result:
                    print(row[0])
                vehicle_id = int(input("Which bike ID would you like to rent? "))
                if vehicle_id in [row[0] for row in result]:
                    cursor.execute("UPDATE bike SET status='rented' WHERE bike_id=?", (vehicle_id,))
                    #print(f"Bike_id={vehicle_id} bike is rented.")
                    self.bikes = 1
                else:
                    print("No available bike with the specified ID was found.")
                    vehicle_id = None
            else:
                print("There is no bike available.")
                vehicle_id = None
        elif vehicle_type == "car":
            cursor.execute(f"SELECT car_id FROM car WHERE status='free'")
            result = cursor.fetchall()
            if result:
                print(f"ID of available cars: ")
                for row in result:
                    print(row[0])
                vehicle_id = int(input("Which car ID would you like to rent? "))
                if vehicle_id in [row[0] for row in result]:
                    cursor.execute("UPDATE car SET status='rented' WHERE car_id=?", (vehicle_id,))
                    #print(f"Car_id={vehicle_id} car is rented.")
                    self.cars = 1
                else:
                    print("No available car with the specified ID was found.")
                    vehicle_id = None
            else:
                print("There are no cars available.")
                vehicle_id = None
        else:
            print("Invalid vehicle request.")
            vehicle_id = None
        conn.commit()
        conn.close()
        return vehicle_id

    def calculate_invoice(self, vehicle_type, rental_basis, rental_duration):
        if vehicle_type == "bike":
            ucret = 0
            if rental_basis == 1:  # Hourly
                ucret = rental_duration * 30
            elif rental_basis == 2:  # Daily
                ucret = rental_duration * 150
            elif rental_basis == 3:  # Weekly
                ucret = rental_duration * 500
            return ucret
        elif vehicle_type == "car":
            ucret = 0
            if rental_basis == 1:  # Hourly
                ucret = rental_duration * 100
            elif rental_basis == 2:  # Daily
                ucret = rental_duration * 500
            elif rental_basis == 3:  # Weekly
                ucret = rental_duration * 1500
            return ucret
        else:
            return 0

    def vehicleReturn(self, vehicle_type):
        conn = sqlite3.connect('rental-1.db')
        cursor = conn.cursor()

        cursor.execute(
            f"SELECT  vehicle_id, rental_type, rental_time FROM rental WHERE vehicle_type=? AND status='rented'",
            (vehicle_type,)
        )
        result = cursor.fetchall()

        if result:
            print(f"Rented {vehicle_type} information: ")
            for row in result:
                print(f"Vehicle ID: {row[0]}, Rental Type: {row[1]}, Rental Time: {row[2]}")

            vehicle_id = int(input(f"Enter the {vehicle_type} ID you want to return: "))
            if any(vehicle_id == row[0] for row in result):
                cursor.execute(f"UPDATE {vehicle_type} SET status='free' WHERE {vehicle_type}_id=?", (vehicle_id,))
                return_time = datetime.datetime.now().strftime('%H:%M  %d-%m-%Y ')

                cursor.execute(
                    "UPDATE rental SET status='free', return_time=? WHERE vehicle_id=? AND status='rented'",
                    (return_time, vehicle_id,))

                print(
                    f"{vehicle_type.capitalize()} ID {vehicle_id} vehicle successfully returned. Return Time: {return_time}")
                conn.commit()
                if vehicle_type == "bike":
                    self.bikes -= 1
                elif vehicle_type == "car":
                    self.cars -= 1
                rental_basis = 0
                rental_duration = 0
                for row in result:
                    if row[0] == vehicle_id:
                        rental_basis = 1 if row[1] == 'hourly' else (2 if row[1] == 'daily' else 3)
                        rental_duration = (datetime.datetime.now() - datetime.datetime.strptime(row[2],
                                                                                                '%H:%M %d-%m-%Y ')).total_seconds() / 3600
                        break

                if rental_basis != 0 and rental_duration != 0:
                    ucret = self.calculate_invoice(vehicle_type, rental_basis, rental_duration)
                    print(f"Invoice: {ucret:.2f}TL")
                else:
                    print("The invoice could not be created.")

            else:
                print(f"Rented {vehicle_type} with the specified ID could not be found.")
        else:
            print(f"There are no rented {vehicle_type} to return.")

        conn.close()

