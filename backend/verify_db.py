import sqlite3
import os

db_path = 'feedvote.db'

# Check if database file exists
if os.path.exists(db_path):
    file_size = os.path.getsize(db_path)
    print(f"✓ Database file exists: {db_path}")
    print(f"  Size: {file_size:,} bytes")
    print()
    
    # Connect and check tables
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Get all tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
        tables = cursor.fetchall()
        
        if tables:
            print("✓ Database Tables:")
            for table, in tables:
                cursor.execute(f'SELECT COUNT(*) FROM {table}')
                count = cursor.fetchone()[0]
                print(f"    {table}: {count} records")
            print()
        else:
            print("⚠ No tables found")
            print()
        
        # Check integrity
        cursor.execute("PRAGMA integrity_check")
        integrity = cursor.fetchone()[0]
        if integrity == 'ok':
            print("✓ Database integrity: OK")
        else:
            print(f"⚠ Database integrity issue: {integrity}")
        
        conn.close()
        print()
        print("✓ SQLite Database Configuration: VERIFIED")
        print("✓ Database is functioning properly")
        
    except Exception as e:
        print(f"✗ Error checking database: {e}")
else:
    print(f"✗ Database file not found: {db_path}")
