from . import db #from the package similar to from website, import
from flask_login import UserMixin #users inherit from UserMixin
from sqlalchemy.sql import func

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now()) #func get the current time, use that to store the time and date.
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) #one to many relationships

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True) 
    email = db.Column(db.String(150), unique = True) #max length for String
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    notes = db.relationship('Note') #add into notes the note id every time we create a new note


