# backend/db.py
# backend/db.py
import sqlite3
import os
from datetime import datetime

# Define database path relative to this file
DB_PATH = os.path.join(os.path.dirname(__file__), 'scan_history.db')

# Initialize database: create table if not exists
def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS scans (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                url TEXT NOT NULL,
                category TEXT NOT NULL,
                reason TEXT NOT NULL,
                timestamp TEXT NOT NULL
            )
        ''')
        conn.commit()

# Save a scan record to the database
def save_scan(url, category, reason):
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        c.execute('''
            INSERT INTO scans (url, category, reason, timestamp)
            VALUES (?, ?, ?, ?)
        ''', (url, category, reason, timestamp))
        conn.commit()
        print(f"✅ Saved scan: {url}, {category}, at {timestamp}")

# Fetch scan history, including ID
def get_scan_history(limit=20):
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute('''
            SELECT id, url, category, reason, timestamp
            FROM scans
            ORDER BY id DESC
            LIMIT ?
        ''', (limit,))
        rows = c.fetchall()
        return rows  # Will be processed by app.py
