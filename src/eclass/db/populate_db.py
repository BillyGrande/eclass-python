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
      Question(0, "How to spell Pyton?", "With P", "With Y", "ON", "P-Y-T-H-O-N", "a4"),
      Question(0, "Please select third checkbox", "Not", "Not", "Here", "Not", "a3")
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


