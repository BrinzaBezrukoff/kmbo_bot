from datetime import datetime
from functools import wraps

from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, backref, scoped_session

from config import DATABASE_URI, DATABASE_ECHO
from enums import Role


engine = create_engine(DATABASE_URI, echo=DATABASE_ECHO)

Base = declarative_base()
session_factory = sessionmaker(engine)
Session = scoped_session(session_factory)


def db_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        session = Session()
        res = func(*args, **kwargs, db=session)
        Session.remove()
        return res
    return wrapper


class Subject (Base):
    __tablename__ = "subjects"

    id = Column(Integer, primary_key=True)
    name = Column(String(255))

    def __repr__(self):
        return f'<Subject#{self.id} "{self.name}">'


class User (Base):
    __tablename__ = "users"

    tg_id = Column(Integer, primary_key=True)
    name = Column(String(100), default="Noname")
    surname = Column(String(100), default="Noname")

    role = Column(Integer, default=Role.Guest)

    def __repr__(self):
        return f'<User#{self.tg_id} "{self.name} {self.surname}", {self.role_name}>'

    @property
    def role_name(self):
        return Role(self.role).name

    @property
    def is_guest(self):
        return self.role == Role.Guest

    @classmethod
    def get_guest(cls, tg_id):
        return User(tg_id=tg_id, role=Role.Guest, name="Guest", surname="Guest")


class Deadline (Base):
    __tablename__ = "deadlines"

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    description = Column(Text)

    dead_date = Column(DateTime, default=datetime.now)

    subject_id = Column(Integer, ForeignKey("subjects.id"))
    subject = relationship(Subject, backref=backref("deadlines", lazy="dynamic"))

    def __repr__(self):
        return f'<Deadline#{self.id} "{self.name}" by {self.subject.name}>'


def get_user(db, tg_id):
    user = db.query(User).get(tg_id)
    if not user:
        user = User.get_guest(tg_id)
    return user


def create_all():
    Base.metadata.create_all(engine)


if __name__ == '__main__':
    create_all()
