import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "django_app", "db.sqlite3")

conn = sqlite3.connect(DB_PATH, check_same_thread=False)
cursor = conn.cursor()


cursor.execute("""
CREATE TABLE IF NOT EXISTS otp_store (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    otp TEXT,
    expires_at TEXT
)
""")
conn.commit()