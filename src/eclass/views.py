from eclass import app
from flask import render_template, session, request,redirect,url_for
from eclass.db.db import db_session
from eclass.db.models import Question
from sqlalchemy import select
from flask import session
import os


secret_path = os.path.dirname(os.path.realpath(__file__)) +"/.secret"
f = open(secret_path, "r")
app.secret_key = f.readline()
f.close()


@app.route("/")
def hello_world():
    return render_template('hello.html')

@app.route("/hello/<message>")
def hello(message=None):
    return render_template('hello.html',message=message)

@app.route("/lessons/welcome")
def welcome():
    return render_template('lessons_welcome.html')

@app.route("/tests/welcome")
def test_welcome():
    return render_template('tests_welcome.html')

@app.route("/tests/<chapter>")
@app.route("/tests/<chapter>/<id>")
def quiz(chapter=None, id=None):
    if id == None:
        return render_template('quiz_index.html', chapter=chapter)
    else:
        if session.get('logged_in'):
            statement = select(Question).filter_by(chapter=id)
            user_obj = db_session.scalars(statement).all()
            db_session.query()
            return render_template('quiz_questions.html', question=user_obj[0])
        else:
            return render_template('quiz_login.html', chapter=chapter)


@app.route("/tests/<chapter>/<id>/next")
def quiz_next(chapter=None, id=None):
    if id == None:
        return render_template('quiz_index.html', chapter=chapter)
    else:
        if session.get('logged_in'):
            statement = select(Question).filter_by(chapter=id)
            user_obj = db_session.scalars(statement).all()
            db_session.query()
            return render_template('quiz_questions.html', question=user_obj[0])
        else:
            return render_template('quiz_login.html', chapter=chapter)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        session['logged_in'] = True
        return redirect(url_for('welcome'))
    return '''
        <form method="post">
            <p><input type=text name=username>
            <p><input type=submit value=Login>
        </form>
        '''

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    session.pop('logged_in', None)
    return redirect(url_for('welcome'))