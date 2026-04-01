import sqlite3

conn = sqlite3.connect("bank.db")
cursor = conn.cursor()

# Create table
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    account_number TEXT UNIQUE,
    balance REAL
)
""")

conn.commit()


# ---------------- FUNCTIONS ---------------- #

def create_account():
    name = input("Enter your name: ")
    acc_no = input("Enter account number: ")
    balance = float(input("Enter initial balance: "))

    try:
        cursor.execute("INSERT INTO users (name, account_number, balance) VALUES (?, ?, ?)",
                       (name, acc_no, balance))
        conn.commit()
        print("Account created successfully!")
    except:
        print("Account number already exists!")


def login():
    acc_no = input("Enter account number: ")

    cursor.execute("SELECT * FROM users WHERE account_number = ?", (acc_no,))
    user = cursor.fetchone()

    if user:
        print("Login successful! Welcome", user[1])
        return acc_no
    else:
        print("Invalid account number")
        return None


def deposit(acc_no):
    amount = float(input("Enter amount to deposit: "))

    cursor.execute("UPDATE users SET balance = balance + ? WHERE account_number = ?",
                   (amount, acc_no))
    conn.commit()

    print("Amount deposited successfully!")


def withdraw(acc_no):
    amount = float(input("Enter amount to withdraw: "))

    cursor.execute("SELECT balance FROM users WHERE account_number = ?", (acc_no,))
    balance = cursor.fetchone()[0]

    if balance >= amount:
        cursor.execute("UPDATE users SET balance = balance - ? WHERE account_number = ?",
                       (amount, acc_no))
        conn.commit()
        print("Withdrawal successful!")
    else:
        print("Insufficient balance!")


def check_balance(acc_no):
    cursor.execute("SELECT balance FROM users WHERE account_number = ?", (acc_no,))
    balance = cursor.fetchone()[0]

    print("Your balance is:", balance)


# ---------------- MAIN PROGRAM ---------------- #

while True:
    print("\n----- BANK SYSTEM -----")
    print("1. Create Account")
    print("2. Login")
    print("3. Exit")

    choice = input("Enter choice: ")

    if choice == "1":
        create_account()

    elif choice == "2":
        user = login()

        if user:
            while True:
                print("\n--- MENU ---")
                print("1. Deposit")
                print("2. Withdraw")
                print("3. Check Balance")
                print("4. Logout")

                ch = input("Enter choice: ")

                if ch == "1":
                    deposit(user)
                elif ch == "2":
                    withdraw(user)
                elif ch == "3":
                    check_balance(user)
                elif ch == "4":
                    break
                else:
                    print("Invalid choice")

    elif choice == "3":
        print("Thank you!")
        break

    else:
        print("Invalid choice")
