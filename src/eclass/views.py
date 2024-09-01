from eclass import app
from flask import render_template, session, request,redirect,url_for
from eclass.db.db import db_session
from eclass.db.models import Question, Result
from sqlalchemy import select
from sqlalchemy.sql import func
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

@app.route("/lessons/0")
def welcome_0():
    return render_template('lessons_0.html')

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
                if session.get(id, default=False):
                    answer = session.get(id)
            else:
                ids = session.get('ids')
                if request.args.get('back', default=False):
                    answer = session.get(id)
            statement = select(Question).filter_by(id=int(id))
            question_obj = db_session.scalars(statement).all()
            question = question_obj[0]
            return render_template('quiz_questions.html', question=question, chapter=chapter, ids=ids, 
            length=len(ids), id=id, answer=answer)
        else:
            return render_template('quiz_login.html', chapter=chapter)

# ["1","2","3"].join("|").split("|")

@app.route("/tests/<chapter>/<id>/finish", methods=['POST'])
def quiz_finish(chapter=None, id=None):
        ids = session.get('ids')
        session[id] = request.form['answer']
        results = []
        n = 0
        correct_n = 0
        correct_ids = []
        for i in ids:
            n = n + 1
            statement = select(Question).filter_by(id=int(i))
            question_obj = db_session.scalars(statement).first()
            given_answer = session.get(i)
            correct_answer = question_obj.correct 
            print(question_obj.question)
            print(f"User gave: {given_answer}, correct answer is {correct_answer}")
            if correct_answer == given_answer:
                result = True
                correct_n = correct_n + 1
                correct_ids.append(i)
            else:
                result = False
            results.append([question_obj.question, getattr(question_obj, correct_answer), 
            getattr(question_obj, given_answer), result, n])
        if correct_n == 0:
            percentage = 0
        else:
            percentage = 100 * correct_n / n
        r = Result(username=session.get('username'),chapter=chapter,score=percentage,answers_total=n,
                        answers_right=n,ids="|".join(ids),ids_correct="|".join(correct_ids))
        db_session.add(r)
        db_session.commit()
        for id in ids:
            session.pop(id, None)
        return render_template('quiz_finish.html', chapter=chapter, results=results, percentage=int(percentage)) 

@app.route("/tests/static/finish")
def static_quiz_finish(chapter=None, id=None):
    return render_template('quiz_finish_static.html', chapter=0)


@app.route('/profile')
def profile(username=None):
    if session.get('logged_in'):
        username = username=session.get('username')
        chapters = [0, 1]
        scores = {}
        average = {}
        attempts = {}
        for chapter in chapters:
            #best_score_query = db_session.query(func.max(Result.score)).filter_by(chapter=chapter,username=username)
            best_score_query = select(func.max(Result.score)).filter_by(chapter=chapter,username=username)
            total_attempts_query = select(func.count(Result.score)).filter_by(chapter=chapter,username=username)
            sum_score_qurey = select(func.sum(Result.score)).filter_by(chapter=chapter,username=username)
            best_score = db_session.scalars(best_score_query).one()
            total_attempts = db_session.scalars(total_attempts_query).one()
            average_score = db_session.scalar(sum_score_qurey)
            scores[chapter] = best_score if best_score != None else 0
            attempts[chapter] = total_attempts
            average[chapter] = int(average_score / total_attempts) if total_attempts > 0 else 0
        print(scores)
        return render_template('profile.html', username=username, scores=scores, attempts=attempts, average=average)
    else:
        return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        session['logged_in'] = True
        if request.args.get('previous', default=False):
            if request.args.get('previous', default=False) == "quiz":
                chapter = request.args.get('chapter', default=False)
                return redirect(url_for('quiz', chapter=chapter))
        return redirect(url_for('welcome'))
    if session.get('logged_in'):
        return redirect(url_for('profile'))
    else:
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