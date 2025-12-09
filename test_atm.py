import unittest
import sqlite3
from database import Database
from atm_system import User

class TestATMSystem(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.db = Database(db_file='test_atm.db')  # Use a separate test DB
        cls.db.setup_database()
        # Clear tables for testing
        cursor = cls.db.connection.cursor()
        cursor.execute("DELETE FROM Transactions")
        cursor.execute("DELETE FROM Users")
        cls.db.connection.commit()
        cursor.close()

    def test_user_registration(self):
        user = User(self.db)
        self.assertTrue(user.register("testuser", "password123"))
        self.assertFalse(user.register("testuser", "password123"))  # Duplicate

    def test_user_login(self):
        user = User(self.db)
        user.register("testuser2", "password123")
        self.assertTrue(user.login("testuser2", "password123"))
        self.assertFalse(user.login("testuser2", "wrongpass"))

    def test_deposit_and_balance(self):
        user = User(self.db)
        user.register("testuser3", "password123")
        user.login("testuser3", "password123")
        user.deposit(100.0)
        user.check_balance()
        self.assertEqual(user.balance, 100.0)

    def test_withdraw_overdraft(self):
        user = User(self.db)
        user.register("testuser4", "password123")
        user.login("testuser4", "password123")
        user.deposit(50.0)
        user.withdraw(100.0)  # Should fail
        self.assertEqual(user.balance, 50.0)

    @classmethod
    def tearDownClass(cls):
        cls.db.close()
        # Optional: Remove test DB file after tests
        import os
        if os.path.exists('test_atm.db'):
            os.remove('test_atm.db')

if __name__ == "__main__":
    unittest.main()