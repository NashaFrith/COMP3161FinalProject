

--Create Database
CREATE DATABASE uwi;
GRANT ALL PRIVILEGES ON uwi TO nacho@localhost;


--Create Tables
--input will be updated during script creation
CREATE Table Account (UserID int, uType varchar(8), Pass varchar(255))
CREATE Table Student (StudentID int, FirstName varchar(255), LastName varchar(255));
CREATE Table Lecturer (LecID int, LecName varchar(255));


CREATE Table Course (CourseID int, CourseName varchar(255), CourseCode varchar(255), LecID int);
CREATE Table Section (CourseID int, SectionID int);


CREATE Table Assignment (AssID int, CourseID int, Grade int);
CREATE Table Assign (CourseID int, StudentID int, AvGrade int); --course averages

CREATE Table Event (EventID int, CourseID int, EventName varchar(255), Duedate date);

CREATE Table Forum (ForumID int, CourseID int, ForumName varchar(255));
CREATE Table Thread (ThreadID int, ForumID int, Title varchar(255), Body varchar(255)); --if parentID=0, it's the main thread
CREATE Table Reply (MainThreadID int, ReplyID int, UserID int, ReplyBody varchar(255));