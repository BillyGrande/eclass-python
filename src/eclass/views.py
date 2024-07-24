from eclass import app
from flask import render_template
from eclass.db.db import db_session
from eclass.db.models import Question
from sqlalchemy import select

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
def quiz_index(chapter=0):
    return render_template('quiz_index.html', chapter=chapter)

@app.route("/tests/<chapter>/<id>")
def quiz_quetion(chapter=None, id=0):
    statement = select(Question).filter_by(chapter=id)
    user_obj = db_session.scalars(statement).all()
    db_session.query()
    return render_template('quiz_questions.html', question=user_obj[0])