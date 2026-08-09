import sqlite3
from scripts.load_owners_to_sqlite import CREATE_OWNER_TABLE

conn = sqlite3.connect(":memory:")
cursor = conn.cursor()

cursor.execute(CREATE_OWNER_TABLE)

cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
print(cursor.fetchall())