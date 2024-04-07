from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), nullable=True, unique=True)
    password = db.Column(db.String(255), nullable=True)
    points = db.Column(db.Integer, default=0)
    privilaged = db.Column(db.Integer, default=0)


class Questions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(255))
    question = db.Column(db.String(255))
    answer = db.Column(db.String(255))
    variants = relationship('Variants', backref='question', lazy=True)



class Variants(db.Model):    
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer,  db.ForeignKey('questions.id'), nullable=False)
    variants = db.Column(db.String(255))
