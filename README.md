# Used Car Price Prediction & Marketplace 🚗💨

A complete college-level DBMS project built with **Flask** and **SQLite**. This application simulates a used car marketplace where users can buy and sell cars, complete with AI-powered price predictions based on historical SQL data.

## 🌟 Key Features
- **User Authentication**: Secure login/register system for buyers and sellers.
- **Car Listings**: Sellers can post detailed car specifications and manage their listings.
- **Marketplace Search**: Advanced filtering by Brand, Price, and Fuel Type.
- **Price Prediction**: Real-time price estimation using SQL aggregate logic.
- **Messaging System**: Built-in buyer-seller inquiry platform.
- **Transaction Management**: Automated 'Sold' status updates via SQL triggers.
- **Premium UI**: Modern dark-mode design with Glassmorphism.

## 🗄️ Database Design (DBMS Highlights)
- **7 Related Tables**: Users, Cars, CarSpecifications, Listings, Reviews, Messages, Transactions.
- **Trigger**: Automatic status update from 'available' to 'sold' upon transaction.
- **View**: `AvailableCars` for clean, optimized active listing queries.
- **Indices**: Performance-optimized indexing on frequently searched columns.

## 🚀 Installation & Setup

### 1. Clone the repository and navigate to the project root:
```bash
# Assuming you have the code in 'Used-Car-Marketplace'
cd nitin's project
```

### 2. Setup Virtual Environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Linux/macOS
# or
venv\Scripts\activate     # On Windows
```

### 3. Install dependencies:
```bash
pip install -r requirements.txt
```

### 4. Initialize the database:
```bash
python3 scripts/init_db.py
```

### 5. Run the application:
```bash
python3 backend/app.py
```
Open your browser and visit: `http://127.0.0.1:5000`

## 📁 Project Structure
- `database/`: SQL schema, triggers, and views.
- `backend/`: Flask application logic and database file.
- `backend/frontend/`: HTML templates and CSS styling.
- `scripts/`: Database initialization and verification scripts.

## 📝 License
This project is for academic and educational purposes.
