import sqlite3
import os

def recreate_table():
    # Path to your database
    db_path = r"C:\Users\Guest User\Databasessqllite\grampanchayat.db"
    
    if not os.path.exists(db_path):
        print(f"Database not found at: {db_path}")
        return
    
    try:
        # Connect to the database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print("Recreating outward_entries table with srNo as primary key...")
        
        # Drop the existing table
        cursor.execute("DROP TABLE IF EXISTS outward_entries")
        print("✓ Dropped existing table")
        
        # Create new table with srNo as primary key
        create_table_sql = """
        CREATE TABLE outward_entries (
            srNo VARCHAR(50) PRIMARY KEY,
            jaKramank VARCHAR(50) NOT NULL UNIQUE,
            reportType VARCHAR(100) NOT NULL,
            timeNDate DATETIME NOT NULL,
            name VARCHAR(200) NOT NULL,
            village_id INTEGER DEFAULT 1,
            gram_panchayat_id INTEGER DEFAULT 1,
            district_id INTEGER DEFAULT 1,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        );
        """
        
        cursor.execute(create_table_sql)
        print("✓ Created new table with srNo as primary key")
        
        # Commit changes
        conn.commit()
        print("✓ Database updated successfully!")
        
        # Show the new table structure
        cursor.execute("PRAGMA table_info(outward_entries)")
        columns = cursor.fetchall()
        print("\nNew table structure:")
        for col in columns:
            print(f"  {col[1]} ({col[2]}) - Primary: {col[5]}, Not Null: {col[3]}")
        
    except Exception as e:
        print(f"Error recreating table: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    recreate_table() 