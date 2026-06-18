import sqlite3
from pathlib import Path

Path("db").mkdir(exist_ok=True)

conn = sqlite3.connect("db/nifty100.db")
print("Database created successfully!")

conn.close()