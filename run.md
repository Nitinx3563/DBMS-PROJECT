# Step-by-Step Guide to Run the Project 🚀

Follow these commands in order to get the **DriveDeal Marketplace** up and running.

### 1. Navigate to the Project Folder
```bash
cd "/home/sspl/nitin's project"
```

### 2. Create the Virtual Environment
```bash
python3 -m venv venv
```

### 3. Activate the Virtual Environment
**On Linux/macOS:**
```bash
source venv/bin/activate
```
**On Windows:**
```bash
venv\Scripts\activate
```

### 4. Install Required Packages
```bash
pip install -r requirements.txt
```

### 5. Initialize the Database
This script will create the `cars.db` file and set up all Tables, Triggers, and Views.
```bash
python3 scripts/init_db.py
```

### 6. Run the Application
```bash
python3 backend/app.py
```
---

### 🌐 Accessing the App
Once the server starts, open your browser and go to:
**[http://127.0.0.1:5000](http://127.0.0.1:5000)**

### 🧪 Verification (Optional)
To verify that the database triggers and views are working correctly, run:
```bash
python3 scripts/verify_sql.py
```
