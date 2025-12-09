import sqlite3
from database import Database
from datetime import datetime

class User:
    def __init__(self, db, user_id=None, username=None, balance=0.0):
        self.db = db
        self.user_id = user_id
        self.username = username
        self.balance = balance

    def register(self, username, password):
        """Register a new user."""
        try:
            hashed_password = self.db.hash_password(password)
            cursor = self.db.connection.cursor()
            query = "INSERT INTO Users (username, password, balance) VALUES (?, ?, ?)"
            cursor.execute(query, (username, hashed_password, 0.0))
            self.db.connection.commit()
            cursor.close()
            print("Registration successful!")
            return True
        except sqlite3.IntegrityError:
            print("Username already exists. Please choose another.")
            return False
        except Exception as e:
            print(f"Registration failed: {e}")
            return False

    def login(self, username, password):
        """Authenticate a user."""
        try:
            cursor = self.db.connection.cursor()
            query = "SELECT user_id, password, balance FROM Users WHERE username = ?"
            cursor.execute(query, (username,))
            result = cursor.fetchone()
            cursor.close()
            if result and self.db.verify_password(password, result[1]):
                self.user_id = result[0]
                self.username = username
                self.balance = result[2]
                print("Login successful!")
                return True
            else:
                print("Invalid username or password.")
                return False
        except Exception as e:
            print(f"Login failed: {e}")
            return False

    def check_balance(self):
        """Retrieve and display the current balance."""
        try:
            cursor = self.db.connection.cursor()
            query = "SELECT balance FROM Users WHERE user_id = ?"
            cursor.execute(query, (self.user_id,))
            result = cursor.fetchone()
            cursor.close()
            if result:
                self.balance = result[0]
                print(f"Your current balance is: ${self.balance:.2f}")
            else:
                print("Error retrieving balance.")
        except Exception as e:
            print(f"Error checking balance: {e}")

    def deposit(self, amount):
        """Deposit funds into the account."""
        if amount <= 0:
            print("Deposit amount must be positive.")
            return
        try:
            cursor = self.db.connection.cursor()
            # Update balance
            query1 = "UPDATE Users SET balance = balance + ? WHERE user_id = ?"
            cursor.execute(query1, (amount, self.user_id))
            # Record transaction
            query2 = "INSERT INTO Transactions (user_id, amount, transaction_type) VALUES (?, ?, 'deposit')"
            cursor.execute(query2, (self.user_id, amount))
            self.db.connection.commit()
            cursor.close()
            self.balance += amount
            print(f"Deposited ${amount:.2f}. New balance: ${self.balance:.2f}")
        except Exception as e:
            print(f"Deposit failed: {e}")

    def withdraw(self, amount):
        """Withdraw funds from the account, preventing overdrafts."""
        if amount <= 0:
            print("Withdrawal amount must be positive.")
            return
        if amount > self.balance:
            print("Insufficient funds. Cannot withdraw.")
            return
        try:
            cursor = self.db.connection.cursor()
            # Update balance
            query1 = "UPDATE Users SET balance = balance - ? WHERE user_id = ?"
            cursor.execute(query1, (amount, self.user_id))
            # Record transaction
            query2 = "INSERT INTO Transactions (user_id, amount, transaction_type) VALUES (?, ?, 'withdraw')"
            cursor.execute(query2, (self.user_id, amount))
            self.db.connection.commit()
            cursor.close()
            self.balance -= amount
            print(f"Withdrew ${amount:.2f}. New balance: ${self.balance:.2f}")
        except Exception as e:
            print(f"Withdrawal failed: {e}")

    def transaction_history(self):
        """Display the user's transaction history."""
        try:
            cursor = self.db.connection.cursor()
            query = "SELECT amount, transaction_type, timestamp FROM Transactions WHERE user_id = ? ORDER BY timestamp DESC"
            cursor.execute(query, (self.user_id,))
            results = cursor.fetchall()
            cursor.close()
            if results:
                print("Transaction History:")
                for amount, trans_type, timestamp in results:
                    print(f"{timestamp} - {trans_type.capitalize()}: ${amount:.2f}")
            else:
                print("No transactions found.")
        except Exception as e:
            print(f"Error retrieving history: {e}")

class ATMSystem:
    def __init__(self):
        self.db = Database()
        self.db.setup_database()
        self.current_user = None

    def run(self):
        """Main CLI loop."""
        while True:
            if not self.current_user:
                print("\n--- ATM Management System ---")
                print("1. Register")
                print("2. Login")
                print("3. Exit")
                choice = input("Choose an option: ").strip()
                if choice == '1':
                    self.register_user()
                elif choice == '2':
                    self.login_user()
                elif choice == '3':
                    print("Goodbye!")
                    break
                else:
                    print("Invalid choice. Try again.")
            else:
                print(f"\n--- Welcome, {self.current_user.username} ---")
                print("1. Check Balance")
                print("2. Deposit")
                print("3. Withdraw")
                print("4. Transaction History")
                print("5. Logout")
                choice = input("Choose an option: ").strip()
                if choice == '1':
                    self.current_user.check_balance()
                elif choice == '2':
                    self.deposit_funds()
                elif choice == '3':
                    self.withdraw_funds()
                elif choice == '4':
                    self.current_user.transaction_history()
                elif choice == '5':
                    self.logout()
                else:
                    print("Invalid choice. Try again.")

    def register_user(self):
        """Handle user registration."""
        username = input("Enter username: ").strip()
        password = input("Enter password: ").strip()
        if not username or not password:
            print("Username and password cannot be empty.")
            return
        user = User(self.db)
        user.register(username, password)

    def login_user(self):
        """Handle user login."""
        username = input("Enter username: ").strip()
        password = input("Enter password: ").strip()
        user = User(self.db)
        if user.login(username, password):
            self.current_user = user

    def deposit_funds(self):
        """Handle deposit."""
        try:
            amount = float(input("Enter deposit amount: ").strip())
            self.current_user.deposit(amount)
        except ValueError:
            print("Invalid amount. Please enter a number.")

    def withdraw_funds(self):
        """Handle withdrawal."""
        try:
            amount = float(input("Enter withdrawal amount: ").strip())
            self.current_user.withdraw(amount)
        except ValueError:
            print("Invalid amount. Please enter a number.")

    def logout(self):
        """Logout the current user."""
        print("Logged out successfully.")
        self.current_user = None

if __name__ == "__main__":
    import sqlite3  # Ensure it's imported for exception handling
    atm = ATMSystem()
    try:
        atm.run()
    finally:
        atm.db.close()