import sqlite3


# Connect to the SQLite database
def connect_db(db_name):
    return sqlite3.connect(db_name)


# Function to execute SQL script
def execute_sql_script(cursor, sql_file):
    with open(sql_file, 'r') as file: #opens the file and reads the contents of the sql file
        sql_script = file.read()
    cursor.executescript(sql_script) # This runs the sql file/script


# Function to check data in a table
def check_table_data(cursor, table_name):
    cursor.execute(f"SELECT * FROM {table_name};") #fetches all the data from the tables
    rows = cursor.fetchall()
    print(f"Data in {table_name}:") # prints the data in the table
    for row in rows:
        print(row)


def main():
    db_name = 'db.sqlite3'  # name of database
    schema_file = 'schema.sql' #name of schema sql file
    populate_file = 'populate_table.sql' #name of file


    # Connection to the Database
    conn = connect_db(db_name)
    cursor = conn.cursor() # creates a cursor object for executing commands


    # Executes schema and populate tables
    # Also prints the tables with the information
    print("Creating tables...")
    execute_sql_script(cursor, schema_file)


    print("Populating tables...")
    execute_sql_script(cursor, populate_file)


    # Checks the data in each table
    tables = ['users', 'events', 'attendance'] #These are the names of the tables in schema.sql
    # Iterates through the tables and prints the information
    for table in tables:
        check_table_data(cursor, table)


    # Commit any changes and closes the connection
    conn.commit()
    conn.close()


if __name__ == "__main__":
    main()




