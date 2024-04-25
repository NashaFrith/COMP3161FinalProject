from flask import Flask, request, make_response, jsonify
import mysql.connector


app = Flask(__name__)
app.json.sort_keys = False
def get_db_connection():
    connection = mysql.connector.connect(
    host = 'localhost',
    user= 'comp3161',
    password = 'password123!',
    database = 'uwi2')
    return connection


###########################Events###########################
@app.route('/events', methods=['POST'])
def create_event():
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        content = request.json
        EventID = content['EventID']
        CourseID = content['CourseID']
        EventName = content['EventName']
        Duedate = content['Duedate']
        query = "INSERT INTO Event (EventID, CourseID, EventName, Duedate) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (EventID, CourseID, EventName, Duedate))
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
        ForumID = content['ForumID']
        CourseID = content['CourseID']
        ForumName = content['ForumName']
        query = "INSERT INTO Forum (ForumID, CourseID, ForumName) VALUES (%s, %s, %s)"
        cursor.execute(query, (ForumID, CourseID, ForumName))
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
        ThreadID = content['ThreadID']
        ForumID = content['ForumID']
        Title = content['Title']
        Body = content['Body']
        created_by = content['created_by']
        query = "INSERT INTO Thread (ThreadID, ForumID, Title, Body, created_by) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(query, (ThreadID, ForumID, Title, Body, created_by))
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
        ReplyID = content['ReplyID']
        ReplyBody = content['ReplyBody']
        created_by = content['created_by']
        query = "INSERT INTO Reply (MainThreadID, ReplyID, ReplyBody, created_by) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (MainThreadID, ReplyID,ReplyBody, created_by))
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
        query = f"SELECT * FROM Reply WHERE MainThreadID = {main_thread_id}"
        cursor.execute(query)
        result = cursor.fetchall()

        replies = []
        for MainThreadID, ReplyID, ReplyBody, created_by in result:
            replies.append({
                'MainThreadID': MainThreadID,
                'ReplyID': ReplyID,                
                'ReplyBody': ReplyBody,
                'created_by': created_by
            })
        cursor.close()
        connection.close()
        return jsonify(replies) 

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
        for CourseID, SectionID in result:
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
        SectionID = content['SectionID']        
        query = "INSERT INTO Section (CourseID, SectionID) VALUES (%s, %s)"
        cursor.execute(query, (CourseID, SectionID))
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
        ItemID = content['ItemID']
        title = content['title']
        itype = content['itype']
        query = "INSERT INTO Item (SectionID, ItemID, title, itype) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (SectionID, ItemID, title, itype))
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
        for CourseID, AssID, StudentID, Grade, date_submit in result:
            assignments.append({
                'CourseID': CourseID,
                'AssID': AssID,
                'StudentID': StudentID,
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
        AssID = content['AssID']
        StudentID = content['StudentID']
        CourseID = content['CourseID']
        date_submit = content['date_submit']
        query = "INSERT INTO Assignment (AssID, StudentID, CourseID, date_submit) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (AssID, StudentID, CourseID, date_submit))
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
            cursor.execute(f"UPDATE Assignment SET Grade='{Grade}' WHERE AssID={assignment_id}")
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
        query = ("CREATE OR REPLACE VIEW CourseAverageGrades AS SELECT StudentID, CourseID, AVG(Grade) AS avgGrade " +
                "FROM Assignment GROUP BY CourseID, StudentID;")
        cursor.execute(query)

        query = ("CREATE OR REPLACE VIEW StudentOverallAverage AS SELECT StudentID, AVG(avgGrade) AS overallAvg " +
                "FROM CourseAverageGrades GROUP BY StudentID;")
        cursor.execute(query)

        query = ("SELECT StudentID, FirstName, LastName, overallAvg FROM StudentOverallAverage " +
                "JOIN Account ON StudentID = UserID ORDER BY overallAvg DESC " +
                "LIMIT 10;")
        cursor.execute(query)     
        result = cursor.fetchall()
        students = []
        for StudentID, FirstName, LastName, OverallAverage in result:
            students.append({
                'StudentID': StudentID,
                'FirstName': FirstName,
                'LastName': LastName,
                'OverallAverage': round(OverallAverage, 1)
            })
        cursor.close()
        connection.close()
        return jsonify(students) 

    except Exception as e:
        return jsonify({'error': str(e)})