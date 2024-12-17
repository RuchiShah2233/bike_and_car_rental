import sqlite3

# Create database connection
conn = sqlite3.connect('rental-1.db')
cursor = conn.cursor()

# Update car table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS car (
        car_id INTEGER PRIMARY KEY AUTOINCREMENT,
        status TEXT DEFAULT 'free'
    )
''')

# Update bike table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS bike (
        bike_id INTEGER PRIMARY KEY AUTOINCREMENT,
        status TEXT DEFAULT 'free'    
    )
''')

# Update rental table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS rental (
        id INTEGER PRIMARY KEY,
        vehicle_id INTEGER,
        vehicle_type TEXT,
        rental_type TEXT,
        rental_time DATETIME,
        return_time DATETIME ,
        status TEXT DEFAULT 'rented' ,
        FOREIGN KEY (vehicle_id, vehicle_type) REFERENCES car(car_id, 'car') 
                                              ON DELETE CASCADE
                                              ON UPDATE CASCADE,
        FOREIGN KEY (vehicle_id, vehicle_type) REFERENCES bike(bike_id, 'bike') 
                                              ON DELETE CASCADE
                                              ON UPDATE CASCADE,
        CHECK (vehicle_type IN ('bike', 'car')),
        CHECK (rental_type IN ('hourly', 'daily', 'weekly'))
    )
''')


# Add car data

cursor.execute("INSERT INTO car (status) VALUES ('free')")
cursor.execute("INSERT INTO car (status) VALUES ('free')")
cursor.execute("INSERT INTO car (status) VALUES ('free')")
cursor.execute("INSERT INTO car (status) VALUES ('free')")
cursor.execute("INSERT INTO car (status) VALUES ('free')")
cursor.execute("INSERT INTO car (status) VALUES ('free')")
cursor.execute("INSERT INTO car (status) VALUES ('free')")
cursor.execute("INSERT INTO car (status) VALUES ('free')")
cursor.execute("INSERT INTO car (status) VALUES ('free')")
cursor.execute("INSERT INTO car (status) VALUES ('free')")


# Add bike data
cursor.execute("INSERT INTO bike (status) VALUES ('free')")
cursor.execute("INSERT INTO bike (status) VALUES ('free')")
cursor.execute("INSERT INTO bike (status) VALUES ('free')")
cursor.execute("INSERT INTO bike (status) VALUES ('free')")
cursor.execute("INSERT INTO bike (status) VALUES ('free')")
cursor.execute("INSERT INTO bike (status) VALUES ('free')")
cursor.execute("INSERT INTO bike (status) VALUES ('free')")
cursor.execute("INSERT INTO bike (status) VALUES ('free')")
cursor.execute("INSERT INTO bike (status) VALUES ('free')")
cursor.execute("INSERT INTO bike (status) VALUES ('free')")



# Save database connection
conn.commit()

# Close database connection
conn.close()
