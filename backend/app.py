import sqlite3
import os
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from algorithms import quick_sort, merge_sort, get_best_value_cars, binary_search_price_range

app = Flask(__name__, 
            template_folder='frontend/templates',
            static_folder='frontend/static')
app.secret_key = 'supersecretkey_for_college_project'

# Database configuration
DATABASE = 'cars.db'

def get_db_connection():
    db_path = os.path.join(os.path.dirname(__file__), DATABASE)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

# Initialization: Ensure database is set up correctly (handled via schema.sql already)

# --- AUTH ROUTES ---

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        password = request.form['password']
        location = request.form['location']
        role = request.form['role']
        
        hashed_pw = generate_password_hash(password)
        
        conn = get_db_connection()
        try:
            conn.execute('INSERT INTO Users (name, email, phone, password, location, role) VALUES (?, ?, ?, ?, ?, ?)',
                         (name, email, phone, hashed_pw, location, role))
            conn.commit()
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('Email already exists!', 'danger')
        finally:
            conn.close()
            
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM Users WHERE email = ?', (email,)).fetchone()
        conn.close()
        
        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['user_id']
            session['name'] = user['name']
            session['role'] = user['role']
            flash(f'Welcome back, {user["name"]}!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password.', 'danger')
            
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

# --- MAIN ROUTES ---

@app.route('/')
def index():
    conn = get_db_connection()
    # Get some featured listings using the view
    all_listings = conn.execute('SELECT * FROM AvailableCars').fetchall()
    listings = all_listings[:6] # Top 6 for featured
    
    # GREEDY RECOMMENDATION: Best Value Cars under $50,000
    recommendations = get_best_value_cars(all_listings, budget=50000, top_n=3)
    
    conn.close()
    return render_template('index.html', listings=listings, recommendations=recommendations)

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
        
    conn = get_db_connection()
    # If seller, show their listings
    my_listings = conn.execute('''
        SELECT L.*, C.brand, C.model, C.year 
        FROM Listings L 
        JOIN Cars C ON L.car_id = C.car_id 
        WHERE C.user_id = ?
    ''', (session['user_id'],)).fetchall()
    
    # Simple message count (bonus)
    messages = conn.execute('''
        SELECT M.*, U.name as sender_name 
        FROM Messages M 
        JOIN Users U ON M.sender_id = U.user_id 
        WHERE M.receiver_id = ? 
        ORDER BY timestamp DESC
    ''', (session['user_id'],)).fetchall()
    
    conn.close()
    return render_template('dashboard.html', listings=my_listings, messages=messages)

@app.route('/add_car', methods=['GET', 'POST'])
def add_car():
    if 'user_id' not in session:
        return redirect(url_for('login'))
        
    if request.method == 'POST':
        # Car details
        brand = request.form['brand']
        model = request.form['model']
        year = int(request.form['year'])
        fuel_type = request.form['fuel_type']
        mileage = int(request.form['mileage'])
        
        # Specs
        engine = request.form['engine']
        transmission = request.form['transmission']
        color = request.form['color']
        seats = int(request.form['seats'])
        
        # Listing
        price = float(request.form['price'])
        condition = request.form['condition']
        
        conn = get_db_connection()
        
        # PRICE PREDICTION LOGIC (SQL based)
        # Calculate avg price for same brand, model, year
        pred_data = conn.execute('''
            SELECT AVG(price) as avg_p 
            FROM Listings L 
            JOIN Cars C ON L.car_id = C.car_id 
            WHERE C.brand = ? AND C.model = ? AND C.year = ?
        ''', (brand, model, year)).fetchone()
        
        predicted_price = pred_data['avg_p'] if pred_data['avg_p'] else price # Default to current price if no data
        
        # Insert Car
        cur = conn.cursor()
        cur.execute('INSERT INTO Cars (user_id, brand, model, year, fuel_type, mileage) VALUES (?, ?, ?, ?, ?, ?)',
                    (session['user_id'], brand, model, year, fuel_type, mileage))
        car_id = cur.lastrowid
        
        # Insert Specs
        cur.execute('INSERT INTO CarSpecifications (car_id, engine, transmission, color, seats) VALUES (?, ?, ?, ?, ?)',
                    (car_id, engine, transmission, color, seats))
        
        # Insert Listing
        cur.execute('INSERT INTO Listings (car_id, price, predicted_price, condition) VALUES (?, ?, ?, ?)',
                    (car_id, price, predicted_price, condition))
        
        conn.commit()
        conn.close()
        flash('Listing added successfully!', 'success')
        return redirect(url_for('dashboard'))
        
    return render_template('add_car.html')

@app.route('/search')
def search():
    brand = request.args.get('brand', '')
    max_price = request.args.get('max_price', '')
    fuel_type = request.args.get('fuel_type', '')
    sort_by = request.args.get('sort_by', 'newest') # Default sort
    
    # Initial query for basic filters (Brand, Fuel Type)
    query = 'SELECT * FROM AvailableCars WHERE 1=1'
    params = []
    
    if brand:
        query += ' AND brand LIKE ?'
        params.append(f'%{brand}%')
    if fuel_type:
        query += ' AND fuel_type = ?'
        params.append(fuel_type)
        
    conn = get_db_connection()
    db_results = [dict(row) for row in conn.execute(query, params).fetchall()]
    conn.close()
    
    results = db_results
    
    # --- DAA INTEGRATION: SORTING ---
    # We sort the data in Python using our manual implementations
    if sort_by == 'price_low':
        results = quick_sort(results, 'price')
    elif sort_by == 'price_high':
        results = quick_sort(results, 'price', reverse=True)
    elif sort_by == 'newest':
        results = merge_sort(results, 'year', reverse=True)
    elif sort_by == 'mileage_low':
        results = merge_sort(results, 'mileage')

    # --- DAA INTEGRATION: OPTIMIZED SEARCH (BINARY SEARCH) ---
    # If filtered results are sorted by price, we can use Binary Search for the price range
    if max_price:
        max_p = float(max_price)
        # Ensure data is sorted by price for Binary Search to work
        search_data = quick_sort(results, 'price')
        results = binary_search_price_range(search_data, 0, max_p)
        
        # Re-apply requested sorting if it wasn't price_low
        if sort_by == 'price_high':
            results = results[::-1] # Reverse the price_low sorted slice
        elif sort_by == 'newest':
            results = merge_sort(results, 'year', reverse=True)
        # (Technically price_low is already handled by binary_search output)
    
    return render_template('search.html', results=results)

@app.route('/car/<int:listing_id>')
def car_details(listing_id):
    conn = get_db_connection()
    car = conn.execute('''
        SELECT L.*, C.*, CS.*, U.name as seller_name, U.location, U.user_id as seller_id
        FROM Listings L 
        JOIN Cars C ON L.car_id = C.car_id 
        JOIN CarSpecifications CS ON C.car_id = CS.car_id
        JOIN Users U ON C.user_id = U.user_id
        WHERE L.listing_id = ?
    ''', (listing_id,)).fetchone()
    
    if not car:
        conn.close()
        flash('Car not found.', 'danger')
        return redirect(url_for('index'))
        
    # Get reviews for the seller
    reviews = conn.execute('SELECT * FROM Reviews WHERE seller_id = ?', (car['seller_id'],)).fetchall()
    conn.close()
    
    return render_template('car_details.html', car=car, reviews=reviews)

@app.route('/buy/<int:listing_id>', methods=['POST'])
def buy_car(listing_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
        
    conn = get_db_connection()
    listing = conn.execute('SELECT * FROM Listings WHERE listing_id = ?', (listing_id,)).fetchone()
    car = conn.execute('SELECT * FROM Cars WHERE car_id = ?', (listing['car_id'],)).fetchone()
    
    if listing and listing['status'] == 'available':
        # Insert transaction - The trigger will update Listing status to 'sold'
        conn.execute('''
            INSERT INTO Transactions (listing_id, buyer_id, seller_id, price) 
            VALUES (?, ?, ?, ?)
        ''', (listing_id, session['user_id'], car['user_id'], listing['price']))
        conn.commit()
        flash('Congratulations! You have purchased the car.', 'success')
    else:
        flash('Sorry, this car is no longer available.', 'warning')
        
    conn.close()
    return redirect(url_for('dashboard'))

@app.route('/message/<int:listing_id>', methods=['POST'])
def send_message(listing_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
        
    receiver_id = request.form['receiver_id']
    message_text = request.form['message']
    
    conn = get_db_connection()
    conn.execute('''
        INSERT INTO Messages (sender_id, receiver_id, listing_id, message) 
        VALUES (?, ?, ?, ?)
    ''', (session['user_id'], receiver_id, listing_id, message_text))
    conn.commit()
    conn.close()
    
    flash('Message sent to seller!', 'success')
    return redirect(url_for('car_details', listing_id=listing_id))

if __name__ == '__main__':
    app.run(debug=True, port=5000)
