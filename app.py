from flask import Flask, render_template, request, url_for, redirect, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

##Database Models
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Student(db.Model):
    student_id = db.Column(db.String(80), primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(80), nullable=False)
    enrollments = db.relationship('Enrollment', backref = "enroller", lazy=True)
    personal_tasks = db.relationship('Personal_task', backref="taskmaster", lazy=True)
    reminders = db.relationship('Reminder', backref="worrier", lazy=True)
    def __repr__(self):
        return self

class Enrollment(db.Model):
    enroll_id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.String(80), db.ForeignKey('student.student_id'), nullable=False) #fk
    course_id = db.Column(db.Integer, db.ForeignKey('course.course_id'), nullable=False) #fk
    def __repr__(self):
        return self

class Personal_task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.String(80), db.ForeignKey('student.student_id'), nullable=False) #fk
    task_body = db.Column(db.String(240), nullable=False)
    def __repr__(self):
        return self

class Post(db.Model):
    post_id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('course.course_id'),nullable=False) #fk
    post_body = db.Column(db.String(80), nullable=False)
    def __repr__(self):
        return self

class Uni_task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('course.course_id'),nullable=False) #fk
    task_body = db.Column(db.String(100), nullable=False)
    task_date = db.Column(db.String(80), nullable=False)
    def __repr__(self):
        return self

class Course(db.Model):
    course_id = db.Column(db.Integer, primary_key=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.teacher_id') nullable=False) #fk
    course_title = db.Column(db.String(80), nullable=False)
    enrollments = db.relationship('Enrollment', backref = "enrolled", lazy=True)
    posts = db.relationship('Post', backref = "classroom", lazy=True)
    task_id = db.relationship('Uni_task', backref="coursework", lazy=True)
    def __repr__(self):
        return self

class Reminder(db.Model):
    reminder_id = db.Column(db.String(80), primary_key=True)
    student_id = db.Column(db.String(80), db.ForeignKey('student.student_id'), nullable=False) #fk
    reminder_date = db.Column(db.String(80), nullable=False)
    def __repr__(self):
        return self

class Teacher(db.Model):
    teacher_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(80), nullable=False)
    courses = db.relationship('Course', backref='lecturer', lazy=True)
    def __repr__(self):
        return self
## Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/home')
def home():
    #home page
    return redirect('/')

@app.route('/login')
def login():
    #login page
    return render_template('login.html')

@app.route('/register')
def register():
    #register page
    return render_template('register.html')

@app.route('/registerst',methods=['POST'])
def registerst():
    #student register logic
    if request.method == "POST":
        name = str(request.form['name'])
        id = str(request.form['id'])
        password = str(request.form['password'])
        password2 = str(request.form['password2'])
        email = str(request.form['email'])
        #email find
        #password hash
        #database push
        return redirect('login')


@app.route('/registertc',methods=['POST'])
def registertc():
    if request.method == "POST":
        name = str(request.form['name'])
        password = str(request.form['password'])
        password2 = str(request.form['password2'])
        email = str(request.form['email'])
        #password hash
        #database push
    #teacher register logic
    return redirect('login')

@app.route('/loginst',methods=['POST'])
def loginst():
    #student login logic
    if request.method == "POST":
        password = str(request.form['password'])
        email = str(request.form['email'])
        print(password+" "+email)
        return redirect('/')

@app.route('/logintc',methods=['POST'])
def logintc():
    if request.method == "POST":
        password = str(request.form['password'])
        email = str(request.form['email'])
    #teacher login logic
    pass

@app.route('/logoutst',methods=['POST'])
def logoutst():
    #student logout logic
    pass

@app.route('/logouttc',methods=['POST'])
def logouttc():
    #teacher logout logic
    pass
if __name__ == "__main__":
    app.run(debug=True)
