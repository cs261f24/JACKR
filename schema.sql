DROP TABLE IF EXISTS item;
DROP TABLE IF EXISTS suggestion;
DROP TABLE IF EXISTS attendance;
DROP TABLE IF EXISTS events;
DROP TABLE IF EXISTS users;
/*DROP TABLE IF EXISTS other_departments;
*/

/* Users Table: Stores information about students and admins
* id: Unique identifier for each user
* username: The user's login name
* password: Stores a hashed password for user's for additional security
* email: The user's email, which is also unique
* role: Either student or admin, to differentiate the user types
*/
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    firstName TEXT NOT NULL,
    lastName TEXT NOT NULL,
    password TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    role TEXT NOT NULL CHECK (role IN ('student', 'admin'))
);

/*Event Table: Stores event details
* id: Unique identifier for each event
* name: The name of the event
* description: The name of the description
*
*/
CREATE TABLE events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL,
    description TEXT,
    date TEXT NOT NULL,
    location TEXT,
    time TEXT NOT NULL
);

-- Attendance Table: Records attendance for events
CREATE TABLE attendance (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT NOT NULL,
    name TEXT NOT NULL,
    event_id INTEGER NOT NULL,
    events_attended BOOLEAN DEFAULT 0,
    FOREIGN KEY (event_id) REFERENCES events (id),
    UNIQUE (email, event_id) -- Ensure uniqueness for each user-event pair
);


CREATE TABLE suggestion (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    eventname TEXT NOT NULL,
    eventdescription TEXT
);
/* Departments Table: Stores information about various departments
* id: Unique identifier for each department
* name: The name of the department
* description: A brief description of what the department focuses on
* head: The head of the department
*/
/*CREATE TABLE other_departments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL,
    description TEXT,
    head TEXT,
);






