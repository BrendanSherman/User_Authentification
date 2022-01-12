#initializes Flask application and SQLalchemy database

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

#initialize database
db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
	app = Flask(__name__)
	app.config['SECRET_KEY'] = 'kimigadaisuki'
	app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}' #locates database.db
	db.init_app(app) #initializes database with flask application

	#imports blueprints from within package
	from .views import views
	from .auth import auth

	#connects blueprints to flask app
	app.register_blueprint(views, url_prefix='/')
	app.register_blueprint(auth, url_prefix='/')
	
	return app

