"""
This Flask app serves a very simple web page that shows a table of items
(names and quantities) that are stored in a SQLite database. When things get
more complex they should be broken up into multiple Python files.
"""


import os
import sqlite3
import re
from flask import Flask, g, render_template
from flask import request, redirect, url_for, flash, session # Used for login functionality
import click
from test_db import connect_db # importing the database data insertion into flask
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime



# There are better ways to do this, see the Flask tutorial
app = Flask(__name__)



app.secret_key = 'my-super-secret-key'



# Name of the SQLite database file that will be created
DB_PATH = 'db.sqlite3'




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



def get_logininfo():
    """
    Fetches login information from the users table.
    """

    conn = get_db()
    cur = conn.cursor()

    query = '''
    SELECT firstName, lastName, password
    FROM users
    ORDER BY firstName, lastName
    '''

    cur.execute(query)
    return cur.fetchall()

@app.route('/add_event', methods=['GET', 'POST'])
def add_events():
    """
    Handles adding a new event to the events table.
    """
    if request.method == 'POST':
        # Retrieve form data
        event_name = request.form['event_name']
        event_date = request.form['event_date']
        event_location = request.form['event_location']
        event_description = request.form['event_description']
        event_time = request.form['event_time']

        try:
            event_time_obj = datetime.strptime(event_time, "%H:%M")
            event_time_12hr = event_time_obj.strftime("%I:%M %p")
        except ValueError:
            event_time_12hr = event_time

        conn = get_db()  # Get database connection
        cur = conn.cursor()

        # Fetch the suggestions from the database
        suggestion = []
        cur.execute("SELECT eventname, eventdescription FROM suggestion")
        suggestion = cur.fetchall()

        # Insert the new event into the database
        try:
            cur.execute(
                'INSERT INTO events (name, date, location, description, time) VALUES (?, ?, ?, ?, ?)',
                (event_name, event_date, event_location, event_description, event_time_12hr)
            )
            conn.commit()  # Save the changes
            info_message = "Event added successfully!"
        except sqlite3.IntegrityError:
            info_message = "This event already exists."
        finally:
            conn.close()  # Close the connection

        # Redirect to the FacultyEventPage with a success message
        return render_template('FacultyEventPage.html', info=info_message, suggestion=suggestion, event_time=event_time_12hr)

    # Render the FacultyEventPage if it's a GET request
    return render_template('FacultyEventPage.html', suggestion=suggestion)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = get_db()
        cur = conn.cursor()


        # Fetch the events from the database  
        cur.execute("SELECT name, date, description, location, time FROM events ORDER BY date")
        event = cur.fetchall()

        # Fetch the user from the database
        userquery = 'SELECT * FROM users WHERE email = ?'
        cur.execute(userquery, (email,))
        user = cur.fetchone()

        # Fetch the suggestions from the database
        suggestion = []
        cur.execute("SELECT eventname, eventdescription FROM suggestion")
        suggestion = cur.fetchall()

        conn.close()

        # Check if the user exists and the password matches
        if user and check_password_hash(user['password'], password):
            session['email'] = email
            firstName = user['firstName']

            # Check the user's role
            role = user['role']
            if role == 'admin':
                return render_template("FacultyEventPage.html", info = "Hello " + firstName + "!", suggestion=suggestion)  # Redirect to admin view
            else:
                return render_template("StudentView.html", info = "Hello " + firstName + "!")  # Redirect to student view
        else:
            flash('Invalid email or password', 'error')
            return render_template('loginPage.html')
    return render_template('loginPage.html')

           
@app.route('/')
def items():
    """
    Serves a page which shows the items sorted by name. See the file
    templates/items.html for the template. The list returned from get_items()
    is passed as the positional parameter items, which is then accessible
    within the template.
    """


    return render_template('StartPage.html', items=get_logininfo())

@app.route('/mark_attendance/<int:event_id>', methods=['POST'])
def mark_attendance(event_id):
    if 'email' not in session:
        # Redirect if not logged in
        return redirect(url_for('login'))
    
    student_email = session['email']  # Assuming the student's email is stored in session
    
    # Get the student's full name from the users table
    db = get_db()
    student = db.execute("""
        SELECT firstName, lastName FROM users WHERE email = ?
    """, (student_email,)).fetchone()
    
    if student:
        student_name = f"{student['firstName']} {student['lastName']}"
    else:
        student_name = "Unknown"  # In case the student is not found (shouldn't happen if they are logged in)
    
    # Insert attendance if not already present
    db.execute("""
        INSERT OR IGNORE INTO attendance (email, name, event_id, events_attended)
        VALUES (?, ?, ?, 1)
    """, (student_email, student_name, event_id))
    
    # Alternatively, update if already attended
    db.execute("""
        UPDATE attendance
        SET events_attended = 1
        WHERE email = ? AND event_id = ?
    """, (student_email, event_id))
    
    db.commit()

    # Redirect to the student's dashboard or back to the event view
    return render_template('StudentView.html', info1="Your attendance has been recorded!")  # Redirect back to the student dashboard


@app.route('/studentview4faculty')
def student_view_4faculty():
    # Retrieve the selected date from the query parameter
    selected_date = request.args.get('date')
    
    # Connect to the database and query events for the selected date
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()
    
    events = []
    if selected_date:
        cursor.execute("SELECT name, date, description, location, time FROM events WHERE date = ?", (selected_date,))
        events = cursor.fetchall()
    
    conn.close()
    
    # Render `studentviewforfaculty.html`, passing the events for the selected date
    return render_template('StudentViewForFaculty.html', events=events)

@app.route('/studentview')
def student_view():
    # Retrieve the selected date from the query parameter
    selected_date = request.args.get('date')
    
    # Connect to the database and query events for the selected date
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()
    
    events = []
    if selected_date:
    # Query to get event details along with attendance information
        cursor.execute("""
        SELECT 
            e.id, 
            e.name, 
            e.date, 
            e.description, 
            e.location, 
            e.time,
            COALESCE(a.events_attended, 0) AS events_attended
        FROM events e
        LEFT JOIN attendance a ON e.id = a.event_id AND a.email = ?
        WHERE e.date = ?
        """, (session['email'], selected_date))
    
        events = cursor.fetchall()

    conn.close()
    
    # Render `studentview.html`, passing the events for the selected date
    return render_template('StudentView.html', events=events)


# Sign-up route to register new users
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Fetching form data
        firstName = request.form['firstName']
        lastName = request.form['lastName']
        password = request.form['password']
        email = request.form['email']
        role = request.form['role']


        hashed_password = generate_password_hash(password)


        # Connect to the database
        conn = connect_db('db.sqlite3')
        cursor = conn.cursor()

        try:
            # Insert the new user data into the 'users' table
            cursor.execute(
                'INSERT INTO users (firstName, lastName, password, email, role) VALUES (?, ?, ?, ?, ?)',
                (firstName, lastName, hashed_password, email, role)
            )
            conn.commit()  # Save the changes to the database
        except sqlite3.IntegrityError:
            return render_template('signupPage.html', info = "This email already exists.")
        finally:
            # Close the database connection
            conn.close()

        # Redirect the user to the start page after successful sign-up
        return render_template('StartPage.html', info = "Sign-up successful!")
    # Render the sign-up form if the request method is GET
    return render_template('signupPage.html')


@app.route("/faculty")
def back_to_faculty():
    conn = get_db()
    cur = conn.cursor()
    suggestion = []
    cur.execute("SELECT eventname, eventdescription FROM suggestion")
    suggestion = cur.fetchall()

    conn.close()
    return render_template("FacultyEventPage.html", suggestion=suggestion)

@app.route("/student_dashboard", methods=['GET', 'POST'])
def back_to_student():
    conn = get_db()  # Get database connection
    cur = conn.cursor()

    # Fetch events for the dashboard
    cur.execute("SELECT name, date, description, location FROM events ORDER BY date")
    event = cur.fetchall()
    
    info1 = None  # Default value for info1
    
    if request.method == "POST":
        # Get form data
        eventname = request.form['eventname']
        eventdescription = request.form['eventdescription']
        
        try:
            # Insert the new event data into the 'suggestion' table
            cur.execute(
                'INSERT INTO suggestion (eventname, eventdescription) VALUES (?, ?)',
                (eventname, eventdescription)
            )
            conn.commit()  # Save changes
            info1 = "Event added successfully!"  # Success message
        except sqlite3.IntegrityError as e:
            info1 = "An error occurred while adding the event."  # Error message for unexpected issues
        finally:
            conn.close()  # Close connection

    return render_template("StudentView.html", event=event, info1=info1)


@app.route("/student_dashboard4faculty", methods=['GET', 'POST'])
def back_to_student_for_faculty():
    conn = get_db()  # Get database connection
    cur = conn.cursor()

    # Fetch events for the dashboard
    cur.execute("SELECT name, date, description, location FROM events ORDER BY date")
    event = cur.fetchall()
    
    info1 = None  # Default value for info1
    
    if request.method == "POST":
        # Get form data
        eventname = request.form['eventname']
        eventdescription = request.form['eventdescription']
        
        try:
            # Insert the new event data into the 'suggestion' table
            cur.execute(
                'INSERT INTO suggestion (eventname, eventdescription) VALUES (?, ?)',
                (eventname, eventdescription)
            )
            conn.commit()  # Save changes
            info1 = "Event added successfully!"  # Success message
        except sqlite3.IntegrityError as e:
            info1 = "An error occurred while adding the event."  # Error message for unexpected issues
        finally:
            conn.close()  # Close connection

    return render_template("StudentViewForFaculty.html", event=event, info1=info1)


@app.route('/delete_event/<event_name>', methods=['POST'])
def delete_event(event_name):
    # Connect to the SQLite database
    conn = get_db()
    cursor = conn.cursor()

    # Execute the delete statement to remove the event by its name
    cursor.execute("DELETE FROM suggestion WHERE eventname = ?", (event_name,))
    
    # Commit and close connection
    conn.commit()
    conn.close()
    # Redirect to the page where events are displayed, with a query parameter to show the modal
    return redirect(url_for('back_to_faculty', show_modal=True))

@app.route("/my_activities")
def my_activities():
    if 'email' not in session:
        return redirect(url_for('login'))  # If the student is not logged in, redirect to login

    student_email = session['email']  # Get the student's email from the session

    # Connect to the database
    db = get_db()

    # Fetch all activities with attendance status
    activities = db.execute("""
        SELECT events.id, events.name, events.date, events.description,
               IFNULL(attendance.events_attended, 0) AS attended
        FROM events
        LEFT JOIN attendance ON events.id = attendance.event_id AND attendance.email = ?
    """, (student_email,)).fetchall()

    # Convert the results to a list of dictionaries for easier handling in the template
    activities = [
        {
            'name': activity['name'],
            'date': activity['date'],
            'description': re.sub(r'<p>|</p>', '', activity['description']),  # get rid of <p> tags
            'attended': bool(activity['attended'])  # Convert 0/1 to a boolean
        }
        for activity in activities
    ]
    
    return render_template("MyActivities.html", activities=activities)


@app.route("/my_activities4faculty")
def my_activities_for_faculty():
    return render_template("MyActivitiesforFaculty.html")

@app.route('/logout')
def logout():
    
    return render_template("StartPage.html")

@app.route('/print_report')
def print_report():
        return render_template('PrintReport.html')

@app.route('/event_suggestions')
def event_suggestions():
    conn = get_db()  # Get database connection
    cur = conn.cursor()

    # Fetch event suggestions
    cur.execute("SELECT eventname, eventdescription FROM suggestion")
    suggestions = cur.fetchall()  # List of tuples (eventname, eventdescription)

    conn.close()  # Close the connection

    return render_template('EventSuggestions.html', suggestions=suggestions)

@app.route('/my_students')
def my_students():
    db = get_db()
    students = db.execute("""
        SELECT
            u.firstName || ' ' || u.lastName AS name,
            u.email,
            COUNT(a.event_id) AS events_attended
        FROM users u
        LEFT JOIN attendance a ON u.email = a.email
        WHERE u.role = 'student'
        GROUP BY u.email
    """).fetchall()
    return render_template('MyStudents.html', students=students)



if __name__ == '__main__':
    app.run(debug=True)
