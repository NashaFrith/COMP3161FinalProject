from faker import Faker
from faker.providers import DynamicProvider
import random


fake = Faker()
sqls = []
sqlsStu = []
sqlsAcc = []
ids = []
cids = []
lids = []
lecmax = []
fids = []
tids = []
secids = []
as_courses = []

course_provider = DynamicProvider(
    provider_name = "course",
    elements = ["Intro to Computing", "Object-oriented Programming","Math for Computing","Computing and Society", "Discrete Mathematics for Computer Science","Analysis of Algorithms","Digital Logic Design","Software Engineering","Object Technology","Net-Centric Computing","Computer Organisation"," Operating Systems","Introduction to Artificial Intelligence","Database Management Systems","Language Processors","Theory of Computation","Real-Time Embedded Systems","Group Project","Internship in Computing","Project Management","Academic Writing I & II","Abnormal Psychology","Accommodations Management","Advanced Financial Accounting","Advanced Financial Management","Advanced Taxation","Applied Mathematics for Hospitality","Applied Research","Audit Practice & Procedures I & II","Bar Operations","Behaviour and the Social Environment","Fundamentals of Accounting","Game Theory I","Geographical Information Systems","Gerontology","Hospitality Accounting","Hospitality Ethics","Hospitality Law","Human and Social Behaviour","Human Computer Interaction & Interface Design","Human Development and Function","Human Relation in Organization","Human Resource Counselling","Human Resource Information Systems","Human Sexual Behaviour","Industrial & Employee Relations","Industrial Automation","Information Assurance & Security","Information Technology Audit and Controls","Innovation in Production and Operations Management","Intake and Assessment","Integrated Food Service Management","Integrated Marketing Communication","Intelligent Systems","International Business Management","International Economics","International Logistics","International Marketing","International Travel & Tourism","Internet Authoring I & II","Internship 1 & II","Internship Logistics Supply Chain","Introduction to Advertising","Introduction to Business & Economic Statistics","Introduction to Business Administration","Introduction to Family Counselling","Introduction to Forensic Psychology","Introduction to Literature","Introduction to Politics","Introduction to Production and Operations Management","Introduction to Psychology","Introduction to Research","Introduction to Sociology","Introduction to Spanish","Introduction to Supervisory Management","Introduction to Tourism & Hospitality Management","Job Analysis and Design","Labour Economics","Legal and Ethical Issues","Legal Concepts for Commerce","Linux+","Management Accounting","Management Information Systems","Management of Social Service Organization","Managing Cultural Diversity","Manufacturing Strategies","Market Research", "Marketing Management","Materials Management","Menu Planning","Mobile App Development","Object Oriented Programming Design using C++","Occupational Health and Safety","Operating Systems","Organization Design, Development and Dynamics","Organizational Psychology","Organizational Theory & Behaviour","Orientation to University Life","Performance Management","Personality Theories","Port Management","Portfolio Management","Practicum I & II","Principles of Microeconomics","Principles of Macro Economics","Principles of Marketing","Principles of Preventative Maintenance","Principles of Preventative Maintenance & Waste Management","Principles of Time Management","Production and Operations Management","Programming Design using Java","Programming Techniques","Project Management","Project+","Psychological Tests and Measurement","Public Relations","Public Speaking","Purchasing Management","Quality Management","Quantitative Methods","Recruitment, Selection and Orientation","Retail Management","Risk Analysis and Management","Sales Management","Sanitation, Hygiene & Safety","Securities Analysis","Security +","Server Plus","Social Justice and Advocacy","Social Media/Market Optimisation","Social Psychology","Social Work Practice I, II, III","Social Work Theories and Policy Frameworks","Sociology of Family and Relationships","Spa Services & Management","Statistics for the Behavioural Sciences","Strategic Management","Strategic Marketing","Sustainable Tourism","System Analysis & Design I & II","Taxation Theory and Practice","Tourism & Hospitality Marketing","Tourism Marketing","Tourism Planning & Policy Development","Training and Development","Transportation Management","Warehouse & Inventory Management","courseA","courseB","courseC","courseD","courseE","courseF"]
)

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

#Create Queries
sql = "CREATE Table Account (UserID int, uType varchar(8), Pass varchar(255), FirstName varchar(255), LastName varchar(255),PRIMARY KEY(UserID))"
sqls.append(sql)
sql = "CREATE Table Course (CourseID int, CourseName varchar(80), CourseCode varchar(20), PRIMARY KEY(CourseID));"
sqls.append(sql)
sql = "CREATE Table Section (CourseID int, SectionID int, PRIMARY KEY(SectionID));"
sqls.append(sql)
sql = "CREATE Table Item(SectionID int, ItemID int, title int, itype varchar(20), PRIMARY KEY(ItemID));"
sqls.append(sql)
sql = "CREATE Table Teaches(CourseID int, UserID int, PRIMARY KEY(CourseID));"
sqls.append(sql)
sql = "CREATE Table Assignment (AssID int, UserID int, CourseID int, Grade int, date_submit date, PRIMARY KEY(AssID));"
sqls.append(sql)
sql = "CREATE Table Enroll (CourseID int, StudentID int, PRIMARY KEY(CourseID));"
sqls.append(sql)
sql = "CREATE Table Event (EventID int, CourseID int, EventName varchar(255), Duedate date, PRIMARY KEY(EventID));"
sqls.append(sql)
sql = "CREATE Table Forum (ForumID int, CourseID int, ForumName varchar(255));"
sqls.append(sql)
sql = "CREATE Table Thread (ThreadID int, ForumID int, Title varchar(80), Body varchar(255), created_by varchar(30));"
sqls.append(sql)
sql = "CREATE Table Replies (MainThreadID int, ReplyID int, ReplyBody varchar(255), created_by varchar(30));"
sqls.append(sql)

with open(r'/home/nacho/repos/COMP3161FinalProject/insert.sql','w') as f:
    for i, sql in enumerate(sqls):
        f.write(sql + '\n')


#INSERT INTO ACCOUNT
for i in range(1):
    id = 9000 + i
    fname = fake.first_name()
    lname= fake.last_name()
    type = "Admin"
    pa = type + str(id)
    sql = "INSERT INTO Account (UserID, uType, Pass, FirstName, LastName) VALUES ('{}','{}','{}','{}','{}')".format(id, type, pa,fname,lname)
    sqls.append(sql)

id = 0
for i in range(100000):
    id = id + 1
    ids.append(id)
    fname = fake.first_name()
    lname= fake.last_name()
    type = "Student"
    pa = fname + str(random.randint(0,200))
    sql = "INSERT INTO Account (UserID, uType, Pass, FirstName, LastName) VALUES ('{}','{}','{}','{}','{}')".format(id, type, pa,fname,lname)
    sqls.append(sql)


for _ in range(30):
    lid = random.randint(1011,1050)
    fname = fake.first_name()
    lname= fake.last_name()
    lids.append(lid) 
    pa = fname + str(random.randint(0,20))
    type = "Lecturer"

    sql = "INSERT INTO Account (UserID, uType, Pass, FirstName, LastName) VALUES ('{}','{}','{}','{}','{}')".format(lid, type, pa,fname,lname)
    sqls.append(sql)


#INSERT INTO COURSE   
for i in range(200):
    cid = 3001 + i
    c_code = "COMP" + str(cid)
    cname = fake.unique.course()
    cids.append(cid)

for cid in cids:
    sql = "INSERT INTO Course (CourseID, CourseName, CourseCode) VALUES ('{}','{}','{}')".format(cid,cname,c_code)
    sqls.append(sql)

#INSERT INTO SECTION
for cid in cids:
    for i in range(0,2):
        secid = i +1
        secids.append(secid)
        sql = "INSERT INTO Section(CourseID, SectionID) VALUES ('{}','{}')".format(cid,secid)
        sqls.append(sql)

#INSERT INTO ITEM
for secid in secids:
    for i in range(0,4):
        itemid = i + 20
        title = "Learning File" + " " + str(i)
        type = fake.item_type()
        sql = "INSERT INTO Item(SectionID,ItemID,title,itype) VALUES ('{}','{}','{}','{}')".format(secid,itemid,title,type)
        sqls.append(sql)

#INSERT INTO TEACHES
for cid in cids:
    lid = lids.pop(0)
    lids.append(lid)
    sql = "INSERT INTO Teaches (CourseID, UserID) VALUES ('{}','{}')".format(cid,lid)
    sqls.append(sql)
'''
for i in range(30):
    cid = 4001 + i
    c_code = "INFO" + str(cid)
    cname = "IT" + " " + real_job(fake)
    sql = "INSERT INTO Course (CourseID, CourseName, CourseCode) VALUES ('{}','{}','{}')".format(cid,cname,c_code)
    sqls.append(sql)
    cids.append(cid)
'''

#INSERT INTO ENROLL
for s in sqls:
    if s.startswith("INSERT INTO Account"):
        id = s.split("'")[1]
        type = s.split("'")[3]
    
        if type == "Student":          
            i = random.randint(3,6) 
            for _ in range(i):
                cid = random.choice(cids)
                if cid not in as_courses:
                    as_courses.append(cid)
                    break
                grade = random.randint(0,100)
                sql = "INSERT INTO Enroll (CourseID, StudentID) VALUES ('{}','{}')".format(cid,id)
                sqls.append(sql)

#INSERT INTO ASSIGNMENT
i = 1
for s in sqls:
    if s.startswith("INSERT INTO Enroll"):
        cid = s.split("'")[1]
        id = s.split("'")[3]
        print(id)
        aid = 1111 + i
        i+=1
        grade = random.randint(0,100)
        sdate = fake.date()

        sql = "INSERT INTO Assignment (AssID, UserID, CourseID,Grade,date_submit) VALUES ('{}','{}','{}','{}','{}')".format(aid,id,cid,grade,sdate)
        sqls.append(sql)


#INSERT INTO EVENT
i = 1
for cid in cids:
    eid = 2222 + i
    ddate = fake.date()
    i + 1
    ename = "Assignment" + " " + str(i)
    sql = "INSERT INTO Event (EventID, CourseID, EventName, Duedate) VALUES ('{}','{}','{}','{}')".format(eid,cid,ename,ddate)
    sqls.append(sql)

#INSERT INTO FORUM
for i in range(5):
    fid = i
    fids.append(fid)
    cid = random.choice(cids)
    fname = "What do you think about" + fake.unique.color()
    sql = "INSERT INTO Forum (ForumID, CourseID, ForumName) VALUES ('{}','{}','{}')".format(fid,cid,fname)
    sqls.append(sql)

#INSERT INTO THREAD
for i in range(2):
    tid = 100 + random.randint(0,100)
    fid = random.choice(fids)
    title = fake.sentence(10)
    body = fake.sentence(50)
    tids.append(tid)
    id = random.choice(ids)

    sql = "INSERT INTO Thread (ThreadID, ForumID, Title, Body,created_by) VALUES ('{}','{}','{}','{}','{}')".format(tid,fid,title,body,id)
    sqls.append(sql)

#INSERT INTO REPLIES
for i in range(2):
    tid = random.choice(tids)
    rid = 200 + random.randint(0,200)
    body = fake.sentence(20)
    id = random.choice(ids)
    
    sql = "INSERT INTO Replies (MainThreadID, ReplyID,ReplyBody,created_by) VALUES ('{}','{}','{}','{}')".format(tid,rid,body,id)
    sqls.append(sql)


#with open(r'/home/nacho/repos/COMP3161FinalProject/insert.sql','w') as f:
    #for i, sql in enumerate(sqls):
        #f.write(sql + '\n')