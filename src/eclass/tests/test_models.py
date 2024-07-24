from sqlalchemy import select
from eclass.db.models import User, Question
from eclass.db.db import db_session


def test_quiz_introduction():
    statement = select(Question).filter_by(chapter=0)
    user_obj = db_session.scalars(statement).all()
    db_session.query()
    assert user_obj[0].question=="When python first appeared?"
    
