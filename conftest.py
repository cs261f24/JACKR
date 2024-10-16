# conftest.py
import pytest
import sqlite3
from test_db import connect_db, execute_sql_script

@pytest.fixture(scope="session", autouse=True)
def reset_db():
    """Reset the database before the test session."""
    conn = connect_db('db.sqlite3')
    cursor = conn.cursor()

    # Re-initialize the database by running schema.sql and populate_table.sql
    execute_sql_script(cursor, 'schema.sql')
    execute_sql_script(cursor, 'populate_table.sql')

    conn.commit()
    conn.close()

    yield
