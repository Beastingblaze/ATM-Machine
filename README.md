---

# 🏧 ATM Management System (Python + SQLite)

A fully functional **ATM Management System** built using **Python**, **SQLite**, and **bcrypt** for secure password management.
This project supports **user registration, login, balance inquiry, deposits, withdrawals, and transaction history**, along with a full **unit test suite**.

---

## 📌 Features

### 👤 User Account Operations

* Create an account with secure password hashing (bcrypt)

* User login with password verification


### 💰 Banking Transactions

* Check balance
* Deposit money
* Withdraw money (with overdraft protection)
* View detailed transaction history


### 🗄 Database

* SQLite database with:

  * Users table
  * Transactions table
  * Indexes for fast lookup


### ✅ Unit Tests

* Registration
* Login
* Deposit
* Withdrawal & overdraft prevention


---

## 🛠️ Tech Stack

* **Python 3.8+**
* **SQLite3**
* **bcrypt** for password hashing
  Requirements file:


---

## 📂 Project Structure

```
├── atm_system.py
├── database.py
├── test_atm.py
├── requirements.txt
└── README.md
```

---

## 🚀 How to Run the Project

### 1️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 2️⃣ Run the ATM System

```bash
python atm_system.py
```

### 3️⃣ Run Unit Tests

```bash
python -m unittest test_atm.py
```

---

## 🧩 How It Works

### 🔑 Authentication

* Passwords are hashed using `bcrypt` before storing
* Login compares input password with stored hash


### 💵 Transactions

* All deposits/withdrawals update the balance safely
* Each transaction is logged with timestamp


### 🗃 Database Schema

* **Users Table:** Stores username, hashed password, and balance
* **Transactions Table:** Stores deposits & withdrawals with timestamps


---

## 🧪 Testing Coverage

The `test_atm.py` covers:

| Test         | Description                   |
| ------------ | ----------------------------- |
| Registration | Valid & duplicate usernames   |
| Login        | Correct & incorrect passwords |
| Deposit      | Update balance accurately     |
| Withdraw     | Prevent overdrafts            |
|              |                               |

Run tests:

```bash
python -m unittest test_atm.py
```

---

## 📜 License

This project is open-source and free to use.

---
