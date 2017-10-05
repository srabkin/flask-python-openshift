from flask import Flask, request
from flask import Flask, request, redirect, render_template, session, abort, flash
from flask_sqlalchemy import SQLAlchemy
from flask_sqlalchemy import orm
from flaskrun import flaskrun

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    password = db.Column(db.String)

    def __init__(self, username, password):
        self.username = username
        self.password = password

db.create_all()

def do_admin_login():
    user = User("admin","password")
    POST_USERNAME = str(request.form['username'])
    POST_PASSWORD = str(request.form['password'])

    query = db.session.query(User).filter(User.username.in_([POST_USERNAME]),
                                           User.password.in_([POST_PASSWORD]))
    result = query.first()
    if result:
        session['logged_in'] = True
    else:
        flash('wrong password!')

def add_user():
    user = User(request.form["username"],request.form["password"])
    db.session.add(user)
    db.session.commit()

user = User("admin" , "password")
db.session.add(user)
db.session.commit()
