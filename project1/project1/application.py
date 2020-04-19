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
session=Session()
@app.route("/")
def index():
    return "project 1:TODO"
@app.route("/Register", methods = ['POST', 'GET'])
def form():
    db.create_all()
    if request.method =='POST':
        udata=data(request.form['Name'],request.form['email'],request.form['password'])
        userd=data.query.filter_by(email=request.form['email']).first()
        if userd is not None:
            variable='Email already exists!! try again'
            return render_template("registration.html",variable=variable)
        db.session.add(udata)
        db.session.commit()
        print("Sucesssfully Registered")
        variable1='Registration Successful'
        return render_template("registration.html",variable1=variable1)
    else:
        return render_template("registration.html")
@app.route('/admins')
def admin():
    usersinfo = data.query.all()
    return render_template("admins.html",admin = usersinfo)
 