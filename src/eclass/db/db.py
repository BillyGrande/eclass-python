from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, declarative_base
import os

#file_path = os.path.abspath(os.getcwd()) +"eclass.db"
file_path = os.path.join(os.path.dirname(__file__), 'eclass.db')

#engine = create_engine('sqlite:///db/eclass.db')
engine = create_engine('sqlite:///'+ file_path)
db_session = scoped_session(sessionmaker(autocommit=False,autoflush=False,bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    import eclass.db.models
    Base.metadata.create_all(bind=engine)
