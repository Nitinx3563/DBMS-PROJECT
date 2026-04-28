import sqlite3
import os
from werkzeug.security import generate_password_hash

db_path = 'backend/cars.db'

def populate():
    if not os.path.exists(db_path):
        print("Database not found. Run init_db.py first.")
        return

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    
    # 1. Register the User
    email = 'rakshitsharma378@gmail.com'
    password = 'admin@123'
    hashed_pw = generate_password_hash(password)
    
    try:
        cur = conn.cursor()
        cur.execute('INSERT INTO Users (name, email, phone, password, location, role) VALUES (?, ?, ?, ?, ?, ?)',
                    ('Rakshit Sharma', email, '9876543210', hashed_pw, 'Delhi, India', 'seller'))
        user_id = cur.lastrowid
        print(f"User created with ID: {user_id}")
    except sqlite3.IntegrityError:
        user = conn.execute('SELECT user_id FROM Users WHERE email = ?', (email,)).fetchone()
        user_id = user['user_id']
        print(f"User already exists with ID: {user_id}")

    # 2. Mock Car Data (15 cars)
    mock_cars = [
        ('Toyota', 'Fortuner', 2021, 'Diesel', 35000, '2.8L Sigma 4', 'Automatic', 'White', 7, 32000, 'Excellent'),
        ('Honda', 'City', 2019, 'Petrol', 45000, '1.5L i-VTEC', 'Manual', 'Silver', 5, 8500, 'Good'),
        ('Hyundai', 'Creta', 2022, 'Petrol', 12000, '1.4L Turbo', 'Automatic', 'Black', 5, 16000, 'Excellent'),
        ('Maruti Suzuki', 'Swift', 2018, 'Petrol', 55000, '1.2L DualJet', 'Manual', 'Red', 5, 4500, 'Fair'),
        ('Tata', 'Nexon EV', 2023, 'Electric', 8000, 'Ziptron', 'Automatic', 'Blue', 5, 14500, 'Excellent'),
        ('Mahindra', 'Thar', 2022, 'Diesel', 15000, '2.2L mHawk', 'Manual', 'Grey', 4, 15500, 'Excellent'),
        ('Kia', 'Seltos', 2021, 'Diesel', 22000, '1.5L CRDi', 'Automatic', 'White', 5, 13500, 'Good'),
        ('BMW', 'X5', 2020, 'Diesel', 30000, '3.0L Inline-6', 'Automatic', 'Blue', 5, 55000, 'Excellent'),
        ('Mercedes-Benz', 'C-Class', 2017, 'Petrol', 60000, '2.0L Turbo', 'Automatic', 'Silver', 5, 22000, 'Good'),
        ('Ford', 'Endeavour', 2019, 'Diesel', 48000, '3.2L TDCi', 'Automatic', 'Black', 7, 28000, 'Good'),
        ('Volkswagen', 'Virtus', 2023, 'Petrol', 5000, '1.5L TSI', 'Automatic', 'Yellow', 5, 17000, 'Excellent'),
        ('Skoda', 'Slavia', 2022, 'Petrol', 10000, '1.0L TSI', 'Manual', 'Blue', 5, 12000, 'Excellent'),
        ('MG', 'Hector', 2021, 'Hybrid', 25000, '1.5L Turbo', 'Manual', 'White', 5, 14000, 'Good'),
        ('Nissan', 'Magnite', 2022, 'Petrol', 15000, '1.0L Turbo', 'Manual', 'Brown', 5, 7500, 'Good'),
        ('Audi', 'A4', 2021, 'Petrol', 18000, '2.0L TFSI', 'Automatic', 'White', 5, 38000, 'Excellent')
    ]

    for brand, model, year, fuel, mileage, engine, trans, color, seats, price, cond in mock_cars:
        # Check if listing already exists for this car model for this user
        existing = conn.execute('''
            SELECT L.listing_id FROM Listings L 
            JOIN Cars C ON L.car_id = C.car_id 
            WHERE C.user_id = ? AND C.brand = ? AND C.model = ? AND C.year = ?
        ''', (user_id, brand, model, year)).fetchone()
        
        if existing:
            print(f"Listing for {brand} {model} already exists.")
            continue

        # Insert Car
        cur.execute('INSERT INTO Cars (user_id, brand, model, year, fuel_type, mileage) VALUES (?, ?, ?, ?, ?, ?)',
                    (user_id, brand, model, year, fuel, mileage))
        car_id = cur.lastrowid
        
        # Insert Specs
        cur.execute('INSERT INTO CarSpecifications (car_id, engine, transmission, color, seats) VALUES (?, ?, ?, ?, ?)',
                    (car_id, engine, trans, color, seats))
        
        # Insert Listing (Predicted price is set to random near price for mock data)
        cur.execute('INSERT INTO Listings (car_id, price, predicted_price, condition, status) VALUES (?, ?, ?, ?, ?)',
                    (car_id, price, price * 0.98, cond, 'available'))
        
        print(f"Added: {brand} {model} (${price})")

    conn.commit()
    conn.close()
    print("Population complete.")

if __name__ == "__main__":
    populate()
