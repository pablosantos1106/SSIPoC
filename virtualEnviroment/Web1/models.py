from datetime import datetime
from flask_login import UserMixin
from sqlalchemy import Column, Integer, String
from . import db

class User(UserMixin, db.Model):
    __tablename__ = 'Users'
    id = Column(Integer, primary_key=True, nullable=False) # primary keys are required by SQLAlchemy
    username = Column(String(40), unique=True, nullable=False)
    url = Column(String(20), nullable=False)
    port = Column(Integer, nullable=False)
    wallet =  Column(String(30), nullable=False)
    password = Column(String(100), nullable=False)
