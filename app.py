from flask import Flask, render_template, request, url_for, redirect, session, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.secret_key = 'secret'
bcrypt = Bcrypt()
##Database Models
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Student(db.Model):
    student_id = db.Column(db.String(80), primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(80), nullable=False)
    enrollments = db.relationship('Enrollment', backref = "student", lazy=True)
    personal_tasks = db.relationship('Personal_task', backref="student", lazy=True)
    reminders = db.relationship('Reminder', backref="student", lazy=True)
    def __repr__(self):
        return f"Student('{self.student_id}', '{self.email}', '{self.name}', '{self.password}')"

class Enrollment(db.Model):
    enroll_id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.String(80), db.ForeignKey('student.student_id'), nullable=False) #fk
    course_id = db.Column(db.Integer, db.ForeignKey('course.course_id'), nullable=False) #fk
    def __repr__(self):
        return f"Enrollment('{self.enroll_id}', '{self.course_id}', {self.student_id})"

class Personal_task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.String(80), db.ForeignKey('student.student_id'), nullable=False) #fk
    task_body = db.Column(db.String(240), nullable=False)
    def __repr__(self):
        return f"Personal_task('{self.task_id}', '{self.student_id}', '{self.task_body}')"

class Post(db.Model):
    post_id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('course.course_id'),nullable=False) #fk
    post_body = db.Column(db.String(1000), nullable=False)
    post_title = db.Column(db.String(80), nullable=False)
    post_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    def __repr__(self):
        return f"Post('{self.post_id}', '{self.course_id}', '{self.post_body}', '{self.post_title}')"

class Uni_task(db.Model):
    task_title = db.Column(db.String(100), nullable=False)
    task_id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('course.course_id'),nullable=False) #fk
    task_body = db.Column(db.String(1000), nullable=False)
    task_date = db.Column(db.DateTime, nullable=False)
    def __repr__(self):
        return f"Uni_Task('{self.task_title}','{self.task_id}', '{self.course_id}', '{self.task_body}', {self.task_date})"

class Course(db.Model):
    course_id = db.Column(db.String(10), primary_key=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.teacher_id'), nullable=False) #fk
    course_title = db.Column(db.String(80), nullable=False)
    enrollments = db.relationship('Enrollment', backref = "enrolled", lazy=True)
    posts = db.relationship('Post', backref = "classroom", lazy=True)
    task_id = db.relationship('Uni_task', backref="coursework", lazy=True)
    def __repr__(self):
        return f"Course('{self.teacher_id}', '{self.course_id}', '{self.course_title}')"

class Reminder(db.Model):
    reminder_id = db.Column(db.Integer, primary_key=True)
    reminder_body = db.Column(db.String(100), nullable=False)
    student_id = db.Column(db.String(80), db.ForeignKey('student.student_id'), nullable=False) #fk
    reminder_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    def __repr__(self):
        return f"Reminder('{self.reminder_id}', '{self.reminder_date}', {self.reminder_body})"

class Teacher(db.Model):
    teacher_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(80), nullable=False)
    courses = db.relationship('Course', backref='lecturer', lazy=True)
    def __repr__(self):
        return f"Teacher('{self.teacher_id}', '{self.name}', '{self.email}', '{self.password}')"

class Admin(db.Model):
    admin_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(80), nullable=False)
    def __repr__(self):
        return f"Admin('{self.admin_id}', '{self.name}', '{self.email}', '{self.password}')"

## Routes
@app.route('/')
def index():
    if 'student' in session:
        return redirect('/studentdash')
    if 'teacher' in session:
        return redirect('/teacherdash')
    if 'admin' in session:
        return redirect('/admin')
    return render_template('index.html')

@app.route('/home')
def home():
    if 'student' in session:
        return redirect('/studentdash')
    if 'teacher' in session:
        return redirect('/teacherdash')
    if 'admin' in session:
        return redirect('/admin')
    #home page
    return redirect('/')

@app.route('/login')
def login():
    #login page
    if 'student' in session:
        return redirect('/studentdash')
    if 'teacher' in session:
        return redirect('/teacherdash')
    if 'admin' in session:
        return redirect('/admin')
    return render_template('login.html')

@app.route('/register')
def register():
    #register page
    if 'student' in session:
        return redirect('/studentdash')
    if 'teacher' in session:
        return redirect('/teacherdash')
    if 'admin' in session:
        return redirect('/admin')
    return render_template('register.html')

@app.route('/registerst',methods=['POST','GET'])
def registerst():
    #student register logic
    errors = []
    if request.method == "POST":
        name = str(request.form['name'])
        student_id = str(request.form['studentId'])
        password = str(request.form['password'])
        password2 = str(request.form['password2'])
        email = str(request.form['email'])
        #email find
        check = Student.query.filter_by(email=email).first()
        check = Student.query.get(student_id)
        print(check)
        if not password or not name or not student_id or not password2 or not email:
            errors.append('Please fill in all the information')
        if check:
            errors.append('User Already Exists')
        if password != password2:
            errors.append('Passwords do not match')
        if len(password) < 6:
            errors.append('Passwords need to be at least 6 characters')
        if errors:
            return render_template('register.html', errors=errors)
        else:
            #password hash
            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
            print(hashed_password)
            #database push
            user = Student(email=email, student_id = student_id, password = hashed_password, name = name)
            db.session.add(user)
            db.session.commit()
            flash('You can now Login!', 'success_msg')
            return redirect('login')
    else:
        return redirect('/register')

@app.route('/registertc',methods=['POST', 'GET'])
def registertc():
    if request.method == "POST":
        name = str(request.form['name'])
        password = str(request.form['password'])
        password2 = str(request.form['password2'])
        email = str(request.form['email'])
        #checks
        errors= []
        check = Teacher.query.filter_by(email=email).first()
        print(check)
        if not password or not name or not password2 or not email:
            errors.append('Please fill in all the information')
        if check:
            errors.append('User Already Exists')
        if password != password2:
            errors.append('Passwords do not match')
        if len(password) < 6:
            errors.append('Passwords need to be at least 6 characters')
        if errors:
            return render_template('register.html', errors=errors)
        else:
            #password hash
            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
            print(hashed_password)
            #database push
            user = Teacher(email=email, password = hashed_password, name = name)
            db.session.add(user)
            db.session.commit()
            flash('You can now Login!', 'success_msg')
            return redirect('login')
    else:
        return redirect('/register')

@app.route('/studentdash')
def studentdash():
    if 'student' in session:
        student = session['student']
        todo = Personal_task.query.filter_by(student_id = student["student_id"])
        enrollments = Enrollment.query.filter_by(student_id = student["student_id"])
        tasks = {}
        mapuh = {}
        reminders = Reminder.query.filter_by(student_id = student["student_id"])
        for task in todo:
            tasks[task.task_id] = task.task_body
        for enrollment in enrollments:
            course = Course.query.filter_by(course_id = enrollment.course_id).first()
            if course:
                mapuh[course.course_id] = course.course_title
        return render_template('studentdash.html',student=student,tasks=tasks,reminders=reminders,mapuh=mapuh)
    else:
        return redirect('/login')

@app.route('/enrollcourse',methods=['POST','GET'])
def enrollcourse():
    error = ''
    if 'student' in session:
        if request.method == 'POST':
            course_id = str(request.form['course_id'])
            student_id = str(request.form['student_id'])
            student = session['student']
            c = Course.query.filter_by(course_id=course_id).first()
            if not c:
                error = "Course does not exist!"
                todo = Personal_task.query.filter_by(student_id = student_id)
                enrollments = Enrollment.query.filter_by(student_id = student_id)
                tasks = {}
                mapuh = {}
                reminders = Reminder.query.filter_by(student_id = student_id)
                for task in todo:
                    tasks[task.task_id] = task.task_body
                for enrollment in enrollments:
                    course = Course.query.filter_by(course_id = enrollment.course_id).first()
                    if course:
                        mapuh[course.course_id] = course.course_title
                return render_template('studentdash.html',student=student,tasks=tasks,reminders=reminders,mapuh=mapuh,error=error)
            else:
                e = Enrollment(course_id=course_id, student_id=student_id)
                db.session.add(e)
                db.session.commit()
            return redirect('/studentdash')
        else:
            return redirect('/studentdash')
    else:
        return redirect('/studentdash')

@app.route('/loginst',methods=['POST','GET'])
def loginst():
    #student login logic
    if request.method == "POST":
        password = str(request.form['password'])
        email = str(request.form['email'])
        if not email or not password:
            error = 'Please fill in all the data'
            return render_template('login',error=error)
        check = Student.query.filter_by(email=email).first()
        if check and bcrypt.check_password_hash(str(check.password), password):
            student = {
                'name' : check.name,
                'student_id' : check.student_id,
                'student_email' : check.email
            }
            session['student'] = student
            return redirect('/studentdash')
        else:
            error = 'Invalid Email or Password'
            return render_template('login.html',error=error)

@app.route('/admin')
def admin():
    if 'admin' in session:
        admin = session['admin']
        courses = Course.query.all();
        teachers = Teacher.query.all();
        students = Student.query.all();
        return render_template('admin.html', teachers = teachers, students = students, admin=admin, courses=courses)
    else:
        return render_template('adminlogin.html')

@app.route('/logoutadmin')
def logoutadmin():
    session.pop('admin',None)
    return redirect('/admin')


@app.route('/adminlogin', methods=['POST','GET'])
def adminlogin():
    if request.method == "POST":
        password = str(request.form['password'])
        email = str(request.form['email'])
        if not email or not password:
            error = 'Please fill in all the data'
            return render_template('adminlogin.html',error=error)
        check = Admin.query.filter_by(email=email).first()
        if check and (check.password == password):
            admin = {
                'name' : check.name,
                'id' : check.admin_id,
                'email' : check.email,
            }
            session['admin'] = admin
            return redirect('/admin')
        else:
            error = 'Invalid Email or Password'
            return render_template('adminlogin.html',error=error)

@app.route('/teacherdash')
def teacherdash():
    if 'teacher' in session:
        session.pop('course',None)
        teacher = session['teacher']
        courses = Course.query.filter_by(teacher_id = teacher["id"])
        mapuh = {}
        for course in courses:
            mapuh[course.course_id] = course.course_title
        return render_template('teacherdash.html',teacher=teacher, mapuh=mapuh)
    else:
        return redirect('/login')

@app.route('/get_course',methods=['POST','GET'])
def getcourse():
    if request.method == 'POST':
        session.pop('course',None)
        course_id = str(request.form['course_id'])
        course_title = str(request.form['course_title'])
        if 'teacher' in session:
            teacher = session['teacher']
            course = {
                'course_id':course_id,
                'course_title':course_title
            }
            session['course']=course
            return redirect('/course')
        if 'student' in session:
            student = session['student']
            course = {
                'course_id':course_id,
                'course_title':course_title
            }
            session['course']=course
            return redirect('/course')
        else:
            return redirect('/')
    else:
        return redirect('/')

@app.route('/addpost',methods=['POST','GET'])
def addpost():
    if request.method=='POST':
        course_id = str(request.form['course_id'])
        post_title = str(request.form['post_title'])
        post_body = str(request.form['post_body'])
        p = Post(course_id=course_id, post_body=post_body, post_title=post_title)
        db.session.add(p)
        db.session.commit()
        return redirect('/course')
    return redirect('/course')

@app.route('/addtask',methods=['POST','GET'])
def addtask():
    if request.method=='POST':
        if 'student' in session:
            student = session['student']
            task_body = str(request.form['task_body'])
            if task_body == '':
                return redirect('/Todolist')
            student_id = student['student_id']
            t = Personal_task(student_id=student_id,task_body=task_body)
            db.session.add(t)
            db.session.commit()
            return redirect('/Todolist')
        else:
            return redirect('/')
    else:
        return redirect('/')

@app.route('/deltask',methods=['POST','GET'])
def deltask():
    if request.method=='POST':
        if 'student' in session:
            student = session['student']
            task_id = str(request.form['task_id'])
            student_id = student['student_id']
            t = Personal_task.query.filter_by(task_id=task_id).first()
            db.session.delete(t)
            db.session.commit()
            return redirect('/Todolist')
        else:
            return redirect('/')


@app.route('/addreminder',methods=['POST','GET'])
def addreminder():
    if request.method=='POST':
        if 'student' in session:
            student = session['student']
            reminder_body = str(request.form['reminder_body'])
            reminder_date = datetime.strptime(request.form['reminder_date'], '%Y-%m-%d')
            if reminder_body == '':
                return redirect('/Reminders')
            student_id = student['student_id']
            r = Reminder(student_id=student_id,reminder_body=reminder_body, reminder_date=reminder_date)
            db.session.add(r)
            db.session.commit()
            return redirect('/Reminders')
        else:
            return redirect('/')
    else:
        return redirect('/')

@app.route('/delrem',methods=['POST','GET'])
def delrem():
    if request.method=='POST':
        if 'student' in session:
            student = session['student']
            reminder_id = str(request.form['reminder_id'])
            student_id = student['student_id']
            r = Reminder.query.filter_by(reminder_id=reminder_id).first()
            db.session.delete(r)
            db.session.commit()
            return redirect('/Reminders')
        else:
            return redirect('/')

@app.route('/addassignment',methods=['POST','GET'])
def addassignment():
    if request.method=='POST':
        course_id = str(request.form['course_id'])
        task_title = str(request.form['task_title'])
        task_body = str(request.form['task_body'])
        task_date = datetime.strptime(request.form['task_date'], '%Y-%m-%d')
        print(course_id)
        print(task_date)
        u_t = Uni_task(course_id=course_id, task_body=task_body, task_title=task_title, task_date = task_date)
        db.session.add(u_t)
        db.session.commit()
        return redirect('/course')
    return redirect('/course')



@app.route('/addcourse',methods=['POST','GET'])
def addcourse():
    if 'teacher' in session:
        if request.method == 'POST':
            course_id = str(request.form['course_id'])
            course_name = str(request.form['course_name'])
            teacher_id = str(request.form['teacher_id'])
            course = Course.query.filter_by(course_id=course_id)
            if not course:
                c = Course(course_id=course_id, course_title=course_name, teacher_id=teacher_id)
                db.session.add(c)
                db.session.commit()
                return redirect('/teacherdash')
            else:
                error = 'Course already exists'
                session.pop('course',None)
                teacher = session['teacher']
                courses = Course.query.filter_by(teacher_id = teacher["id"])
                mapuh = {}
                for course in courses:
                    mapuh[course.course_id] = course.course_title
                return render_template('teacherdash.html',teacher=teacher, mapuh=mapuh, error=error)

        else:
            return redirect('/teacherdash')
    else:
        return redirect('/login')


@app.route('/delcourse',methods=['POST','GET'])
def delcourse():
    if request.method == "POST":
        course_id = str(request.form['course_id'])
        tasks = Uni_task.query.filter_by(course_id=course_id).all()
        for task in tasks:
            db.session.delete(task)
            db.session.commit()
        posts = Post.query.filter_by(course_id=course_id).all()
        for post in posts:
            db.session.delete(post)
            db.session.commit()
        c = Course.query.filter_by(course_id=course_id).first()
        db.session.delete(c)
        db.session.commit()
        return redirect('/')
    else:
        return redirect('/')

@app.route('/delstudent',methods=['POST','GET'])
def delstudent():
    if request.method == "POST":
        student_id = str(request.form['student_id'])
        todos = Personal_task.query.filter_by(student_id=student_id).all()
        for task in todos:
            db.session.delete(task)
            db.session.commit()
        reminders = Reminder.query.filter_by(student_id=student_id).all()
        for task in reminders:
            db.session.delete(task)
            db.session.commit()
        enrollments = Enrollment.query.filter_by(student_id=student_id).all()
        for entry in enrollments:
            db.session.delete(entry)
            db.session.commit()
        s = Student.query.filter_by(student_id=student_id).first()
        db.session.delete(s)
        db.session.commit()
        return redirect('/')
    else:
        return redirect('/')

@app.route('/delteacher',methods=['POST','GET'])
def delteacher():
    if request.method == "POST":
        teacher_id = str(request.form['teacher_id'])
        courses = Course.query.filter_by(teacher_id=teacher_id).all()
        for course in courses:
            db.session.delete(course)
            db.session.commit()
        t = Teacher.query.filter_by(teacher_id=teacher_id).first()
        db.session.delete(t)
        db.session.commit()
        return redirect('/')
    else:
        return redirect('/')

@app.route('/editcourse', methods=['POST','GET'])
def editcourse():
    if request.method == "POST":
        course_id = str(request.form['course_id'])
        course_name = str(request.form['course_name'])
        course = Course.query.filter_by(course_id=course_id).first()
        course.course_title = course_name
        db.session.commit()
        return redirect('/')
    else:
        return redirect('/')

@app.route('/editteacher', methods=['POST','GET'])
def editteacher():
    if request.method == "POST":
        teacher_id = str(request.form['teacher_id'])
        teacher_name = str(request.form['teacher_name'])
        email = str(request.form['email'])
        tc = Teacher.query.filter_by(teacher_id=teacher_id).first()
        if email != '':
            tc.email = email
        if teacher_name != '':
            tc.name = teacher_name
        db.session.commit()
        return redirect('/')
    else:
        return redirect('/')

@app.route('/editstudent', methods=['POST','GET'])
def editstudent():
    if request.method == "POST":
        student_id = str(request.form['student_id'])
        name = str(request.form['name'])
        email = str(request.form['email'])
        tc = Student.query.filter_by(student_id=student_id).first()
        if email != '':
            tc.email = email
        if name != '':
            tc.name = name
        db.session.commit()
        return redirect('/')
    else:
        return redirect('/')

@app.route('/course',methods=['POST','GET'])
def course():
    if 'teacher' in session and 'course' in session:
        course = session['course']
        c = Course.query.filter_by(course_id=course['course_id']).all()
        posts = c[0].posts
        uni_tasks = c[0].task_id
        print(uni_tasks)
        return render_template('course.html',posts=posts, course=course, uni_tasks = uni_tasks)
    if 'student' in session and 'course' in session:
        course = session['course']
        c = Course.query.filter_by(course_id=course['course_id']).all()
        posts = c[0].posts
        uni_tasks = c[0].task_id
        print(uni_tasks)
        return render_template('coursest.html',posts=posts, course=course, uni_tasks = uni_tasks)
    else:
        return redirect('/login')

@app.route('/logintc',methods=['POST','GET'])
def logintc():
    if request.method == "POST":
        password = str(request.form['password'])
        email = str(request.form['email'])
        if not email or not password:
            error = 'Please fill in all the data'
            return render_template('login',error=error)
        check = Teacher.query.filter_by(email=email).first()
        if check and bcrypt.check_password_hash(str(check.password), password):
            mapuh = {}
            for course in check.courses:
                mapuh[course.course_id] = course.course_title
            teacher = {
                'name' : check.name,
                'id' : check.teacher_id,
                'email' : check.email,
                'courses' : mapuh
            }
            session['teacher'] = teacher
            return redirect('/teacherdash')
        else:
            error = 'Invalid Email or Password'
            return render_template('login.html',error=error)

@app.route('/Todolist')
def Todolist():
    if 'student' in session:
        student = session['student']
        tasks = Personal_task.query.filter_by(student_id=student['student_id']).all()
        return render_template('todo.html',student=student, tasks=tasks)
    else:
        return redirect('/login')

@app.route('/Reminders')
def Reminders():
    if 'student' in session:
        student = session['student']
        reminders = Reminder.query.filter_by(student_id=student['student_id']).all()
        return render_template('reminders.html',student=student, reminders=reminders)
    else:
        return redirect('/login')

@app.route('/logoutst')
def logoutst():
    #student logout logic
    session.pop('student',None)
    return redirect('/login')

@app.route('/logouttc')
def logouttc():
    #teacher logout logic
    session.pop('teacher',None)
    return redirect('/login')

if __name__ == "__main__":
    app.run(debug=True)
