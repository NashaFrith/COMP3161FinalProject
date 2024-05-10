-- You must have at least 100,000 students.
SELECT COUNT(*) FROM Account WHERE uType = 'Student';

-- You must have at least 200 courses.
SELECT COUNT(*) FROM Course; 

-- No student can do more than 6 courses
SELECT StudentID, FirstName, LastName, COUNT(CourseID) FROM Account a
JOIN Enroll e ON a.UserID = e.StudentID
WHERE uType = 'Student'
GROUP BY StudentID, FirstName, LastName
HAVING COUNT(CourseID) > 6;

-- A student must be enrolled in at least 3 courses.
SELECT StudentID, FirstName, LastName, COUNT(CourseID) FROM Account a
JOIN Enroll e ON a.UserID = e.StudentID
WHERE uType = 'Student'
GROUP BY StudentID, FirstName, LastName
HAVING COUNT(CourseID) < 3;

-- Each course must have at least 10 members.
SELECT CourseCode, CourseName, COUNT(StudentID) FROM Course c
JOIN Enroll e ON c.CourseID = e.CourseID
GROUP BY CourseCode, CourseName
HAVING COUNT(StudentID) < 10;

-- No lecturer can teach more than 5 courses.
SELECT t.UserID, FirstName, LastName, COUNT(CourseID) FROM Account a
JOIN Teaches t ON a.UserID = t.UserID
WHERE uType = 'Lecturer'
GROUP BY t.UserID, FirstName, LastName
HAVING COUNT(CourseID) > 5;

-- A lecturer must teach at least 1 course.
SELECT t.UserID, FirstName, LastName, COUNT(CourseID) FROM Account a
JOIN Teaches t ON a.UserID = t.UserID
WHERE uType = 'Lecturer'
GROUP BY t.UserID, FirstName, LastName
HAVING COUNT(CourseID) < 1;