#Blueprint file defines all authentication routes (URLs) for site 
from flask import Blueprint, render_template, request, flash, redirect, url_for
from.models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		email = request.form.get('email')
		password = request.form.get('password')

		#Fetches user with the entered email
		user = User.query.filter_by(email=email).first() 
		#If user exists, check entered password against database
		if user:
			if check_password_hash(user.password, password):
				flash('Logged in ' + user.first_name, category='success')
				#flask sesssion remembers that user is logged in
				login_user(user, remember=True) 
				return redirect(url_for('views.home'))
			else:
				flash('Password incorrect', category='error')
		else:
			flash('User with that email does not exist', category='error')

	return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required #requires user to be logged in to access logout route 
def logout():
	logout_user()
	return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
	if request.method == 'POST':
		#accesses information submitted by user
		email = request.form.get('email')
		first_name = request.form.get('firstName')
		password1 = request.form.get('password1')
		password2 = request.form.get('password2')

		user = User.query.filter_by(email=email).first()
		#Checks if entered email address already in use 
		if user:
			flash('Account with this email address already exists', category='error')
		#Otherwise, verifies all fields
		elif len(email) < 5:
			flash('Email must be greater than 5 characters', category='error')
		elif len(first_name) < 2:
			flash('First name must be greater than 1 character', category='error')
		elif password1 != password2:
			flash('Passwords don\'t match', category='error')
		elif len(password1) < 7:
			flash('Password must be at least 7 characters', category='error')
		else:
			#If all conditions met, creates new user and adds it to database
			new_user = User(email=email, first_name=first_name, 
				password=generate_password_hash(password1, method='sha256'))
			db.session.add(new_user)
			db.session.commit()
			flash('Account created successfully!', category='success')
			return redirect(url_for('views.home'))


	return render_template("sign_up.html", user=current_user)

