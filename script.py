from faker import Faker
from faker.providers import DynamicProvider
import random

fake = Faker()

sqls = []
ids = []
cids = []
lids = []  # Define ids list

course_provider = DynamicProvider(
    provider_name="course",
    elements=["Intro to Computing", "Object-oriented Programming", "Math for Computing", "Computing and Society",
              "Discrete Mathematics for Computer Science", "Analysis of Algorithms", "Digital Logic Design",
              "Software Engineering", "Object Technology", "Net-Centric Computing", "Computer Organisation",
              "Operating Systems", "Introduction to Artificial Intelligence", "Database Management Systems",
              "Language Processors", "Theory of Computation", "Real-Time Embedded Systems", "Group Project",
              "Internship in Computing", "Project Management"]
)

item_provider = DynamicProvider(
    provider_name="item_type",
    elements=["link", "file", "slide"]
)

fake.add_provider(course_provider)
fake.add_provider(item_provider)


def real_job(fake):
    job = fake.job()
    job = job.replace("'", "")
    return job


with open('queries.sql', 'w') as file:
    file.write(f"use uwi;\n")
    # INSERT INTO ACCOUNT
    for i in range(2):
        id = 9000 + i
        fname = fake.first_name()
        lname = fake.last_name()
        type = "Admin"
        pa = type + str(id)
        file.write(
            "INSERT INTO Account (UserID, uType, Pass, FirstName, LastName) VALUES ('{}','{}','{}','{}','{}');\n".format(
                id, type, pa, fname, lname))

    id = 0
    for i in range(100):
        id += 1
        ids.append(id)
        fname = fake.first_name()
        lname = fake.last_name()
        type = "Student"
        pa = fname + str(random.randint(0, 200))
        file.write(
            "INSERT INTO Account (UserID, uType, Pass, FirstName, LastName) VALUES ('{}','{}','{}','{}','{}');\n".format(
                id, type, pa, fname, lname))

    for _ in range(3):
        lid = random.randint(1011, 1050)
        fname = fake.first_name()
        lname = fake.last_name()
        lids.append(lid)  # Append lid to lids list
        pa = fname + str(random.randint(0, 20))
        type = "Lecturer"

        file.write(
            "INSERT INTO Account (UserID, uType, Pass, FirstName, LastName) VALUES ('{}','{}','{}','{}','{}');\n".format(
                lid, type, pa, fname, lname))

    # INSERT INTO COURSE
    for i in range(20):
        cid = 3001 + i
        c_code = "COMP" + str(cid)
        cname = fake.unique.course()
        cids.append(cid)
        file.write(
            "INSERT INTO Course (CourseID, CourseName, CourseCode) VALUES ('{}','{}','{}');\n".format(cid, cname,
                                                                                                          c_code))

    # INSERT INTO SECTION
    for cid in cids:
        for i in range(0, 2):
            secid = i + 1
            file.write("INSERT INTO Section(CourseID, SectionID) VALUES ('{}','{}');\n".format(cid, secid))

    # INSERT INTO ITEM
    for secid in range(1, len(cids) * 2 + 1):
        for i in range(0, 4):
            itemid = i + 20
            title = "Learning File" + " " + str(i)
            itype = fake.item_type()
            file.write("INSERT INTO Item(SectionID,ItemID,title,itype) VALUES ('{}','{}','{}','{}');\n".format(secid,
                                                                                                                   itemid,
                                                                                                                   title,
                                                                                                                   itype))

    # INSERT INTO TEACHES
    for cid in cids:
        lid = lids.pop(0)
        lids.append(lid)
        file.write("INSERT INTO Teaches (CourseID, UserID) VALUES ('{}','{}');\n".format(cid, lid))

    # Populate Enroll table
    for student_id in ids:
        # Randomly select courses for each student
        enrolled_courses = random.sample(cids, random.randint(3, 6))
        for course_id in enrolled_courses:
            file.write("INSERT INTO Enroll (CourseID, StudentID) VALUES ('{}','{}');\n".format(course_id, student_id))

    # Populate Assignment table
    for course_id in cids:
        for student_id in ids:
            # Simulate assignments for each enrolled student in each course
            assignment_id = 1111  # Reset assignment ID for each course
            for _ in range(1):  # Simulate 5 assignments per course
                grade = random.randint(0, 100)
                sdate = fake.date()
                file.write(
                    "INSERT INTO Assignment (AssID, UserID, CourseID, Grade, date_submit) VALUES ('{}','{}','{}','{}','{}');\n".format(
                        assignment_id, student_id, course_id, grade, sdate))
                assignment_id += 1

print("SQL generated successfully")
