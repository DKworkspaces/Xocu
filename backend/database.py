import sqlite3

DATABASE_NAME = "form_data.db"

def init_db():
    """Create the admin data table and seed it with 3 entries if empty."""
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS admins (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            ) STRICT;
        """)
        
        # Verify if seeding is required to avoid duplication constraints
        cursor.execute("SELECT COUNT(*) FROM admins")
        if cursor.fetchone()[0] == 0:
            admin_users = [
                ('admin_one', 'pass123'),
                ('admin_two', 'secure456'),
                ('admin_three', 'super789')
            ]
            cursor.executemany(
                "INSERT INTO admins (username, password) VALUES (?, ?)", 
                admin_users
            )
            print("Successfully initialized database with 3 administrative profiles.")
            
        conn.commit()

def verify_admin(username, password):
    """Authenticate data credentials using standard SQLite queries."""
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM admins WHERE username = ? AND password = ?", 
            (username, password)
        )
        return cursor.fetchone() is not None

def fetch_all_users():
    """Extract rows to display cleanly in your multi-page grid layout."""
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, username FROM admins")
        # Returns raw list arrays back to the application route
        return [{"id": row[0], "username": row[1]} for row in cursor.fetchall()]
