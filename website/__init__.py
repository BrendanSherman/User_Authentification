#initializes Flask application and SQLalchemy database
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

#initialize database
db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
	app = Flask(__name__)
	app.config['SECRET_KEY'] = 'kimigadaisuki'
	app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}' #defines location for db
	db.init_app(app) #connects database with flask application

	#Imports blueprints from within package
	from .views import views
	from .auth import auth

	#Connects blueprints to flask app
	app.register_blueprint(views, url_prefix='/')
	app.register_blueprint(auth, url_prefix='/')

	from .models import User, Note #ensures models.py runs before db creation
	create_db(app)

	login_manager = LoginManager()
	login_manager.login_view = 'auth.login' #specifies when user is not logged in
	login_manager.init_app(app)

	@login_manager.user_loader #decorator specifies function below for loading user
	def load_user(id):
		return User.query.get(int(id)) #get looks for primary key by default

	return app

#Checks for preexisting database, creates one if not
def create_db(app):
	if not path.exists('website/' + DB_NAME):
		db.create_all(app=app)
		print('Database created')