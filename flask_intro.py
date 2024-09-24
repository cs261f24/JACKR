"""
This Flask app serves a very simple web page that shows a table of items
(names and quantities) that are stored in a SQLite database. When things get
more complex they should be broken up into multiple Python files.
"""


import os
import sqlite3
from flask import Flask, g, render_template
from flask import request, redirect, url_for, flash, session # Used for login functionality
from werkzeug.security import generate_password_hash
import click




# There are better ways to do this, see the Flask tutorial
app = Flask(__name__)




app.secret_key = 'my-super-secret-key'


# Name of the SQLite database file that will be created
DB_PATH = 'db.sqlite3'


# We will delete out this database once the SQL files are ready
dbUser_PW = {'Jack': 'Password123'}


def get_db():
    """
    Returns a database connection. If a connection has already been created,
    the existing connection is used, otherwise it creates a new connection.
    """


    # The Flask g object can be used to manage global application-level
    # data. Here we use it to store a database connection object so that we
    # don't have to make a new one every time we want to use the DB during a
    # request
    if 'sqlite_db' not in g:
        g.sqlite_db = sqlite3.connect(
            DB_PATH,
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        # Make result rows behave like dictionaries
        g.sqlite_db.row_factory = sqlite3.Row


    return g.sqlite_db






def close_db(e=None):
    """
    Close the database connection if it was opened.
    """


    db = g.pop('sqlite_db', None)


    if db is not None:
        db.close()








def init_db():
    """
    Run the schema.sql and populate_table.sql SQL scripts to drop and add the
    item table and populate it.
    """


    db = get_db()


    with app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


    with app.open_resource('populate_table.sql') as f:
        db.executescript(f.read().decode('utf8'))




@click.command('init-db')
def init_db_command():
    """
    Create the custom command "init-db" to initialize the database.
    """


    init_db()
    click.echo('Initialized the database')




# Close the DB when the app shuts down and register the init-db command
# There are better ways to do this, see the Flask tutorial
app.teardown_appcontext(close_db)
app.cli.add_command(init_db_command)




def get_items():
    """
    Returns a list of items sorted by name.
    """


    conn = get_db()
    cur = conn.cursor()


    query = '''
SELECT name, quantity
FROM item
ORDER BY name'''


    cur.execute(query)


    # fetchall() gets all the rows as a list
    return cur.fetchall()




def get_events():
    """
    Returns a list of upcoming events.
    """
    conn = get_db()
    cur = conn.cursor()


    query = '''
    SELECT name, date, location, description
    FROM events
    ORDER BY date'''


    cur.execute(query)
    return cur.fetchall()




@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']


        # Here, you'd fetch the user from the database and validate the password
        conn = get_db()
        cur = conn.cursor()


        query = 'SELECT * FROM faculty WHERE username = ?'
        cur.execute(query, (username,))
        user = cur.fetchone()


        if username not in dbUser_PW:
            return render_template('items.html', info='Invalid User')
        else:
            if dbUser_PW[username] != password:
                return render_template('items.html', info="Invalid Password")
            else:
                return render_template("login.html", name = username)
           
@app.route('/')
def items():
    """
    Serves a page which shows the items sorted by name. See the file
    templates/items.html for the template. The list returned from get_items()
    is passed as the positional parameter items, which is then accessible
    within the template.
    """


    return render_template('items.html', items=get_items())


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))