

-- populates the users table (handles both students and admins)
INSERT INTO users (firstName, lastName, password, email, role)
VALUES ('Carter', 'Smart', 'ab213', 'carter@example.com', 'student'),
       ('Nathan', 'Taco', 'ab123', 'nathan@example.com', 'admin'),
       ('Rachel', 'Hamilton', 'abc12', 'Rachel@example.com', 'student'),
       ('Liz', 'Honey', 'abc13', 'Liz@example.com', 'admin'),
       ('Katelyn', 'Hoeting', 'abc14', 'Katelyn@example.com', 'student');


-- populates the events table (stores details of the events students can attend)
INSERT INTO events (name, description, date, location, time)
VALUES ('Computer Science Club Meeting', 'Monthly meeting', '2024-10-10', 'CS LAB', '1:00 PM'),
       ('Cyber Defense Meeting', 'NCL', '2024-10-11', 'Hailstones 15', '5:00 PM'),
       ('Gary Windows Event', 'Windows 11 installation', '2024-10-12', 'CS LAB', '10:00 AM'),
       ('Girl Scout CS event', 'Teach girl scouts', '2024-10-13', 'Hub 102', '6:30 PM');



-- populates the attendance table (records which students attended which events)
INSERT INTO attendance (email, name, events_attended)
VALUES ('nathan@example.com', 'Nathan', 1);

-- populates the suggestion table (stores details of the events students request to faculty)
INSERT INTO suggestion (eventname, eventdescription)
VALUES ('Event 1', 'This is a description')

-- populates the other_departments table with Name, description, and head of dept in the database
/*INSERT INTO other_departments (name, description, head)
VALUES ('Philosophy', 'Philosophy Department focuses on philosophy', 'Richard Polt'),
       ('English', 'English page focuses on English', 'Lara Dorger'),
       ('Biology', 'Biology page focuses on Biology', 'Mike Gehner'),
       ('Nursing', 'Nursing page focuses on Nursing', 'John Little');



