from flask import Blueprint, request, render_template, flash, jsonify #has a bunch of routes

from flask_login import login_required, current_user

from .models import Note
from . import db
import json
views = Blueprint('views', __name__)

#name of the Blueprint
@views.route('/', methods = ['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) < 1:
            flash('Note is too short!', category='error')
        else:
            new_note=Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash("Note added!", category='success')

    return render_template("home.html", user= current_user) #reference the current user and check if it is authenticated in HTML files

@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)

    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})
