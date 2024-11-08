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
    firstName TEXT UNIQUE NOT NULL,
    lastName TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    role TEXT NOT NULL CHECK (role IN ('student', 'admin'))
);

/*Event Table: Stores event details
* id: Unique identifier for each event
* name: The name of the event
* Descri
*
*/
CREATE TABLE events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    date TEXT NOT NULL,
    location TEXT
);

-- Attendance Table: Records attendance for events
CREATE TABLE attendance (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    event_id INTEGER NOT NULL,
    attended_on TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (event_id) REFERENCES events(id),
    UNIQUE(user_id, event_id)
);


CREATE TABLE IF NOT EXISTS suggestion (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    eventname TEXT NOT NULL,
    eventdescription TEXT,
    UNIQUE(eventname)
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






