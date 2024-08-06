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
        session['ids'] = ids=["1","2","3"]
        return render_template('quiz_index.html', chapter=chapter, ids=["1","2","3"], length=len([1,2,3]), id=["1","2","3"][0])
    else:
        answer = None
        if session.get('logged_in'):
            if request.method == 'POST':
                answer_id = request.form['answer_id']
                session[answer_id] = request.form['answer']
                ids = session.get('ids')
            else:
                ids = session.get('ids')
                if request.args.get('back', default="No", type=str) == "Yes":
                    answer = session.get(id)
            statement = select(Question).filter_by(id=int(id))
            question_obj = db_session.scalars(statement).all()
            question = question_obj[0]
            return render_template('quiz_questions.html', question=question, chapter=chapter, ids=ids, length=len(ids), id=id, answer=answer)
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
    print("URLENCODED")
    print(text)
    text = text.replace("%5B","").replace("%5D","").replace("%2C%20",",").replace("'","")
    #text = text.replace("[","").replace("]","").replace("%20","")
    print(text.split(","))
    return text.split(",")