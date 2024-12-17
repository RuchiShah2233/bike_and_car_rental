import tkinter as tk
from tkinter import ttk, messagebox
from rent import BikeRental, CarRental, Customer
import datetime

class RentalApplication:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Rental Application")
        self.root.geometry("600x250")

        self.bike_rental = BikeRental(self.root)
        self.car_rental = CarRental(self.root)
        self.customer = Customer()
        self.selected_bike_id = None

        self.create_main_menu()

    def create_main_menu(self):
        main_label = tk.Label(self.root, text="Rental Application", font=("Arial", 24, "bold", "italic"))
        main_label.pack(pady=20)

        frame = tk.Frame(self.root)
        frame.pack()

        bike_button = tk.Button(frame, text="Bike Rental", command=self.show_bike_menu, width=20, height=2,
                                    bg="purple", fg="white", font=("Arial", 12))
        bike_button.grid(row=0, column=0, padx=20, pady=10)

        car_button = tk.Button(frame, text="Car Rental", command=self.show_car_menu, width=20, height=2,
                                 bg="purple", fg="white", font=("Arial", 12))
        car_button.grid(row=0, column=1, padx=20, pady=10)

        exit_button = tk.Button(self.root, text="Exit", command=self.root.destroy, font=("Helvetica", 12), width=10, bg="gray")
        exit_button.pack(pady=20)

    def show_bike_menu(self):
        bike_menu_window = tk.Toplevel(self.root)
        bike_menu_window.title("BIKE RENTAL MENU")
        bike_menu_window.geometry("500x450")

        bike_label = tk.Label(bike_menu_window, text="BIKE RENTAL MENU", font=("Arial", 20, "bold"))
        bike_label.pack(pady=20)

        show_bike_button = tk.Button(bike_menu_window, text="Show Available Bikes",
                                     command=self.bike_rental.stokGoster, width=30, height=2)

        show_bike_button.pack(pady=10)

        hourly_bike_button = tk.Button(bike_menu_window, text="Request bike per hour (30 TL)", command=self.request_bike_hourly, width=30, height=2)
        hourly_bike_button.pack(pady=10)

        daily_bike_button = tk.Button(bike_menu_window, text="Request bike daily (150 TL)", command=self.request_bike_daily, width=30, height=2)
        daily_bike_button.pack(pady=10)

        weekly_bike_button = tk.Button(bike_menu_window, text="Request bike weekly (500 TL)", command=self.request_bike_weekly, width=30, height=2)
        weekly_bike_button.pack(pady=10)

        return_bike_button = tk.Button(bike_menu_window, text="Return bike", command=self.return_bike, width=30, height=2)
        return_bike_button.pack(pady=10)

        back_button = tk.Button(bike_menu_window, text="Main Menu", command=bike_menu_window.destroy, width=30, height=2)
        back_button.pack(pady=10)

    def show_car_menu(self):
        car_menu_window = tk.Toplevel(self.root)
        car_menu_window.title("CAR RENTAL MENU")
        car_menu_window.geometry("500x450")

        car_label = tk.Label(car_menu_window, text="CAR RENTAL MENU", font=("Arial", 20, "bold"))
        car_label.pack(pady=20)

        show_car_button = tk.Button(car_menu_window, text="Show Available Cars", command=self.car_rental.stokGoster, width=30, height=2)
        show_car_button.pack(pady=10)

        hourly_car_button = tk.Button(car_menu_window, text="Request car per hour (100 TL)", command=self.request_car_hourly, width=30, height=2)
        hourly_car_button.pack(pady=10)

        daily_car_button = tk.Button(car_menu_window, text="Request car daily (500 TL)", command=self.request_car_daily, width=30, height=2)
        daily_car_button.pack(pady=10)

        weekly_car_button = tk.Button(car_menu_window, text="Request car weekly (1500 TL)", command=self.request_car_weekly, width=30, height=2)
        weekly_car_button.pack(pady=10)

        return_car_button = tk.Button(car_menu_window, text="Return car", command=self.return_car, width=30, height=2)
        return_car_button.pack(pady=10)

        back_button = tk.Button(car_menu_window, text="Main Menü", command=car_menu_window.destroy, width=30, height=2)
        back_button.pack(pady=10)

    def request_bike_hourly(self):
        hourly_bike_window = tk.Toplevel(self.root)
        hourly_bike_window.title("Request Bike per Hour")
        hourly_bike_window.geometry("650x300")

        label_frame = tk.LabelFrame(hourly_bike_window, text="", font=("Arial", 12, "bold"))
        label_frame.pack(pady=20)

        columns = ("ID", "Status", "Choice")
        tree = ttk.Treeview(label_frame, columns=columns, show="headings")
        for col in columns:
            tree.heading(col, text=col)
        tree.pack()

        self.bike_rental.cursor.execute(
            f"SELECT {self.bike_rental.vehicle_type}_id, status FROM {self.bike_rental.vehicle_type} WHERE status='free'")
        result = self.bike_rental.cursor.fetchall()

        if result:
            for row in result:
                tree.insert("", "end", values=(row[0], row[1], "Select"), tags="button")

            def select_bike(event):
                item = tree.item(tree.focus())
                if item['values'] and item['values'][2] == "Select":
                    # Update the instance variable
                    self.selected_bike_id = item['values'][0]
                    self.confirm_hourly_bike(self.selected_bike_id, hourly_bike_window)

            tree.tag_bind("button", "<ButtonRelease-1>", select_bike)

        else:
            no_data_label = tk.Label(label_frame, text=f"There is no {self.bike_rental.vehicle_type} available.", font=("Arial", 12),
                                     pady=5)
            no_data_label.grid(row=1, column=0, sticky="w", padx=10)

    def confirm_hourly_bike(self, selected_bike_id, window):
        # Close second window
        window.destroy()

        # Rent a bike by the hour
        self.customer.rentalTime_b = self.bike_rental.hourlyRental(selected_bike_id)
        self.customer.rentalBasis_b = 1

    def request_bike_daily(self):
        daily_bike_window = tk.Toplevel(self.root)
        daily_bike_window.title("Request Bike Daily")
        daily_bike_window.geometry("650x300")

        label_frame = tk.LabelFrame(daily_bike_window, text="", font=("Arial", 12, "bold"))
        label_frame.pack(pady=20)

        columns = ("ID", "Status", "Choice")
        tree = ttk.Treeview(label_frame, columns=columns, show="headings")
        for col in columns:
            tree.heading(col, text=col)
        tree.pack()

        self.bike_rental.cursor.execute(
            f"SELECT {self.bike_rental.vehicle_type}_id, status FROM {self.bike_rental.vehicle_type} WHERE status='free'")
        result = self.bike_rental.cursor.fetchall()

        if result:
            for row in result:
                tree.insert("", "end", values=(row[0], row[1], "Select"), tags="button")

            def select_bike(event):
                item = tree.item(tree.focus())
                if item['values'] and item['values'][2] == "Select":
                    selected_bike_id = item['values'][0]
                    self.confirm_daily_bike(selected_bike_id, daily_bike_window)

            tree.tag_bind("button", "<ButtonRelease-1>", select_bike)

        else:
            no_data_label = tk.Label(label_frame, text=f"There is no {self.bike_rental.vehicle_type} available.", font=("Arial", 12),
                                     pady=5)
            no_data_label.grid(row=1, column=0, sticky="w", padx=10)

    def confirm_daily_bike(self, selected_bike_id, window):
        window.destroy()

        self.customer.rentalTime_b = self.bike_rental.dailyRental(selected_bike_id)
        self.customer.rentalBasis_b = 2

    def request_bike_weekly(self):
        weekly_bike_window = tk.Toplevel(self.root)
        weekly_bike_window.title("Request Bike Weekly")
        weekly_bike_window.geometry("650x300")

        label_frame = tk.LabelFrame(weekly_bike_window, text="", font=("Arial", 12, "bold"))
        label_frame.pack(pady=20)

        columns = ("ID", "Status", "Choice")
        tree = ttk.Treeview(label_frame, columns=columns, show="headings")
        for col in columns:
            tree.heading(col, text=col)
        tree.pack()

        self.bike_rental.cursor.execute(
            f"SELECT {self.bike_rental.vehicle_type}_id, status FROM {self.bike_rental.vehicle_type} WHERE status='free'")
        result = self.bike_rental.cursor.fetchall()

        if result:
            for row in result:
                tree.insert("", "end", values=(row[0], row[1], "Select"), tags="button")

            def select_bike(event):
                item = tree.item(tree.focus())
                if item['values'] and item['values'][2] == "Select":
                    selected_bike_id = item['values'][0]
                    self.confirm_weekly_bike(selected_bike_id, weekly_bike_window)

            tree.tag_bind("button", "<ButtonRelease-1>", select_bike)

        else:
            no_data_label = tk.Label(label_frame, text=f"There is no {self.bike_rental.vehicle_type} available.", font=("Arial", 12),
                                     pady=5)
            no_data_label.grid(row=1, column=0, sticky="w", padx=10)

    def confirm_weekly_bike(self, selected_bike_id, window):
        window.destroy()

        self.customer.rentalTime_b = self.bike_rental.weeklyRental(selected_bike_id)
        self.customer.rentalBasis_b = 3

    def request_car_hourly(self):
        hourly_car_window = tk.Toplevel(self.root)
        hourly_car_window.title("Request Car per Hour")
        hourly_car_window.geometry("650x300")

        label_frame = tk.LabelFrame(hourly_car_window, text="", font=("Arial", 12, "bold"))
        label_frame.pack(pady=20)

        columns = ("ID", "Status", "Choice")
        tree = ttk.Treeview(label_frame, columns=columns, show="headings")
        for col in columns:
            tree.heading(col, text=col)
        tree.pack()

        self.car_rental.cursor.execute(
            f"SELECT {self.car_rental.vehicle_type}_id, status FROM {self.car_rental.vehicle_type} WHERE status='free'")
        result = self.car_rental.cursor.fetchall()

        if result:
            for row in result:
                tree.insert("", "end", values=(row[0], row[1], "Select"), tags="button")

            def select_car(event):
                item = tree.item(tree.focus())
                if item['values'] and item['values'][2] == "Select":
                    selected_car_id = item['values'][0]
                    self.confirm_hourly_car(selected_car_id, hourly_car_window)

            tree.tag_bind("button", "<ButtonRelease-1>", select_car)

        else:
            no_data_label = tk.Label(label_frame, text=f"There is no {self.car_rental.vehicle_type} available.", font=("Arial", 12),
                                     pady=5)
            no_data_label.grid(row=1, column=0, sticky="w", padx=10)

    def confirm_hourly_car(self, selected_car_id, window):
        window.destroy()

        self.customer.rentalTime_c = self.car_rental.hourlyRental(selected_car_id)
        self.customer.rentalBasis_c = 1

    def request_car_daily(self):
        daily_car_window = tk.Toplevel(self.root)
        daily_car_window.title("Request Car Daily")
        daily_car_window.geometry("650x300")

        label_frame = tk.LabelFrame(daily_car_window, text="", font=("Arial", 12, "bold"))
        label_frame.pack(pady=20)

        columns = ("ID", "Status", "Choice")
        tree = ttk.Treeview(label_frame, columns=columns, show="headings")
        for col in columns:
            tree.heading(col, text=col)
        tree.pack()

        self.car_rental.cursor.execute(
            f"SELECT {self.car_rental.vehicle_type}_id, status FROM {self.car_rental.vehicle_type} WHERE status='free'")
        result = self.car_rental.cursor.fetchall()

        if result:
            for row in result:
                tree.insert("", "end", values=(row[0], row[1], "Select"), tags="button")

            def select_car(event):
                item = tree.item(tree.focus())
                if item['values'] and item['values'][2] == "Select":
                    selected_car_id = item['values'][0]
                    self.confirm_daily_car(selected_car_id, daily_car_window)

            tree.tag_bind("button", "<ButtonRelease-1>", select_car)

        else:
            no_data_label = tk.Label(label_frame, text=f"There is no {self.car_rental.vehicle_type} available.", font=("Arial", 12),
                                     pady=5)
            no_data_label.grid(row=1, column=0, sticky="w", padx=10)

    def confirm_daily_car(self, selected_car_id, window):
        window.destroy()

        self.customer.rentalTime_c = self.car_rental.dailyRental(selected_car_id)
        self.customer.rentalBasis_c = 2

    def request_car_weekly(self):
        weekly_car_window = tk.Toplevel(self.root)
        weekly_car_window.title("Request Car Weekly")
        weekly_car_window.geometry("650x300")

        label_frame = tk.LabelFrame(weekly_car_window, text="", font=("Arial", 12, "bold"))
        label_frame.pack(pady=20)

        columns = ("ID", "Status", "Choice")
        tree = ttk.Treeview(label_frame, columns=columns, show="headings")
        for col in columns:
            tree.heading(col, text=col)
        tree.pack()

        self.car_rental.cursor.execute(
            f"SELECT {self.car_rental.vehicle_type}_id, status FROM {self.car_rental.vehicle_type} WHERE status='free'")
        result = self.car_rental.cursor.fetchall()

        if result:
            for row in result:
                tree.insert("", "end", values=(row[0], row[1], "Select"), tags="button")

            def select_car(event):
                item = tree.item(tree.focus())
                if item['values'] and item['values'][2] == "Select":
                    selected_car_id = item['values'][0]
                    self.confirm_weekly_car(selected_car_id, weekly_car_window)

            tree.tag_bind("button", "<ButtonRelease-1>", select_car)

        else:
            no_data_label = tk.Label(label_frame, text=f"There is no {self.car_rental.vehicle_type} available.", font=("Arial", 12),
                                     pady=5)
            no_data_label.grid(row=1, column=0, sticky="w", padx=10)

    def confirm_weekly_car(self, selected_car_id, window):
        window.destroy()

        self.customer.rentalTime_c = self.car_rental.weeklyRental(selected_car_id)
        self.customer.rentalBasis_c = 3

    # AracKiralamaUygulamasi sınıfında iade fonksiyonları
    def return_bike(self):
        return_window = tk.Toplevel(self.root)
        return_window.title("Bike Return")
        return_window.geometry("950x300")

        label_frame = tk.LabelFrame(return_window, text="", font=("Arial", 12, "bold"))
        label_frame.pack(pady=20)

        columns = ("ID", "Status", "Rental Type", "Rental Time", "Choice")
        tree = ttk.Treeview(label_frame, columns=columns, show="headings")
        for col in columns:
            tree.heading(col, text=col)
        tree.pack()

        self.bike_rental.cursor.execute(
            f"SELECT r.vehicle_id, b.status, r.rental_type, r.rental_time FROM rental r JOIN bike b ON r.vehicle_id = b.bike_id WHERE b.status='rented'"
        )

        result = self.bike_rental.cursor.fetchall()

        if result:
            for row in result:
                tree.insert("", "end", values=(row[0], row[1], row[2],row[3], "Select"), tags="button")

            def select_bike_for_return(event):
                item = tree.item(tree.focus())
                if item['values'] and item['values'][4] == "Select":
                    selected_bike_id = item['values'][0]
                    self.confirm_return_bike(selected_bike_id, return_window)

            tree.tag_bind("button", "<ButtonRelease-1>", select_bike_for_return)
        else:
            no_data_label = tk.Label(label_frame, text=f"The bike to be returned could not be found.",
                                     font=("Arial", 12), pady=5)
            no_data_label.pack()  # Change here

    def confirm_return_bike(self, selected_bike_id, window):
        window.destroy()

        # Perform a refund
        cursor = self.bike_rental.cursor

        # Fetching rental_type and status based on bike_id
        cursor.execute("SELECT id, rental_type, status FROM rental WHERE vehicle_id=? AND status='rented'",
                       (selected_bike_id,))
        result = cursor.fetchone()

        if result:
            rental_id, rental_type, status = result

            # Update bike status as available
            cursor.execute(f"UPDATE bike SET status='free' WHERE bike_id=?", (selected_bike_id,))

            # Update return time
            return_time = datetime.datetime.now().strftime('%H:%M %d-%m-%Y ')
            cursor.execute(
                f"UPDATE rental SET status='free', return_time=? WHERE vehicle_id=? AND status='rented'",
                (return_time, selected_bike_id)
            )

            # Bu değişiklikleri kaydet
            self.bike_rental.connection.commit()

            # Display confirmation message with rental_id, rental_type, and status
            messagebox.showinfo("Successful",
                                f"Bike ID: {selected_bike_id}, Rental ID: {rental_id}, Rental Type: {rental_type}, Status: {status}, Return Time: {return_time}")
            self.root.update()
        else:
            # Handle the case where information is not found (you can show an error message)
            messagebox.showerror("Error", f"No rental information was found for the selected bike.")

    def return_car(self):
        return_window = tk.Toplevel(self.root)
        return_window.title("Car Return")
        return_window.geometry("950x300")

        label_frame = tk.LabelFrame(return_window, text="", font=("Arial", 12, "bold"))
        label_frame.pack(pady=20)

        columns = ("ID", "Status", "Rental Type", "Rental Time", "Choice")
        tree = ttk.Treeview(label_frame, columns=columns, show="headings")
        for col in columns:
            tree.heading(col, text=col)
        tree.pack()

        self.car_rental.cursor.execute(
            f"SELECT r.vehicle_id, c.status, r.rental_type, r.rental_time FROM rental r JOIN car c ON r.vehicle_id = c.car_id WHERE c.status='rented'"
        )

        result = self.car_rental.cursor.fetchall()

        if result:
            for row in result:
                tree.insert("", "end", values=(row[0], row[1], row[2], row[3], "Select"), tags="button")

            def select_car_for_return(event):
                item = tree.item(tree.focus())
                if item['values'] and item['values'][4] == "Select":
                    selected_car_id = item['values'][0]
                    self.confirm_return_car(selected_car_id, return_window)

            tree.tag_bind("button", "<ButtonRelease-1>", select_car_for_return)
        else:
            no_data_label = tk.Label(label_frame, text=f"Could not find {self.car_rental.vehicle_type} to return.",
                                     font=("Arial", 12), pady=5)
            no_data_label.pack()

    def confirm_return_car(self, selected_car_id, window):
        window.destroy()

        # İade işlemi gerçekleştir
        cursor = self.car_rental.cursor
        cursor.execute(f"UPDATE car SET status='free' WHERE car_id=?", (selected_car_id,))

        # İade zamanını güncelle
        return_time = datetime.datetime.now().strftime('%H:%M %d-%m-%Y ')
        cursor.execute(
            f"UPDATE kiralama SET status='free', return_time=? WHERE vehicle_id=? AND status='rented'",
            (return_time, selected_car_id)
        )

        # Bu değişiklikleri kaydet
        self.car_rental.connection.commit()

        messagebox.showinfo("Successful",
                            f"Car ID {selected_car_id} was returned successfully. Return Time: {return_time}")
        self.root.update()


if __name__ == "__main__":
    app = RentalApplication()
    app.root.mainloop()
