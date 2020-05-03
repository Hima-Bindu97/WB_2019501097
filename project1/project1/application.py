import os

from model import *
from flask import Flask, session,render_template, request,redirect
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)
# Check for environment variable
if not os.getenv("DATABASE_URL"):
   raise RuntimeError("DATABASE_URL is not set")

app.config['SQLALCHEMY_DATABASE_URI'] =os.getenv("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Configure session to use filesystem      
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
db.init_app(app)
# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
Session = scoped_session(sessionmaker(bind=engine))
# session=db()
@app.route("/")
def index():
    if session.get("Name") is not None:
        return render_template("login.html",text="please fill the details")
    return redirect("/Register")
@app.route("/Register", methods = ['POST', 'GET'])
def form():
    if session.get("Name") is not None:
        return render_template("login.html",text="welcome to home page"+session.get("Name"))
    db.create_all()
    if request.method =='GET':
        return render_template("registration.html")
    else:
        udata=data(request.form['Name'],request.form['email'],request.form['password'])
        userd=data.query.filter_by(email=request.form['email'])
        if userd is not None:
            return render_template("registration.html")
        session.add(udata)
        session.commit()
        print("Sucesssfully Registered")
        variable1='Registration Successful'
        return render_template("registration.html",variable1=variable1)
        
@app.route('/admins',methods=['GET'])
def admin():
    usersinfo = data.query.all()
    return render_template("admins.html",admin = usersinfo)
@app.route('/auth', methods=['POST'])
def auth():
    if request.method=="POST":
        user=data.query.filter_by(email=request.form['email']).first()
        if user is not None:
            if request.form['password']==user.password:
                session['email'] = request.form['email']
                session['Name']=request.form['Name']
                print(session)
                return redirect('login.html')
            else:
                variable1 = "Wrong Credentials"
                return render_template("registration.html", variable1 = variable1)
        else:
            print("You are not a registered user. Please first register to login")
            variable1 = "Error: You are not a registered user. Please first register to login"
            return render_template("registration.html", variable1 = variable1)
@app.route('/home')
def home():
        return render_template("login.html")

@app.route('/logout',methods=["GET"])
def logout():
    session.clear()
    variable1 = "Logged Out"
    return render_template("registration.html", variable1 = variable1)