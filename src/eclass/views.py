from eclass import app
from flask import render_template, session, request,redirect,url_for
from eclass.db.db import db_session
from eclass.db.models import Question
from sqlalchemy import select
from flask import session
fr

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
        statement = select(Question).filter_by(chapter=id)
        user_obj = db_session.scalars(statement).all()
        db_session.query()
        return render_template('quiz_questions.html', question=user_obj[0])
    
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('index'))
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
    return redirect(url_for('index'))