from sqlalchemy import Column, Integer, String, ForeignKey
from database import Base
from werkzeug.security import generate_password_hash, check_password_hash

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String(128), unique=True)
    password = Column(String(512))

    def __init__(self, username=None, password=None):
        self.username = username
        self.set_password(password)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

class Group(Base):
    __tablename__ = 'group'
    id = Column(Integer, primary_key=True)
    name = Column(String(256), unique=True)
    access_password = Column(String(512))
    current_donut_master = Column(Integer, ForeignKey('user.id'))

    def __init__(self, name=None, access_password=None, start_date=None, end_date=None):
        self.name = name
        self.access_password = access_password
        self.start_date = start_date
        self.end_date = end_date

class User_Group(Base):
    __tablename__ = 'user_group'
    id = Column(Integer, primary_key=True)
    user = Column(Integer, ForeignKey('user.id'))
    group = Column(Integer, ForeignKey('group.id'))
    is_admin = Column(Integer)

    def __init__(self, user=None, group=None, is_admin=False):
        self.user = user
        self.group = group
        self.is_admin = is_admin

class Contest(Base):
    __tablename__ = 'contest'
    id = Column(Integer, primary_key=True)
    group = Column(Integer, ForeignKey('group.id'))
    donut_master = Column(Integer, ForeignKey('user.id'))
    start_date = Column(String(64))
    end_date = Column(String(64))

    def __init__(self, group=None, donut_master=None, start_date='', end_date=''):
        self.group = group
        self.donut_master = donut_master
        self.start_date = start_date
        self.end_date = end_date