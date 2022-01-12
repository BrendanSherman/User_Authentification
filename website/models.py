from . import db #imports db from current package
from flask_login import UserMixin
from sqlalchemy.sql import func

AUTH_MAX_LENGTH = 150
NOTE_MAX_LENGTH = 10000

class Note(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	data = db.Column(db.String(NOTE_MAX_LENGTH))
	date = db.Column(db.DateTime(timezone=True), default=func.now)
	

class User(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key = True)
	#unique- does not allow duplicate email accounts
	email = db.Column(db.String(AUTH_MAX_LENGTH), unique=True) 
	password = db.Column(db.String(AUTH_MAX_LENGTH))
	first_name = db.Column(db.String(AUTH_MAX_LENGTH))