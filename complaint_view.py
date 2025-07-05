import sqlite3

# Connect to the database
conn = sqlite3.connect("complaints.db")
cursor = conn.cursor()

# Show all tables
print("📋 Tables in the database:")
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
print(cursor.fetchall())

# Show column names of the 'complaint' table
print("\n🧱 Columns in 'complaint' table:")
cursor.execute("PRAGMA table_info(complaint);")
columns = cursor.fetchall()
for col in columns:
    print(f"- {col[1]} ({col[2]})")

# Show all rows
print("\n📦 Complaint Records:")
cursor.execute("SELECT * FROM complaint;")
rows = cursor.fetchall()

for row in rows:
    print(row)

conn.close()
