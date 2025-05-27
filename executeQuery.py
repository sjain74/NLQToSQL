import sqlite3
import globals

def execute_query(query, params=None):
    db_path = globals.SQLITE3_DB  # Path to your SQLite DB file
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        
        results = cursor.fetchall()
        return results
    except sqlite3.Error as e:
        print("Database error:", e)
        return []
    finally:
        conn.close()