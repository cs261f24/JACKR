

-- populates the users table (handles both students and admins)
INSERT INTO users (username, password, email, role)
VALUES ('Carter', 'ab213', 'carter@example.com', 'student'),
       ('Nathan', 'ab123', 'nathan@example.com', 'admin'),
       ('Rachel', 'abc12', 'Rachel@example.com', 'student'),
       ('Liz', 'abc13', 'Liz@example.com', 'admin'),
       ('Katelyn', 'abc14', 'Katelyn@example.com', 'student');


-- populates the events table (stores details of the events students can attend)
INSERT INTO events (name, description, date, location)
VALUES ('Computer Science Club Meeting', 'Monthly meeting', '2024-10-10', 'CS LAB'),
       ('Cyber Defense Meeting', 'NCL', '2024-10-11', 'Hailstones 15'),
       ('Gary Windows Event', 'Windows 11 installation', '2024-10-12', 'CS LAB'),
       ('Girl Scout CS event', 'Teach girl scouts', '2024-10-13', 'Hub 102');


-- populates the attendance table (records which students attended which events)
INSERT INTO attendance (user_id, event_id, attended_on)
VALUES (1, 1, '2024-10-10'),
       (1, 2, '2024-10-11'),
       (1, 3, '2024-10-11'),
       (1, 4, '2024-10-11'),
       (1, 5, '2024-10-11');