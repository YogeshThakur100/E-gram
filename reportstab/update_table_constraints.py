import sqlite3
import os

def update_table_constraints():
    # Path to your database
    db_path = r"C:\Users\Guest User\Databasessqllite\grampanchayat.db"
    
    if not os.path.exists(db_path):
        print(f"Database not found at: {db_path}")
        return
    
    try:
        # Connect to the database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check if unique constraints already exist
        cursor.execute("PRAGMA index_list(outward_entries)")
        indexes = cursor.fetchall()
        
        # Check if unique constraints exist
        has_srno_unique = any('sqlite_autoindex_outward_entries_1' in str(index) for index in indexes)
        has_jakramank_unique = any('sqlite_autoindex_outward_entries_2' in str(index) for index in indexes)
        
        if has_srno_unique and has_jakramank_unique:
            print("Unique constraints already exist!")
            return
        
        # Create unique constraints
        print("Adding unique constraints...")
        
        # Add unique constraint for srNo
        try:
            cursor.execute("CREATE UNIQUE INDEX idx_outward_entries_srno ON outward_entries(srNo)")
            print("✓ Added unique constraint for srNo")
        except sqlite3.IntegrityError as e:
            print(f"⚠ Warning: Could not add unique constraint for srNo: {e}")
        
        # Add unique constraint for jaKramank
        try:
            cursor.execute("CREATE UNIQUE INDEX idx_outward_entries_jakramank ON outward_entries(jaKramank)")
            print("✓ Added unique constraint for jaKramank")
        except sqlite3.IntegrityError as e:
            print(f"⚠ Warning: Could not add unique constraint for jaKramank: {e}")
        
        # Commit changes
        conn.commit()
        print("✓ Database updated successfully!")
        
    except Exception as e:
        print(f"Error updating database: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    update_table_constraints() 