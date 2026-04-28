import sqlite3
import os
from werkzeug.security import generate_password_hash

db_path = 'backend/cars.db'

def populate_more():
    if not os.path.exists(db_path):
        print("Database not found. Run init_db.py first.")
        return

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    
    # 1. Register New Seller
    email = 'mohan_seller@example.com'
    password = 'seller@123'
    hashed_pw = generate_password_hash(password)
    
    try:
        cur = conn.cursor()
        cur.execute('INSERT INTO Users (name, email, phone, password, location, role) VALUES (?, ?, ?, ?, ?, ?)',
                    ('Mohan Kumar', email, '9988776655', hashed_pw, 'Mumbai, India', 'seller'))
        user_id = cur.lastrowid
        print(f"New Seller created with ID: {user_id}")
    except sqlite3.IntegrityError:
        user = conn.execute('SELECT user_id FROM Users WHERE email = ?', (email,)).fetchone()
        user_id = user['user_id']
        print(f"Seller already exists with ID: {user_id}")

    # 2. Mock Car Data (20 cars - Previous & New Brands)
    # (brand, model, year, fuel, mileage, engine, trans, color, seats, price, cond)
    more_cars = [
        ('Toyota', 'Innova Crysta', 2020, 'Diesel', 40000, '2.4L Diesel', 'Manual', 'Silver', 7, 18000, 'Good'),
        ('Honda', 'Civic', 2018, 'Petrol', 50000, '1.8L i-VTEC', 'Automatic', 'White', 5, 22000, 'Excellent'),
        ('BMW', '3 Series', 2021, 'Petrol', 12000, '2.0L Turbo', 'Automatic', 'Blue', 5, 42000, 'Excellent'),
        ('Mercedes-Benz', 'E-Class', 2019, 'Diesel', 35000, '2.0L Diesel', 'Automatic', 'Black', 5, 38000, 'Good'),
        ('Volvo', 'XC90', 2022, 'Hybrid', 10000, '2.0L B6', 'Automatic', 'Grey', 7, 75000, 'Excellent'),
        ('Lexus', 'ES', 2021, 'Hybrid', 15000, '2.5L Hybrid', 'Automatic', 'White', 5, 52000, 'Excellent'),
        ('Land Rover', 'Defender', 2023, 'Diesel', 5000, '3.0L Diesel', 'Automatic', 'Green', 5, 95000, 'Excellent'),
        ('Jaguar', 'F-Pace', 2020, 'Petrol', 25000, '2.0L P250', 'Automatic', 'Red', 5, 48000, 'Good'),
        ('Porsche', 'Cayenne', 2021, 'Petrol', 18000, '3.0L V6', 'Automatic', 'White', 5, 110000, 'Excellent'),
        ('Jeep', 'Compass', 2022, 'Petrol', 14000, '1.4L MultiAir', 'Manual', 'Black', 5, 16000, 'Excellent'),
        ('Audi', 'Q7', 2019, 'Diesel', 42000, '3.0L V6 TDI', 'Automatic', 'Silver', 7, 52000, 'Good'),
        ('Tesla', 'Model Y', 2022, 'Electric', 10000, 'Dual Motor', 'Automatic', 'Blue', 5, 48000, 'Excellent'),
        ('Hyundai', 'Verna', 2021, 'Petrol', 20000, '1.5L Petrol', 'Manual', 'White', 5, 11000, 'Good'),
        ('Kia', 'Carnival', 2020, 'Diesel', 30000, '2.2L Diesel', 'Automatic', 'Black', 7, 24000, 'Excellent'),
        ('Mini', 'Cooper', 2021, 'Petrol', 15000, '2.0L Turbo', 'Automatic', 'Green', 4, 32000, 'Excellent'),
        ('Range Rover', 'Velar', 2022, 'Diesel', 12000, '2.0L Diesel', 'Automatic', 'White', 5, 82000, 'Excellent'),
        ('Skoda', 'Kodiaq', 2022, 'Petrol', 8000, '2.0L TSI', 'Automatic', 'Blue', 7, 34000, 'Excellent'),
        ('Volkswagen', 'Tiguan', 2021, 'Petrol', 16000, '2.0L TSI', 'Automatic', 'Grey', 5, 28000, 'Good'),
        ('MG', 'Astor', 2022, 'Petrol', 11000, '1.5L VTi', 'Manual', 'Silver', 5, 13000, 'Excellent'),
        ('Mahindra', 'XUV700', 2023, 'Diesel', 5000, '2.2L mHawk', 'Automatic', 'White', 7, 21000, 'Excellent')
    ]

    for brand, model, year, fuel, mileage, engine, trans, color, seats, price, cond in more_cars:
        # Insert Car
        cur.execute('INSERT INTO Cars (user_id, brand, model, year, fuel_type, mileage) VALUES (?, ?, ?, ?, ?, ?)',
                    (user_id, brand, model, year, fuel, mileage))
        car_id = cur.lastrowid
        
        # Insert Specs
        cur.execute('INSERT INTO CarSpecifications (car_id, engine, transmission, color, seats) VALUES (?, ?, ?, ?, ?)',
                    (car_id, engine, trans, color, seats))
        
        # Insert Listing
        cur.execute('INSERT INTO Listings (car_id, price, predicted_price, condition, status) VALUES (?, ?, ?, ?, ?)',
                    (car_id, price, price * 0.97, cond, 'available'))
        
        print(f"Added: {brand} {model} (${price})")

    conn.commit()
    conn.close()
    print("Population setup complete.")

if __name__ == "__main__":
    populate_more()
