from sqlalchemy import Column, Integer, String
from eclass.db.db import Base

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    email = Column(String(120), unique=True)

    def __init__(self, name=None, email=None):
        self.name = name
        self.email = email

    def __repr__(self):
        return f'<User {self.name!r}>'


class Question(Base):
    __tablename__ = 'questions'
    id = Column(Integer,primary_key=True)
    chapter = Column(Integer,unique=False)
    question = Column(String(300), unique=False)
    a1 = Column(String(150), unique=False, nullable=True)
    a2 = Column(String(150), unique=False, nullable=True)
    a3 = Column(String(150), unique=False, nullable=True)
    a4 = Column(String(150), unique=False, nullable=True)
    correct = Column(String(3), unique=False)

    def __init__(self, chapter=None, question=None, a1=None, a2=None, a3=None, a4=None, correct=None):
        self.chapter = chapter
        self.question = question
        self.a1 = a1
        self.a2 = a2
        self.a3 = a3
        self.a4 = a4
        self.correct = correct

    def __repr__(self):
        return f'<Question {self.question!r}'