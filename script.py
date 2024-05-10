from faker import Faker
from faker.providers import DynamicProvider
import random
import mysql.connector

fake = Faker()
schemas = []
sqls = []
sqlsStu = []
sqlsAcc = []
ids = []
courses = []
lids = []
lecmax = []
fids = []
tids = []
secids = []
as_courses = []

#Database creation
schemas.append("DROP DATABASE IF EXISTS uwi;")
schemas.append("CREATE DATABASE uwi;")
schemas.append("USE uwi;")

schemas.append("CREATE Table Account (UserID int AUTO_INCREMENT PRIMARY KEY, uType varchar(8), Pass varchar(255), FirstName varchar(255), LastName varchar(255));")

schemas.append("CREATE Table Course (CourseID int AUTO_INCREMENT PRIMARY KEY, CourseName varchar(80), CourseCode varchar(255) UNIQUE);")

schemas.append("""CREATE Table Section(SectionID int AUTO_INCREMENT PRIMARY KEY, CourseID int, SectionName varchar(255),
                FOREIGN KEY (CourseID) REFERENCES Course(CourseID));""")

schemas.append("""CREATE Table Item(SectionID int, ItemID int AUTO_INCREMENT PRIMARY KEY, title varchar(80), itype varchar(20),
FOREIGN KEY (SectionID) REFERENCES Section(SectionID));""")

schemas.append("""CREATE TABLE Teaches (CourseID INT,UserID INT, PRIMARY KEY (CourseID, UserID),
FOREIGN KEY (CourseID) REFERENCES Course(CourseID),
FOREIGN KEY (UserID) REFERENCES Account(UserID));""")

schemas.append("""CREATE Table Assignment (AssID int AUTO_INCREMENT PRIMARY KEY, UserID int, CourseID int,date_submit date,
FOREIGN KEY (UserID) REFERENCES Account(UserID),
FOREIGN KEY (CourseID) REFERENCES Course(CourseID));""")

schemas.append("""CREATE Table Grades(AssID int PRIMARY KEY, Grade int,
FOREIGN KEY (AssID) REFERENCES Assignment(AssID));""")

schemas.append("""CREATE Table Enroll (CourseID int, StudentID int, PRIMARY KEY (CourseID, StudentID),
FOREIGN KEY (CourseID) REFERENCES Course(CourseID),
FOREIGN KEY (StudentID) REFERENCES Account(UserID));""")

schemas.append("""CREATE Table Event (EventID int AUTO_INCREMENT PRIMARY KEY, CourseID int, EventName varchar(255),Duedate date,
FOREIGN KEY (CourseID) REFERENCES Course(CourseID));""")

schemas.append("""CREATE Table Forum (ForumID int AUTO_INCREMENT PRIMARY KEY, CourseID int, ForumName varchar(255),
FOREIGN KEY (CourseID) REFERENCES Course(CourseID));""")

schemas.append("""CREATE Table Thread (ThreadID int AUTO_INCREMENT PRIMARY KEY, ForumID int, Title varchar(80), Body varchar(2048), created_by varchar(30),
FOREIGN KEY (ForumID) REFERENCES Forum(ForumID)); """)

schemas.append("""CREATE Table Replies (MainThreadID int, ReplyID int AUTO_INCREMENT PRIMARY KEY, ReplyBody varchar(2048), created_by varchar(30),
FOREIGN KEY (MainThreadID) REFERENCES Thread(ThreadID));""")

course_provider = DynamicProvider(
    provider_name = "course",
    elements = ["Intro to Computing", "Object-oriented Programming","Math for Computing","Computing and Society", "Discrete Mathematics for Computer Science","Analysis of Algorithms","Digital Logic Design","Software Engineering","Object Technology","Net-Centric Computing","Computer Organisation"," Operating Systems","Introduction to Artificial Intelligence","Database Management Systems","Language Processors","Theory of Computation","Real-Time Embedded Systems","Group Project","Internship in Computing","Project Management"]
)
id = 0
item_provider = DynamicProvider(
    provider_name = "item_type",
    elements = ["link", "file", "slide"]
)

fake.add_provider(course_provider)
fake.add_provider(item_provider)

def real_job(fake):
    job = fake.job()
    job = job.replace("'","")
    return job

#INSERT INTO ACCOUNT
for i in range(1):
    id = 1
    fname = fake.first_name()
    lname= fake.last_name()
    type = "Admin"
    pa = type + str(9000 + id)
    sql = "INSERT INTO Account (uType, Pass, FirstName, LastName) VALUES ('{}','{}','{}','{}');".format(type, pa,fname,lname)
    sqls.append(sql)


for i in range(100000):
    id += 1
    ids.append(id)
    fname = fake.first_name()
    lname= fake.last_name()
    type = "Student"
    pa = fname + str(random.randint(0,200))
    sql = "INSERT INTO Account (uType, Pass, FirstName, LastName) VALUES ('{}','{}','{}','{}');".format(type, pa,fname,lname)
    sqls.append(sql)


for _ in range(85):
    id += 1
    fname = fake.first_name()
    lname= fake.last_name()
    lids.append(id) 
    pa = fname + str(random.randint(0,20))
    type = "Lecturer"

    sql = "INSERT INTO Account (uType, Pass, FirstName, LastName) VALUES ('{}','{}','{}','{}');".format(type, pa,fname,lname)
    sqls.append(sql)


#INSERT INTO COURSE   
for i in range(210):
    cid = 1 + i
    c_code = "COMP" + str(cid + 3000)
    cname = fake.word() + " studies"
    courses.append((cid, cname, c_code))

for cid, cname, c_code in courses:
    sql = "INSERT INTO Course (CourseName, CourseCode) VALUES ('{}','{}');".format(cname, c_code)
    sqls.append(sql)

#INSERT INTO SECTION
for cid, cname, c_code in courses:
    for i in range(0,2):
        secid = i +1
        secids.append(secid)
        sql = "INSERT INTO Section(CourseID) VALUES ('{}');".format(cid)
        sqls.append(sql)

#INSERT INTO ITEM
for secid in secids:
    for i in range(0,4):
        itemid = i + 20
        title = "Learning File" + " " + str(i)
        type = fake.item_type()
        sql = "INSERT INTO Item(SectionID,title,itype) VALUES ('{}','{}','{}');".format(secid,title,type)
        sqls.append(sql)

#INSERT INTO TEACHES
teaches = {}
courseCopy = list(courses)
#Ensuring that each lectuer has a course
for lid in lids:
    course = random.choice(courseCopy)
    courseCopy.remove(course)
    teaches[lid] = teaches.get(lid, 0) + 1
    sql = "INSERT INTO Teaches (CourseID, UserID) VALUES ('{}','{}');".format(course[0],lid)
    sqls.append(sql)

#Assigning the remaining courses to ensure each course has a lecturer
while (len(courseCopy) != 0):
    for course in courseCopy:
        lid = random.choice(lids)
        courseCopy.remove(course)
        teaches[lid] = teaches.get(lid, 0) + 1
        if teaches.get(lid, 0) == 5:
            lids.remove(lid)
        sql = "INSERT INTO Teaches (CourseID, UserID) VALUES ('{}','{}');".format(course[0],lid)
        sqls.append(sql)

#INSERT INTO ENROLL
enrolled = {}
#Ensuring that each course has 10 students
studentsCopy = list(ids)
for course in courses:
    students = random.sample(studentsCopy, 10)
    for id in students:
        enrolled[id] = enrolled.get(id, [])
        enrolled[id].append(course)
        sql = "INSERT INTO Enroll (CourseID, StudentID) VALUES ('{}','{}');".format(course[0],id)
        sqls.append(sql)
        studentsCopy.remove(id)


#Ensuring each student does between 3 and 6 courses
studentsCopy = list(ids)
for id in studentsCopy:
    numC = len(enrolled.get(id, []))
    num_courses = random.randint(3 - numC, 6 - numC)
    courses_enroll = random.sample([course for course in courses if course not in enrolled.get(id, [])], num_courses)
    for course in courses_enroll:
        enrolled.get(id, []).append(course)
        sql = "INSERT INTO Enroll (CourseID, StudentID) VALUES ('{}','{}');".format(course[0],id)
        sqls.append(sql)

def get_db_connection():
    connection = mysql.connector.connect(
    host = 'localhost',
    user= 'comp3161',
    password = 'password123!',
    database = 'uwi')
    return connection


with open(r'insert.sql','w') as f:
    connection = get_db_connection()
    cursor = connection.cursor()
    print("Creating database...")
    for schema in schemas:
        f.write(schema + '\n')
        try:
            cursor.execute(schema)
            connection.commit()
        except mysql.connector.Error as e:
            print(str(e))
    print("Database completed.")
    print("Running insert queries...")
    for i, sql in enumerate(sqls):
        f.write(sql + '\n')
        try:
            cursor.execute(sql)
            connection.commit()
        except mysql.connector.Error as e:
            print(str(e))
    cursor.close()
    connection.close()
print("Tables populated")