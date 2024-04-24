--Create Database
CREATE DATABASE uwi;
GRANT ALL PRIVILEGES ON uwi TO nacho@localhost;


--Create Tables
--input will be updated during script creation
CREATE Table Account (UserID int, uType varchar(8), Pass varchar(255), FirstName varchar(255), LastName varchar(255)) 


CREATE Table Course (CourseID int, CourseName varchar(80), CourseCode varchar(255));
CREATE Table Section (CourseID int, SectionID int);
CREATE Table Item(SectionID int, ItemID int, title int, itype varchar(20));
CREATE Table Teaches(CourseID int, UserID int);

CREATE Table Assignment (AssID int, UserID int, CourseID int, Grade int, date_submit date);
CREATE Table Enroll (CourseID int, StudentID int, AvGrade int); --course averages

CREATE Table Event (EventID int, CourseID int, EventName varchar(255),Duedate date);


CREATE Table Forum (ForumID int, CourseID int, ForumName varchar(255));
CREATE Table Thread (ThreadID int, ForumID int, Title varchar(80), Body varchar(255), created_by varchar(30)); --if parentID=0, it's the main thread
CREATE Table Replies (MainThreadID int, ReplyID int, ReplyBody varchar(255), created_by varchar(30));