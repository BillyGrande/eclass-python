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
@app.route("/tests/<chapter>/<id>", methods=['GET', 'POST'])
def quiz(chapter=None, id=None):
    if id == None:
        return render_template('quiz_index.html', chapter=chapter, ids=["1","2","3"], length=len([1,2,3]), id=["1","2","3"][0])
    else:
        if session.get('logged_in'):
            if request.method == 'POST':
                #print(request.data.decode("utf-8"))
                #print(type(request.data.decode("utf-8")))
                session[id] = request.form['answer']
                ids = request.form['ids-list']
                ids = _urlencoded_to_list(ids)
            else:
                ids = ["1","2","3"]
            statement = select(Question).filter_by(id=int(id))
            question_obj = db_session.scalars(statement).all()
            question = question_obj[0]
            return render_template('quiz_questions.html', question=question, chapter=chapter, ids=ids, length=len([1,2,3]), id=id)
        else:
            return render_template('quiz_login.html', chapter=chapter)

#@app.route("/tests/<chapter>/retrieve")
def quiz_retrieve_questions(chapter=0):
    statement = select(Question).filter_by(chapter=chapter)
    ids = []
    for item in db_session.scalars(statement).all():
        ids.append(item.id)

    return ids




@app.route("/tests/<chapter>/<id>/next", methods=['GET', 'POST'])
def quiz_next(chapter=None, id=None):
    if request.method == 'POST':
        print(request.form['answer'])
        session[id] = request.form['answer']
        try:
            question_id= session.get('questions')[0]
            session['questions'] = session.get('questions').pop(0)
            next_id = session.get('questions').pop(0)
        except TypeError:
            question_id = session.get('questions')
        statement = select(Question).filter_by(id=question_id)
        question_obj = db_session.scalars(statement).all()
        question = question_obj
        return render_template('quiz_questions.html', question=question , next_id=next_id)




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


def _urlencoded_to_list(text):
    text = "%5B'1'%2C%20'2'%2C%20'3'%5D".replace("%5B","").replace("%5D","").replace("%2C%20",",").replace("'","")
    return text.split(",")