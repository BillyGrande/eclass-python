from eclass.db.db import db_session
from eclass.db.models import User, Question
from eclass.db.db import init_db
import sqlalchemy as sqla
from sqlalchemy.exc import OperationalError
from sqlalchemy import text


def _add_users():
   users = [
      User("testuser", 'test@localhost'),
      User("billy", 'billy@localhost')
   ]
   for u in users:
      db_session.add(u)

def _add_questions():
   questions = [
      Question(0, "When python first appeared?", "Late 1980", "In 1991", "At 00s", "Designed 1999 and developed 2002", "a1"),
      Question(0, "Which programming paradigms python supprots?" "Object oriented", "Procedural and Object Oriented", "Functional", "Object oriented, procedural, functional", "a4"),
      Question(0, "What is the type system of Python?", "Static Typing", "Hybrid  Typing", "Dynamic Typing", "Int", "a3" ),
      Question(0, "How to initialiaze a variable?", "int x := 0", "var x = 0", "x = 0", "x := 0 ", "a3" ),
      Question(0, "What print('Hello') does?", "It prints Hello in output", "It prints a hello page, if we have a printer availalbe", "We don't know. We have to define print() first", "All of the above", "a1" ),
      Question(1, "What can't be an integer?", "-0", "1.0", "0", "9", "a2"),
      Question(1, "Which of these is a float?", "3.14" "-0.0", "3/4", "All of the above", "a4"),
      Question(1, "In what type of quotes can we enclose a string?", "Single quote", "Double quotes", "Triple quotes", "All of the above", "a4" ),
      Question(1, "my_message = 'Answer' and x = my_message[2]. What x will be?", "s", "n", "A", "e", "a1"),
      Question(1, "[1,2,3] is . What x will be?", "s", "n", "A", "e", "a1"),
      Question(1, "my_list = [1,2,3,'hello']. How to get the character 'h'", "my_list[-1][-1]", "my_list[4][1]", "my_list[4][0]", "my_list[-1][0]", "a4"),
      Question(1, "Are tuples changeable?", "Yes", "No", "No but we can use append", "Yes and we can use append", "a1"),
      Question(1, "In which sequence this will evaluate? range(10, 2, -2)", "(2,4,6,8)", "(10,8,6,4)", "(2,4,6,8,10)", "(4,6,8,10)", "a2"),
      Question(1, "my_dict = {'Tutorial':'Python', 0: 1, '0':0}. What it the value of my_dict[0]?", "Tutorial':'Python", "Tutorial", "1", "0", "a4"),
      Question(2, "", "", "", "", "", ""),
      Question(2, "", "", "", "", "", ""),
      Question(2, "", "", "", "", "", ""),
      Question(2, "", "", "", "", "", ""),
      Question(2, "", "", "", "", "", ""),
      Question(2, "", "", "", "", "", ""),
      Question(2, "", "", "", "", "", ""),
      Question(2, "", "", "", "", "", ""),



   ]
   for q in questions:
      db_session.add(q)

def populate():
   _add_users()
   _add_questions()
   db_session.commit()

def exists():
   try:
      db_session.execute(text("Select * from users;"))
      return True
   except OperationalError:
      return False



if exists():
   populate()
else:
   print("Initizalizing db")
   init_db()
   populate()


