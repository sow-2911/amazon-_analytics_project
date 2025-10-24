# diagnostic.py
import sqlite3
import os
import pandas as pd

print("🔍 Checking Amazon Analytics Database...")
print("=" * 50)

# Check if database file exists
db_path = 'amazon_india_analytics.db'
if os.path.exists(db_path):
    print(f"✅ Database file found: {db_path}")
    file_size = os.path.getsize(db_path)
    print(f"📁 File size: {file_size} bytes")
else:
    print(f"❌ Database file NOT found: {db_path}")
    print("Please run: python data_cleaning_pipeline.py")
    exit()

# Try to connect and check contents
try:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # List all tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    
    if tables:
        print(f"📊 Found {len(tables)} table(s):")
        for table in tables:
            table_name = table[0]
            print(f"  └─ {table_name}")
            
            # Count rows
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            count = cursor.fetchone()[0]
            print(f"     Rows: {count}")
            
            # Show column names
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = [col[1] for col in cursor.fetchall()]
            print(f"     Columns: {columns}")
            print()
    else:
        print("❌ No tables found in database!")
        print("Run: python data_cleaning_pipeline.py")
    
    conn.close()
    
except Exception as e:
    print(f"❌ Error accessing database: {e}")

print("=" * 50)
input("Press Enter to close...")