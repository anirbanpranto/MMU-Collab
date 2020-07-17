from flask import Flask, render_template, request, url_for, redirect, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

##Database Models
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class student(db.Model):
    student_id = db.Column(db.String(80), primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(80), nullable=False)
    def __repr__(self):
        return self

class teacher(db.Model):
    teacher_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(80), nullable=False)
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
