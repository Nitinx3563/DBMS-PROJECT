import sqlite3

def verify():
    conn = sqlite3.connect('backend/cars.db')
    conn.row_factory = sqlite3.Row

    # 1. Insert Sample Users
    conn.execute('INSERT INTO Users (name, email, phone, password, location, role) VALUES (?, ?, ?, ?, ?, ?)',
                 ('Alice Buyer', 'alice@example.com', '123456', 'plain_text_for_dbms_test', 'New York', 'buyer'))
    conn.execute('INSERT INTO Users (name, email, phone, password, location, role) VALUES (?, ?, ?, ?, ?, ?)',
                 ('Bob Seller', 'bob@example.com', '654321', 'plain_text_for_dbms_test', 'Los Angeles', 'seller'))

    # 2. Insert Sample Car & Listing
    conn.execute('''
        INSERT INTO Cars (user_id, brand, model, year, fuel_type, mileage) 
        VALUES (2, 'Tesla', 'Model 3', 2022, 'Electric', 15000)
    ''')
    car_id = 1
    conn.execute('''
        INSERT INTO CarSpecifications (car_id, engine, transmission, color, seats) 
        VALUES (?, 'Dual Motor', 'Automatic', 'White', 5)
    ''', (car_id,))
    conn.execute('''
        INSERT INTO Listings (car_id, price, predicted_price, condition) 
        VALUES (?, 45000, 44500, 'Excellent')
    ''', (car_id,))

    conn.commit()

    # 3. Check View
    print("Checking AvailableCars View:")
    rows = conn.execute('SELECT * FROM AvailableCars').fetchall()
    for row in rows:
        print(f"Car: {row['brand']} {row['model']} - Price: ${row['price']} - Seller: {row['seller_name']}")

    # 4. Test Trigger (Transaction)
    print("\nTesting Transaction Trigger:")
    listing_id = 1
    conn.execute('''
        INSERT INTO Transactions (listing_id, buyer_id, seller_id, price) 
        VALUES (?, 1, 2, 45000)
    ''', (listing_id,))
    conn.commit()

    status = conn.execute('SELECT status FROM Listings WHERE listing_id = ?', (listing_id,)).fetchone()
    print(f"Listing Status after Transaction: {status['status']}")

    conn.close()

if __name__ == "__main__":
    verify()
