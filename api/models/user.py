from flask import current_app
from sqlalchemy import TIMESTAMP, Column, Integer, String, func
from database import db
from sqlalchemy.orm import relationship

class User(db.Model):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True) ###user
    user_name = Column(String(80), unique=True, nullable=False)
    password = Column(String(128), nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    user_type =Column(String(120), nullable=False)
    updated_on = Column(TIMESTAMP, server_default=func.now(), onupdate=func.current_timestamp())

    def __repr__(self):
        return f"<User {self.username}>"
    
    