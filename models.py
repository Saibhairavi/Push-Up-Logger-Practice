from . import db
from flask_login import UserMixin 
# @adds flaskn login attribute to the model so flask login will work
from flask_login import LoginManager
from datetime import datetime
# from sqlalchemy.orm import backref


# userloader tells flask login how a specific user from id that stored in session coki
class User(db.Model,UserMixin):
    id=db.Column(db.Integer,primary_key=True)
    email=db.Column(db.String(100),unique=True)
    password=db.Column(db.String(100))
    name=db.Column(db.String(100))
    workouts=db.relationship('Workout',backref='author',lazy=True)
    # workouts=db.relationship('Workout',backref=backref('author',uselist=False),lazy=True)
# Lazy parameter determines how the related objects get 
# loaded when querying through relationships

class Workout(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    pushups=db.Column(db.Integer,nullable=False)
    date_posted=db.Column(db.DateTime,nullable=False,default=datetime.utcnow)
    comment=db.Column(db.Text,nullable=False)
    user_id=db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)