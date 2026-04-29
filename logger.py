# logger.py

import csv
import os
import sqlite3
from datetime import datetime
from database import create_connection

# CSV file path
CSV_PATH = "data/violations.csv"

def setup_csv():
    # Create CSV file with headers if not exists
    os.makedirs("data", exist_ok=True)
    if not os.path.exists(CSV_PATH):
        with open(CSV_PATH, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([
                'ID', 'Date', 'Time',
                'Total_Vehicles', 'Safe_Count',
                'Violation_Count', 'Image_Path'
            ])
        print("CSV file created!")

def log_violation(total_vehicles, safe_count, violation_count, image_path=""):
    # Get current date and time
    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%H:%M:%S")

    # Save to CSV file
    with open(CSV_PATH, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([
            '', date_str, time_str,
            total_vehicles, safe_count,
            violation_count, image_path
        ])

    # Save to database
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO violations
        (date, time, total_vehicles, safe_count, violation_count, image_path)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (date_str, time_str, total_vehicles, safe_count, violation_count, image_path))
    conn.commit()
    conn.close()

    print(f"Logged — Total: {total_vehicles} | Safe: {safe_count} | Violations: {violation_count}")