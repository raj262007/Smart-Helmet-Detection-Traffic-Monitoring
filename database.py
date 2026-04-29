# database.py

import sqlite3
import os

# Database file path
DB_PATH = "data/violations.db"

def create_connection():
    # Create data folder if not exists
    os.makedirs("data", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    return conn

def create_table():
    # Create violations table if not exists
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS violations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            time TEXT,
            total_vehicles INTEGER,
            safe_count INTEGER,
            violation_count INTEGER,
            image_path TEXT
        )
    ''')

    conn.commit()
    conn.close()
    print("Database ready!")