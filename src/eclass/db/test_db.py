from eclass.db.db import db_session
from eclass.db.models import User
from eclass.db.db import init_db


init_db()
u = User("testuser", 'test@localhost')
db_session.add(u)
db_session.commit()