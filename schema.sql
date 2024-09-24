DROP TABLE IF EXISTS item;
DROP TABLE IF EXISTS attendance;
DROP TABLE IF EXISTS admin_actions;
DROP TABLE IF EXISTS events;
DROP TABLE IF EXISTS users;


CREATE TABLE item (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL,
    quantity INTEGER NOT NULL
);


/* Users Table: Stores information about students and admins
* id: Unique identifier for each user
* username: The user's login name
* password: Stores a hashed password for user's for additional security
* email: The user's email, which is also unique
* role: Either student or admin, to differentiate the user types
*/


-- Users Table: Stores information about students and admins
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    role TEXT NOT NULL CHECK (role IN ('student', 'admin'))
);

-- Event Table: Stores event details
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

-- Admin Actions Table: Records admin actions on events
CREATE TABLE admin_actions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    admin_id INTEGER NOT NULL,
    action TEXT NOT NULL,
    event_id INTEGER,
    performed_on TEXT NOT NULL,
    FOREIGN KEY (admin_id) REFERENCES users(id),
    FOREIGN KEY (event_id) REFERENCES events(id)
);







