#Blueprint file defines all routes (URLs) for site 
from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note
from . import db
import json

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
	if request.method == 'POST':
		note = request.form.get('note')
		if len(note) < 1:
			flash('Please add content to note', category='error')
		else:
			new_note = Note(data=note, user_id = current_user.id)
			db.session.add(new_note)
			db.session.commit()
			flash('Added Note', category='success')

	return render_template("home.html", user=current_user)


@views.route('/delete-note', methods=['POST'])
def delete_note():
	note_del = json.loads(request.data) #collects data from POST request, loads it as dict
	noteId = note_del['noteId'] #access noteID (JSON attribute)
	note = Note.query.get(noteId) #access note with given noteID in DB
	if note:
		if note.user_id == current_user.id:
				db.session.delete(note)
				db.session.commit()
				
	return jsonify({}) #returning is required for views
