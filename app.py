from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash, make_response
from flask_mysqldb import MySQL
from functools import wraps
import mysql.connector
import MySQLdb.cursors
from datetime import date
import bcrypt

app = Flask(__name__)
   
app.secret_key = 'abcd21234455'  
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'comp3161'
app.config['MYSQL_PASSWORD'] = 'password123!'
app.config['MYSQL_DB'] = 'uwi'
  
mysql = MySQL(app)

def login_required(route_function):
    @wraps(route_function)
    def decorated_function(*args, **kwargs):
        if 'loggedin' not in session:
            return redirect(url_for('login'))
        return route_function(*args, **kwargs)
    return decorated_function

def hash_password(password):
    """Hashes the password using bcrypt."""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def verify_password(plain_password, hashed_password):
    """Verifies if the plain password matches the hashed password."""
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password)

@app.route('/')
@app.route('/login', methods =['GET', 'POST'])
def login():
    mesage = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']        
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM Account WHERE UserID = % s AND Pass = % s', (username, password, ))
        user = cursor.fetchone()
        if user:
            session['loggedin'] = True
            session['username'] = user['UserID']
            session['fname'] = user['FirstName']
            session['lname'] = user['LastName']
            session['role'] = user['uType']
            mesage = 'Logged in successfully !'            
            if user['uType'] == 'Admin':
                return redirect(url_for('admin_dashboard'))
            elif user['uType'] == 'Lecturer':
                return redirect(url_for('lecturer_dashboard'))
            elif user['uType'] == 'Student':
                return redirect(url_for('student_dashboard'))
            else:
                mesage = 'Please enter correct username / password !'
    return render_template('login.html', mesage = mesage)

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('UserID', None)
    session.pop('FirstName', None)
    session.pop('LastName', None)
    session.pop('uType', None)
    return redirect(url_for('login'))

@app.route('/create_account', methods=['GET', 'POST'])
def create_account():
    if request.method == 'POST':
        fname = request.form['fname']
        lname = request.form['lname']
        user_name = request.form['userid']
        pword = request.form['password']
        role = request.form['role']


        # Insert user into Account table
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("INSERT INTO Account (FirstName, LastName, UserID, Pass, uType) VALUES (%s, %s, %s, %s, %s)",
                           (fname, lname, user_name, pword, role))
        mysql.connection.commit()

        # Get the user_id of the newly inserted user
        user_id = cursor.lastrowid

        # Redirect to respective dashboard based on role
        if role == 'Admin':
            return redirect(url_for('admin_dashboard'))  # Redirect to admin dashboard
        elif role == 'Lecturer':
            return redirect(url_for('lecturer_dashboard'))  # Redirect to lecturer dashboard
        elif role == 'Student':
            return redirect(url_for('student_dashboard'))  # Redirect to student dashboard

        flash('User added successfully', 'success')
        return redirect(url_for('login'))
    return render_template('create_account.html', message=None)
            
@app.route('/admin/dashboard')
@login_required
def admin_dashboard():
    if 'username' in session and session['role'] == 'Admin':
        return render_template('admin_dashboard.html')
    else:
        return redirect(url_for('login'))

@app.route('/lecturer/dashboard')
@login_required
def lecturer_dashboard():
    if 'username' in session and session['role'] == 'Lecturer':
        return render_template('lecturer_dashboard.html')
    else:
        return redirect(url_for('login'))

@app.route('/student/dashboard')
@login_required
def student_dashboard():
    if 'username' in session and session['role'] == 'Student':
        return render_template('student_dashboard.html')
    else:
        return redirect(url_for('login'))

########################### Course Content ###########################
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

########################### Events ###########################
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

########################### Forums ###########################
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

########################### Threads ###########################
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

########################### Replies ###########################
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
        query = "INSERT INTO Replies (MainThreadID, ReplyID, ReplyBody, created_by) VALUES (%s, %s, %s, %s)"
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

########################### Assignments ###########################
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
        AssID = content['AssID']
        UserID = content['UserID']
        CourseID = content['CourseID']
        date_submit = content['date_submit']
        query = "INSERT INTO Assignment (AssID, UserID, CourseID, date_submit) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (AssID, UserID, CourseID, date_submit))
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

########################### Reports ###########################
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
    
if __name__ == "__main__":
    app.run(debug=True)