

--Create Database
CREATE DATABASE uwi;
GRANT ALL PRIVILEGES ON uwi TO nacho@localhost;


--Create Tables
--input will be updated during script creation
CREATE Table Account (UserID int, uType varchar(8), pass varchar(255))
CREATE Table Student (StudentID int, FirstName varchar(255), LastName varchar(255), pass varchar(255));
CREATE Table Lecturer (LecID int, FirstName varchar(255), LastName varchar(255), pass varchar(255) );


CREATE Table Courses (CourseID int, CourseName varchar(255), CourseCode varchar(255) );
CREATE Table Content (CourseID int, ContentType varchar(6), Section varchar(255));

CREATE Table Teaches (LecID int, LecName varchar(255), CourseID int, CourseName varchar(255));
CREATE Table Assignment (AssID int, CourseID int, Grade int);
CREATE Table Grades (CourseID int, StudentID int, AvGrade int); --course averages

CREATE Table Event (EventID int, CourseID int, EventName varchar(255), Duedate date);

CREATE Table Forum (ForumID int, CourseID int, ForumName varchar(255));
CREATE Table Thread (ThreadID int, ParentID int,ForumID int, title varchar(255), body varchar(255)); --if parentID=0, it's the main thread
