import sqlite3
import os

db_path = 'backend/cars.db'

def init_db():
    if os.path.exists(db_path):
        os.remove(db_path)
    
    conn = sqlite3.connect(db_path)
    
    # Read and execute schema.sql
    with open('database/schema.sql', 'r') as f:
        schema = f.read()
        conn.executescript(schema)
        
    # Read and execute triggers_views_indexes.sql
    with open('database/triggers_views_indexes.sql', 'r') as f:
        tvi = f.read()
        conn.executescript(tvi)
        
    print(f"Database initialized at {db_path}")
    conn.close()

if __name__ == "__main__":
    init_db()
