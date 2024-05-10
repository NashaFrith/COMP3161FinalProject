from flask import Flask, request, make_response, jsonify
import mysql.connector

app = Flask(__name__)
app.json.sort_keys = False



def get_db_connection():
    connection = mysql.connector.connect(
    host = 'localhost',
    user= 'comp3161',
    password = 'password123!',
    database = 'uwi')
    return connection

################Register User ##################################
@app.route('/user', methods=['POST'])
def register_user():
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        content = request.json
        FirstName = content['FirstName']
        LastName = content['LastName']
        uType = content['uType']
        Pass = content['Pass']
        query = "INSERT INTO Account (FirstName, LastName, uType, Pass) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (FirstName, LastName, uType, Pass))
        connection.commit()

        cursor.execute("SELECT MAX(UserID) FROM Account")
        id = cursor.fetchone()[0]
        connection.commit()
        cursor.close()
        connection.close()
        return jsonify({"success" : "User added",
                        "message": f"Your assigned userID is {id}."})
    except Exception as e:
        return jsonify({'error': str(e)})

###############User Login################################        
@app.route('/login', methods =['POST'])
def login():
    connection = get_db_connection()
    cursor = connection.cursor()
    content = request.json
    username = content['UserID']
    password = content['Password']
    cursor.execute('SELECT * FROM Account WHERE UserID = %s AND Pass = %s', (username, password, ))
    user = cursor.fetchone()

    if user is not None:
        return jsonify({"message": "User logged in successfully",
                        "user":user}), 200
    else:
        return jsonify({"errors": "Invalid username or password"}), 400   
            
#######################Courses #############################

###create course###
@app.route('/create_course', methods=['POST'])
def create_course():
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        content = request.json
        AdminID = content['AdminID']
        CourseName = content['CourseName']
        CourseCode = content['CourseCode']  

        
        admin_query = "SELECT * FROM Account WHERE UserID = %s AND uType = 'admin'"
        cursor.execute(admin_query, (AdminID,))
        admin_result = cursor.fetchone()

        if not admin_result:
            return jsonify({'Error': 'Unauthorized'}), 401

        # Insert new course in the Course table
        course_insert_query = "INSERT INTO Course (CourseName, CourseCode) VALUES (%s, %s)"
        cursor.execute(course_insert_query, (CourseName, CourseCode))

        # Getting CourseID of the new created course
        course_id = cursor.lastrowid

        connection.commit()
        cursor.close()
        connection.close()

        return jsonify({'message': 'Course created successfully'}), 201
    except mysql.connector.Error as e:
        return jsonify({'error': str(e)}), 500

#Retrieve all courses#
@app.route('/get_all_courses', methods=['GET'])
def get_all_courses():
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        
        
        query = "SELECT * FROM Course"
        cursor.execute(query)
        
        courses = cursor.fetchall()

        cursor.close()

        return jsonify(courses), 200
    except mysql.connector.Error as e:
        return jsonify({'error': str(e)}), 500


#Retrieve courses for a student #
@app.route('/courses/student/<int:student_id>', methods=['GET'])
def get_courses_for_student(student_id):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        # Retrieve courses for the given student
        query = """SELECT CourseID, CourseName, CourseCode FROM Course WHERE CourseID IN (
            SELECT CourseID
            FROM Enroll
            WHERE StudentID = %s) """
        cursor.execute(query, (student_id,))
        courses = [{'CourseID': row[0], 'CourseName': row[1], 'CourseCode': row[2]} for row in cursor.fetchall()]

        cursor.close()
        connection.close()
        
        return jsonify(courses), 200
    except mysql.connector.Error as e:
        return jsonify({'Error': str(e)}), 500
    
# Retrieve courses taught by a particular lecturer
@app.route('/courses/lecturer/<int:lecturer_id>', methods=['GET'])
def get_courses_for_lecturer(lecturer_id):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        # Retrieve courses taught by the lecturer
        query = """SELECT CourseID, CourseName, CourseCode
            FROM Course WHERE CourseID IN ( 
                SELECT CourseID FROM Teaches WHERE UserID = %s
            )"""
        cursor.execute(query, (lecturer_id,))
        courses = [{'CourseID': row[0], 'CourseName': row[1], 'CourseCode': row[2]} for row in cursor.fetchall()]

        cursor.close()
        connection.close()
        
        return jsonify(courses), 200
    except mysql.connector.Error as e:
        return jsonify({'Error': str(e)}), 500


@app.route('/register_course', methods=['POST'])
def register_course():
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        content = request.json

        UserID = content ['UserID']  # ID of the user registering for the course
        CourseID = content ['CourseID'] # ID of the course being registered for
        Role = content ['Role']     # Role of the user (student or lecturer)


        if Role == 'student':
            UserID = content ['StudentID']  # ID of the user registering for the course
            query = "SELECT * FROM Enroll WHERE StudentID = %s AND CourseID = %s"
            cursor.execute(query, (UserID, CourseID))
            existing_registration = cursor.fetchone()
            
            if existing_registration:
                return jsonify({'Error': 'Student is already enrolled in the course'}), 400
            
            
            query = "INSERT INTO Enroll (StudentID, CourseID) VALUES (%s, %s)"
            cursor.execute(query, (UserID, CourseID))
        elif Role == 'lecturer':

            UserID = content ['UserID']  # ID of the user registering for the course
            query = "SELECT * FROM Teaches WHERE UserID = %s AND CourseID = %s"
            cursor.execute(query, (CourseID,))
            existing_assignment = cursor.fetchone()
            
            if existing_assignment and existing_assignment[3] is not None:
                return jsonify({'Error': 'Course already has a lecturer assigned'}), 400
            
            query = "INSERT INTO Teaches (UserID, CourseID) VALUES (%s, %s)"
            cursor.execute(query, (UserID, CourseID))
        else:
            return jsonify({'error': 'Invalid role'}), 400

        connection.commit()
        cursor.close()
        connection.close()
        
        return jsonify({'Message': 'Registration successful'}), 201
    except mysql.connector.Error as e:
        return jsonify({'Error': str(e)}), 500

#Retrieve members of  a course#
@app.route('/course/members/<int:course_id>', methods=['GET'])
def get_members_of_course(course_id):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        
        student_query = """SELECT Account.UserID, Account.FirstName, Account.LastName 
            FROM Account JOIN Enroll ON Account.UserID = Enroll.StudentID WHERE Enroll.CourseID = %s"""
        cursor.execute(student_query, (course_id,))
        students = [{'UserID': row[0], 'FirstName': row[1], 'LastName': row[2]} for row in cursor.fetchall()]

        lecturer_query = """SELECT Account.UserID, Account.FirstName, Account.LastName FROM Account
            JOIN Teaches ON Account.UserID = Teaches.UserID
            WHERE Teaches.CourseID = %s"""
        cursor.execute(lecturer_query, (course_id,))
        lecturer = [{'UserID': row[0], 'FirstName': row[1], 'LastName': row[2]} for row in cursor.fetchall()]

        cursor.close()
        connection.close()

        course_members = {'students': students, 'lecturer': lecturer}
        
        return jsonify(course_members), 200
    except mysql.connector.Error as e:
        return jsonify({'error': str(e)}), 500
        

#Retrieve calendar events for a course#
@app.route('/course/events/<course_id>', methods=['GET'])
def get_course_events(course_id):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        
        event_query = f"SELECT EventID, EventName, Duedate FROM Event WHERE CourseID = {course_id}"
        cursor.execute(event_query)
        events = [{'EventID': row[0], 'EventName': row[1], 'Duedate': row[2]} for row in cursor.fetchall()]

        cursor.close()
        connection.close()

        return jsonify(events), 200
    except mysql.connector.Error as e:
        return jsonify({'error': str(e)}), 500
    
#Retrieve Calendar events for student based on date#
@app.route('/student/events/<int:student_id>/<date>', methods=['GET'])
def get_events_for_student(student_id, date):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        
        # Retrieve all calendar events for the given student on the given date
        event_query = f"SELECT EventID, EventName, Duedate FROM Event WHERE CourseID IN (SELECT CourseID FROM Enroll WHERE StudentID = {student_id}) AND DATE(Duedate) = '{date}'"
        cursor.execute(event_query)
        events = [{'EventID': row[0], 'EventName': row[1], 'Duedate': row[2]} for row in cursor.fetchall()]

        cursor.close()
        connection.close()

        return jsonify(events), 200
    except mysql.connector.Error as e:
        return jsonify({'error': str(e)}), 500

####################################################
###########################Events###########################
@app.route('/events', methods=['POST'])
def create_event():
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        content = request.json
        #EventID = content['EventID']
        CourseID = content['CourseID']
        EventName = content['EventName']
        Duedate = content['Duedate']
        query = "INSERT INTO Event (CourseID, EventName, Duedate) VALUES ( %s, %s, %s)"
        cursor.execute(query, (CourseID, EventName, Duedate))
        connection.commit()
        cursor.close()
        connection.close()
        return jsonify({"success" : "Event added"})
    except Exception as e:
        return jsonify({'error': str(e)})

###########################Forums###########################
@app.route('/forums/<course_id>', methods=['GET'])
def get_forums(course_id):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        query = f"SELECT * FROM Forum WHERE CourseID = {course_id}"
        cursor.execute(query)
        result = cursor.fetchall()

        forums = []
        for ForumID, CourseID, ForumName in result:
            forums.append({
                'ForumID': ForumID,
                'CourseID': CourseID,
                'ForumName': ForumName
            })
        cursor.close()
        connection.close()
        return jsonify(forums) 

    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/forums', methods=['POST'])
def create_forum():
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        content = request.json
        #ForumID = content['ForumID']
        CourseID = content['CourseID']
        ForumName = content['ForumName']
        query = "INSERT INTO Forum (CourseID, ForumName) VALUES ( %s, %s)"
        cursor.execute(query, (CourseID, ForumName))
        connection.commit()
        cursor.close()
        connection.close()
        return jsonify({"success" : "Forum added"})
    except Exception as e:
        return jsonify({'error': str(e)})

###########################Threads###########################
@app.route('/discussion_threads/<forum_id>', methods=['GET']) 
def get_discussion_threads(forum_id):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        query = f"SELECT * FROM Thread WHERE ForumID = {forum_id}"
        cursor.execute(query)
        result = cursor.fetchall()

        threads = []
        for ThreadID, ForumID, Title, Body, created_by in result:
            threads.append({
                'ThreadID': ThreadID,
                'ForumID': ForumID,
                'Title': Title,
                'Body': Body,
                'created_by' : created_by
            })
        cursor.close()
        connection.close()
        return jsonify(threads) 

    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/discussion_threads', methods=['POST'])
def create_discussion_threads():
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        content = request.json
        #ThreadID = content['ThreadID']
        ForumID = content['ForumID']
        Title = content['Title']
        Body = content['Body']
        created_by = content['created_by']
        query = "INSERT INTO Thread (ForumID, Title, Body, created_by) VALUES ( %s, %s, %s, %s)"
        cursor.execute(query, (ForumID, Title, Body, created_by))
        connection.commit()
        cursor.close()
        connection.close()
        return jsonify({"success" : "Discussion Thread added"})
    except Exception as e:
        return jsonify({'error': str(e)})

###########################Replies###########################
@app.route('/replies', methods=['POST'])
def create_reply():
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        content = request.json
        MainThreadID = content['MainThreadID']
        #ReplyID = content['ReplyID']
        ReplyBody = content['ReplyBody']
        created_by = content['created_by']
        query = "INSERT INTO Replies (MainThreadID, ReplyBody, created_by) VALUES (%s, %s, %s)"
        cursor.execute(query, (MainThreadID,ReplyBody, created_by))
        connection.commit()
        cursor.close()
        connection.close()
        return jsonify({"success": "Reply added"})
    except Exception as e:
        return jsonify({'error': str(e)})


@app.route('/replies/<main_thread_id>', methods=['GET']) 
def get_replies(main_thread_id):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        
        def fetch_replies(thread_id):
            query = f"SELECT * FROM Replies WHERE MainThreadID = {thread_id}"
            cursor.execute(query)
            result = cursor.fetchall()

            replies = []
            for MainThreadID, ReplyID, ReplyBody, created_by in result:
                reply = {
                    'ReplyID': ReplyID,                
                    'ReplyBody': ReplyBody,
                    'created_by': created_by,
                    'replies': []  
                }
                reply['replies'] = fetch_replies(ReplyID)
                replies.append(reply)

            return replies
        all_replies = fetch_replies(main_thread_id)

        cursor.close()
        connection.close()
        return jsonify(all_replies) 

    except Exception as e:
        return jsonify({'error': str(e)})



###########################Course Content###########################
@app.route('/content/<course_id>', methods=['GET']) 
def get_content(course_id):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        query = f"SELECT * FROM Section WHERE CourseID = {course_id}"
        cursor.execute(query)
        result = cursor.fetchall()

        courseContent = []
        for CourseID, SectionID, SectionName in result:
            items = []
            query2 = f"SELECT * FROM Item WHERE SectionID = {SectionID}"
            cursor.execute(query2)
            result2 = cursor.fetchall()

            for ItemID, SectionID, title, itype in result2:
                items.append({
                    'ItemID': ItemID,
                    'SectionID': SectionID,
                    'title': title,
                    'itype': itype
                })

            courseContent.append({
                'CourseID': CourseID,
                'SectionID': SectionID,
                'SectionName': SectionName,
                'Items': items
            })
        cursor.close()
        connection.close()
        return jsonify(courseContent) 

    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/section', methods=['POST'])
def add_section():
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        content = request.json
        CourseID = content['CourseID'] 
        SectionName = content['SectionName']  
        #SectionID = content['SectionID']        
        query = "INSERT INTO Section (CourseID, SectionName) VALUES (%s, %s)"
        cursor.execute(query, (CourseID, SectionName))
        connection.commit()
        cursor.close()
        connection.close()
        return jsonify({"success" : "Course section created"})
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/items', methods=['POST'])
def add_item():
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        content = request.json
        SectionID = content['SectionID']
       # ItemID = content['ItemID']
        title = content['title']
        itype = content['itype']
        query = "INSERT INTO Item (SectionID, title, itype) VALUES (%s, %s, %s)"
        cursor.execute(query, (SectionID, title, itype))
        connection.commit()
        cursor.close()
        connection.close()
        return jsonify({"success" : "Course item added"})
    except Exception as e:
        return jsonify({'error': str(e)})

###########################Assignments###########################
@app.route('/assignments/<course_id>', methods=['GET']) 
def get_assignments(course_id): #Should it be assignments for a course or student or event?
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        query = f"SELECT * FROM Assignment WHERE CourseID = {course_id}"
        cursor.execute(query)
        result = cursor.fetchall()

        assignments = []
        for CourseID, AssID, UserID, Grade, date_submit in result:
            assignments.append({
                'CourseID': CourseID,
                'AssID': AssID,
                'UserID': UserID,
                'Grade': Grade,
                'date_submit': date_submit
            })
        cursor.close()
        connection.close()
        return jsonify(assignments) 

    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/assignments', methods=['POST'])
def submit_assignment():
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        content = request.json
        #AssID = content['AssID']
        UserID = content['UserID']
        CourseID = content['CourseID']
        date_submit = content['date_submit']
        query = "INSERT INTO Assignment (UserID, CourseID, date_submit) VALUES (%s, %s, %s)"
        cursor.execute(query, (UserID, CourseID, date_submit))
        connection.commit()
        cursor.close()
        connection.close()
        return jsonify({"success" : "Assignment submitted"})
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/add_grade/<int:assignment_id>', methods=['PUT'])
def add_assignment_grade(assignment_id):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        content = request.json
        Grade = content['Grade']
        query = f"SELECT * FROM Assignment WHERE AssID = {assignment_id}"
        cursor.execute(query)
        result = cursor.fetchone()
        if result is not None:
            cursor.execute(f"UPDATE Grade SET Grade='{Grade}' WHERE AssID={assignment_id}")
            connection.commit()
            cursor.close()
            connection.close()
            return jsonify({"success" : "Assignment grade updated"})
        else:
            return jsonify({'error': 'Assignment not found'})
    except Exception as e:
        return jsonify({'error': str(e)})

###########################Reports###########################
@app.route('/courses_with_50plus', methods=['GET'])
def get_courses_with_50plus_students():
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        query = ("SELECT c.CourseID, CourseName, COUNT(StudentID) AS num_students FROM Enroll e " +
                "JOIN Course c on c.CourseID = e.CourseID " +
                "GROUP BY CourseID, CourseName " +
                "HAVING COUNT(StudentID) >= 50;")
        cursor.execute(query)
        result = cursor.fetchall()
        courses = []
        for CourseID, CourseName, StudentCount in result:
            courses.append({
                'CourseID': CourseID,
                'CourseName': CourseName,
                'StudentCount': StudentCount
            })
        cursor.close()
        connection.close()
        return jsonify(courses) 

    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/students_with_5plus_courses', methods=['GET'])
def get_students_with_5plus_courses():
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        query = ("SELECT StudentID, FirstName, LastName, COUNT(CourseID) AS num_courses FROM Enroll " + 
                "JOIN Account  on UserID = StudentID " +
                "GROUP BY StudentID, FirstName, LastName " +
                "HAVING COUNT(CourseID) >= 5;")
        cursor.execute(query)
        result = cursor.fetchall()
        students = []
        for StudentID, FirstName, LastName, CourseCount in result:
            students.append({
                'StudentID': StudentID,
                'FirstName': FirstName,
                'LastName': LastName,
                'CourseCount': CourseCount
            })
        cursor.close()
        connection.close()
        return jsonify(students) 

    except Exception as e:
        return jsonify({'error': str(e)})


@app.route('/lecturers_with_3plus_courses', methods=['GET'])
def get_lecturers_with_3plus_courses():
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        query = ("SELECT t.UserID, a.FirstName, a.LastName, COUNT(t.CourseID) AS num_courses FROM Teaches t " +
                "JOIN Course c on c.CourseID = t.CourseID " +
                "JOIN Account a on a.UserID = t.UserID " + 
                "GROUP BY t.UserID, a.FirstName, a.LastName " +
                "HAVING COUNT(t.CourseID) >= 3;")
        cursor.execute(query)
        result = cursor.fetchall()
        lecturers = []
        for LecID, FirstName, LastName, CourseCount in result:
            lecturers.append({
                'LecID': LecID,
                'FirstName': FirstName,
                'LastName': LastName,
                'CourseCount': CourseCount
            })
        cursor.close()
        connection.close()
        return jsonify(lecturers) 

    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/top10_courses', methods=['GET'])
def get_top10_courses():
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        query = ("SELECT c.CourseID, c.CourseName, c.CourseCode, COUNT(StudentID) AS num_students FROM Enroll e " +
                "JOIN Course c on c.CourseID = e.CourseID " + 
                "GROUP BY c.CourseID, c.CourseName, c.CourseCode " + 
                "ORDER BY num_students DESC LIMIT 10;")
        cursor.execute(query)
        result = cursor.fetchall()
        courses = []
        for CourseID, CourseName, CourseCode, StudentCount in result:
            courses.append({
                'CourseID': CourseID,
                'CourseName': CourseName,
                'CourseCode': CourseCode,
                'StudentCount': StudentCount
            })
        cursor.close()
        connection.close()
        return jsonify(courses) 

    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/top10_students', methods=['GET'])
def get_top10_students():
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        query = ("CREATE OR REPLACE VIEW CourseAverageGrades AS SELECT UserID, CourseID, AVG(Grade) AS avgGrade " +
                "FROM Assignment GROUP BY CourseID, UserID;")
        cursor.execute(query)

        query = ("CREATE OR REPLACE VIEW StudentOverallAverage AS SELECT UserID, AVG(avgGrade) AS overallAvg " +
                "FROM CourseAverageGrades GROUP BY UserID;")
        cursor.execute(query)

        query = ("SELECT sag.UserID, FirstName, LastName, overallAvg FROM StudentOverallAverage sag " +
                "JOIN Account ac ON sag.UserID = ac.UserID ORDER BY overallAvg DESC " +
                "LIMIT 10;")
        cursor.execute(query)     
        result = cursor.fetchall()
        students = []
        for UserID, FirstName, LastName, OverallAverage in result:
            students.append({
                'UserID': UserID,
                'FirstName': FirstName,
                'LastName': LastName,
                'OverallAverage': round(OverallAverage, 1)
            })
        cursor.close()
        connection.close()
        return jsonify(students) 

    except Exception as e:
        return jsonify({'error': str(e)})
