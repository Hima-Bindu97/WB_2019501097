import os

from model import *
from flask import Flask, session,render_template, request,redirect
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import logging

logging.basicConfig(level=logging.DEBUG)
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
    if session.get("email") is None:
        return render_template("registration.html",text="please fill the details")
    return render_template("login.html",text="welcome to home page"+session.get("email"))
@app.route("/Register", methods = ['POST', 'GET'])
def form():
    db.create_all()
    if request.method =='POST':
        udata=data(request.form['Name'],request.form['email'],request.form['password'])
        userd=data.query.filter_by(email=request.form['email'])
        if userd is not None:
            return render_template("registration.html")
        session.add(udata)
        session.commit()
        print("Sucesssfully Registered")
        variable1='Registration Successful'
        return render_template("registration.html",variable1=variable1)
    else:
        return render_template("registration.html")
@app.route('/admins')
def admin():
    usersinfo = data.query.all()
    return render_template("admins.html",admin = usersinfo)
@app.route('/auth', methods=['POST','GET'])
def auth():
    user=data.query.filter_by(email=request.form['email']).first()
    if user is not None:
        if request.form['password']==user.password:
            session['email'] = request.form['email']
            session['Name']=request.form['Name']
            print(session)
            return redirect('/home')
        else:
            variable1 = "Wrong Credentials"
            return render_template("registration.html", variable1 = variable1)
    else:
        print("You are not a registered user. Please first register to login")
        variable1 = "Error: You are not a registered user. Please first register to login"
        return render_template("registration.html", variable1 = variable1)
@app.route('/home')
def home():
        user=session['email']
        return render_template("login.html")

@app.route('/logout')
def logout():
    user=session['email']
    session.clear()
    variable1 = "Logged Out"
    return render_template("registration.html", variable1 = variable1)