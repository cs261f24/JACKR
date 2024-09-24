INSERT INTO item(name, quantity) VALUES('Table', 10);
INSERT INTO item(name, quantity) VALUES('Chair', 20);

-- populates the users table (handles both students and admins)
INSERT INTO users (username, password, email, role)
VALUES ('Carter', 'ab213', 'carter@example.com', 'student'),
       ('Nathan', 'ab123', 'nathan@example.com', 'admin');


-- populates the events table (stores details of the events students can attend)
INSERT INTO events (name, description, date, location)
VALUES ('Computer Science Club Meeting', 'Monthly meeting', '2024-10-10', 'CS LAB'),
       ('Cyber Defense Meeting', 'NCL', '2024-10-11', 'Hailstones 15');


-- populates the attendance table (records which students attended which events)
INSERT INTO attendance (user_id, event_id, attended_on)
VALUES (1, 1, '2024-10-10'),
       (1, 2, '2024-10-11');