-- populate_table.sql

-- Insert sample faculty data
INSERT INTO faculty (username, password) VALUES 
    ('admin', 'hashed_password_1'),  -- Replace with hashed passwords
    ('faculty1', 'hashed_password_2'),
    ('faculty2', 'hashed_password_3');

-- Insert sample events data
INSERT INTO events (name, date, location, description) VALUES
    ('Annual Science Fair', '2024-11-10', 'Main Hall', 'A showcase of student projects.'),
    ('Department Meeting', '2024-09-30', 'Room 101', 'Monthly faculty meeting.'),
    ('Guest Lecture', '2024-10-15', 'Auditorium', 'Lecture by an industry expert.');
