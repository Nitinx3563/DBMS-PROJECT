import sqlite3
import os
from werkzeug.security import generate_password_hash
from datetime import datetime

db_path = 'backend/cars.db'

def populate_buyers():
    if not os.path.exists(db_path):
        print("Database not found. Run init_db.py first.")
        return

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    
    # 1. Register Buyers
    buyers_data = [
        ('Aman Verma', 'aman_buyer@example.com', '9000000001'),
        ('Priya Singh', 'priya_buyer@example.com', '9000000002'),
        ('Rahul Mehta', 'rahul_buyer@example.com', '9000000003')
    ]
    
    buyer_ids = []
    password = 'buyer@123'
    hashed_pw = generate_password_hash(password)
    
    for name, email, phone in buyers_data:
        try:
            cur = conn.cursor()
            cur.execute('INSERT INTO Users (name, email, phone, password, location, role) VALUES (?, ?, ?, ?, ?, ?)',
                        (name, email, phone, hashed_pw, 'Delhi, India', 'buyer'))
            buyer_ids.append(cur.lastrowid)
            print(f"Buyer created: {name}")
        except sqlite3.IntegrityError:
            user = conn.execute('SELECT user_id FROM Users WHERE email = ?', (email,)).fetchone()
            buyer_ids.append(user['user_id'])
            print(f"Buyer already exists: {name}")

    # 2. Add Mock Messages
    # Let's get some listings
    listings = conn.execute('SELECT listing_id, car_id FROM Listings LIMIT 5').fetchall()
    
    for i, listing in enumerate(listings):
        car = conn.execute('SELECT user_id FROM Cars WHERE car_id = ?', (listing['car_id'],)).fetchone()
        seller_id = car['user_id']
        buyer_id = buyer_ids[i % len(buyer_ids)]
        
        conn.execute('''
            INSERT INTO Messages (sender_id, receiver_id, listing_id, message) 
            VALUES (?, ?, ?, ?)
        ''', (buyer_id, seller_id, listing['listing_id'], f"Hi, I'm interested in this car. Is it still available?"))
        print(f"Message sent from Buyer {buyer_id} to Seller {seller_id}")

    # 3. Add Mock Reviews
    # Seller 1 (Rakshit) and Seller 2 (Mohan)
    sellers = [1, 2]
    for seller_id in sellers:
        for buyer_id in buyer_ids:
            conn.execute('''
                INSERT INTO Reviews (buyer_id, seller_id, rating, comment) 
                VALUES (?, ?, ?, ?)
            ''', (buyer_id, seller_id, 5 if buyer_id % 2 == 0 else 4, "Great experience dealing with this seller!"))
            print(f"Review added for Seller {seller_id} by Buyer {buyer_id}")

    # 4. Simulate a Transaction
    # Mark one car as sold via transaction
    listing_to_sell = conn.execute('SELECT listing_id, car_id, price FROM Listings WHERE status = "available" LIMIT 1').fetchone()
    if listing_to_sell:
        car = conn.execute('SELECT user_id FROM Cars WHERE car_id = ?', (listing_to_sell['car_id'],)).fetchone()
        conn.execute('''
            INSERT INTO Transactions (listing_id, buyer_id, seller_id, price) 
            VALUES (?, ?, ?, ?)
        ''', (listing_to_sell['listing_id'], buyer_ids[0], car['user_id'], listing_to_sell['price']))
        print(f"Transaction completed for Listing {listing_to_sell['listing_id']}. Trigger should mark it as SOLD.")

    conn.commit()
    conn.close()
    print("Buyer population and interactions complete.")

if __name__ == "__main__":
    populate_buyers()
