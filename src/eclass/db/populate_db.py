from eclass.db.db import db_session
from eclass.db.models import User, Question
from eclass.db.db import init_db
import sqlalchemy as sqla
from sqlalchemy.exc import OperationalError
from sqlalchemy import text

#init_db()
#u = User("testuser", 'test@localhost')
#db_session.add(u)


try:
   #db_session.execute(text("Select 1;"))
   q = Question(0, "When python first appeared?", "Late 1980", "In 1991", "At 00s", "Designed 1999 and developed 2002", "a1")
   db_session.add(q)
   db_session.commit()
except OperationalError:
   print("Initizalizing db")
   init_db()
    

