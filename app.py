import os

from flask import Flask, request
from flask import render_template
from flask import redirect, session
from flask_sqlalchemy import SQLAlchemy
from flaskrun import flaskrun
import userlogin

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    done = db.Column(db.Boolean, default=False)

    def __init__(self, content):
        self.content = content
        self.done = False

    def __repr__(self):
        return '<Content %s>' % self.content


db.create_all()


@app.route('/')
def tasks_list():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        tasks = Task.query.all()
        return render_template('list.html', tasks=tasks)


@app.route('/task', methods=['POST'])
def add_task():
    content = request.form['content']
    if not content:
        return 'Error'

    task = Task(content)
    db.session.add(task)
    db.session.commit()
    return redirect('/')


@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    task = Task.query.get(task_id)
    if not task:
        return redirect('/')

    db.session.delete(task)
    db.session.commit()
    return redirect('/')


@app.route('/done/<int:task_id>')
def resolve_task(task_id):
    task = Task.query.get(task_id)

    if not task:
        return redirect('/')
    if task.done:
        task.done = False
    else:
        task.done = True

    db.session.commit()
    return redirect('/')

@app.route('/login', methods=['POST'])
def do_login():
    userlogin.do_admin_login()
    return redirect('/')

@app.route('/logout')
def do_logout():
    session['logged_in'] = False
    return redirect('/')

@app.route('/adduser')
def add_user():
    return render_template('adduser.html')


@app.route('/submituser', methods=['POST'])
def submit_user():
    userlogin.add_user()
    return redirect('/')

if __name__ == '__main__':
    app.secret_key = os.urandom(12)
    flaskrun(app)
