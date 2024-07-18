from eclass import app
from flask import render_template

@app.route("/")
def hello_world():
    return render_template('hello.html')

@app.route("/hello/<message>")
def hello(message=None):
    return render_template('hello.html',message=message)
