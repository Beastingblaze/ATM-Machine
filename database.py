import sqlite3
import bcrypt

class Database:
    def __init__(self, db_file='atm_management.db'):
        self.db_file = db_file
        self.connection = None

    def connect(self):
        """Establish a connection to the SQLite database."""
        try:
            self.connection = sqlite3.connect(self.db_file)
            print("Connected to SQLite database.")
        except Exception as e:
            print(f"Error connecting to database: {e}")
            raise

    def close(self):
        """Close the database connection."""
        if self.connection:
            self.connection.close()
            print("Database connection closed.")

    def setup_database(self):
        """Create the database and tables if they don't exist."""
        try:
            self.connect()
            cursor = self.connection.cursor()

            # Create Users table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS Users (
                    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL,
                    balance REAL DEFAULT 0.0
                )
            """)

            # Create Transactions table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS Transactions (
                    transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    amount REAL NOT NULL,
                    transaction_type TEXT CHECK(transaction_type IN ('deposit', 'withdraw')) NOT NULL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE
                )
            """)

            # Add indexes for performance
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_username ON Users(username)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_user_id_timestamp ON Transactions(user_id, timestamp)")

            self.connection.commit()
            cursor.close()
            print("Database and tables set up successfully.")
        except Exception as e:
            print(f"Error setting up database: {e}")
            raise

    def hash_password(self, password):
        """Hash a password using bcrypt."""
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def verify_password(self, password, hashed):
        """Verify a password against its hash."""
        return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))