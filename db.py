from datetime import datetime

from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, backref

from config import DATABASE_URI, DATABASE_ECHO
from perms import Role


engine = create_engine(DATABASE_URI, echo=DATABASE_ECHO)

Base = declarative_base()
Session = sessionmaker(engine)
session = Session()


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

    role = Column(Integer, default=Role.GUEST)

    def __repr__(self):
        return f'<User#{self.id} "{self.name} {self.surname}", r: {self.role}>'

    def is_user(self):
        return self.role == Role.USER

    def is_admin(self):
        return self.role == Role.ADMIN

    def is_editor(self):
        return self.role == Role.EDITOR


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


def create_all():
    Base.metadata.create_all(engine)


if __name__ == '__main__':
    create_all()
