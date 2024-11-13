import sqlite3
import hashlib
import os

# Connect to the SQLite database
def connect_db(db_name):
    try:
        return sqlite3.connect(db_name)
    except sqlite3.Error as e:
        print(f"Error connecting to database: {e}")
        return None

# List all tables in the database
def list_tables(cursor):
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print("Tables in the database:")
    for table in tables:
        print(table[0])

# Execute an SQL script
def execute_sql_script(cursor, sql_file):
    try:
        with open(sql_file, 'r') as file:
            sql_script = file.read()
        cursor.executescript(sql_script)
        print(f"Successfully executed {sql_file}.")
    except Exception as e:
        print(f"Error executing {sql_file}: {e}")

# Check data in a specific table
def check_table_data(cursor, table_name):
    try:
        cursor.execute(f"SELECT * FROM {table_name};")
        rows = cursor.fetchall()
        print(f"\nData in {table_name}:")
        for row in rows:
            print(row)
    except sqlite3.Error as e:
        print(f"Error reading data from {table_name}: {e}")

# Hash a password with a salt
def hash_password(password):
    salt = os.urandom(32)
    hashed_password = hashlib.sha256(password.encode() + salt).hexdigest()
    return salt.hex() + ':' + hashed_password

# Verify the hashed password
def verify_password(stored_password, input_password):
    salt, hashed_password = stored_password.split(':')
    salt = bytes.fromhex(salt)
    return hashlib.sha256(input_password.encode() + salt).hexdigest() == hashed_password

# Create a new user
def create_user(firstName, lastName, password, email, role):
    conn = connect_db('db.sqlite3')
    if conn is None:
        return False

    cur = conn.cursor()
    hashed_password = hash_password(password)

    

# Check if a user can log in
def check_user_login(firstName, password):
    conn = connect_db('db.sqlite3')
    if conn is None:
        return False

    cur = conn.cursor()
    cur.execute("SELECT password FROM users WHERE firstName = ? AND lastName = ?", (firstName, lastName,))
    user = cur.fetchone()
    conn.close()

    if user and verify_password(user[0], password):
        print(f"Login successful for {firstName, lastName}.")
        return True
    else:
        print(f"Login failed for {firstName, lastName}.")
        return False

def main():
    db_name = 'db.sqlite3'
    schema_file = 'schema.sql'
    populate_file = 'populate_table.sql'

    conn = connect_db(db_name)
    if conn is None:
        return

    cursor = conn.cursor()

    print("Creating tables...")
    execute_sql_script(cursor, schema_file)

    print("Populating tables...")
    execute_sql_script(cursor, populate_file)

    tables = ['users', 'events', 'attendance', 'other_departments']
    for table in tables:
        check_table_data(cursor, table)

    print("\nTesting user creation:")
    create_user('newuser', 'newpassword', 'newuser@example.com', 'student')

    print("\nTesting user login:")
    check_user_login('newuser', 'newpassword')

    conn.commit()
    conn.close()

if __name__ == "__main__":
    main()