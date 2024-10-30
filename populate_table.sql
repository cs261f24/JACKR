

-- populates the users table (handles both students and admins)
INSERT INTO users (firstName, lastName, password, email, role)
VALUES ('Carter', 'Smart', 'ab213', 'carter@example.com', 'student'),
       ('Nathan', 'Taco', 'ab123', 'nathan@example.com', 'admin'),
       ('Rachel', 'Hamilton', 'abc12', 'Rachel@example.com', 'student'),
       ('Liz', 'Honey', 'abc13', 'Liz@example.com', 'admin'),
       ('Katelyn', 'Hoeting', 'abc14', 'Katelyn@example.com', 'student');


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

-- populates the other_departments table with Name, description, and head of dept in the database
/*INSERT INTO other_departments (name, description, head)
VALUES ('Philosophy', 'Philosophy Department focuses on philosophy', 'Richard Polt'),
       ('English', 'English page focuses on English', 'Lara Dorger'),
       ('Biology', 'Biology page focuses on Biology', 'Mike Gehner'),
       ('Nursing', 'Nursing page focuses on Nursing', 'John Little');



