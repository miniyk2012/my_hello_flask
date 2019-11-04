import os
import threading

from flask import url_for, redirect, render_template, flash, abort
from loguru import logger

from demos.database import db
from demos.database.forms import NewNoteForm, EditNoteForm, DeleteNoteForm
from demos.database.models import Note


def get_val(thread_local):
    try:
        return thread_local.val
    except AttributeError:
        return None


def register(app):
    thread_local = threading.local()

    @app.route('/set-threadlocal/<val>')
    def set_threadlocal(val):
        logger.info(threading.activeCount())
        thread_local.val = val
        logger.info('set val={}, thread_id={}, threadname={}, pid={}'
                    .format(get_val(thread_local), threading.currentThread().ident, threading.currentThread().name,
                            os.getpid()))
        return get_val(thread_local)

    @app.route('/get-threadlocal')
    def get_threadlocal():
        logger.info(threading.activeCount())
        logger.info('get val={}, thread_id={}, threadname={}, pid={}'
                    .format(get_val(thread_local), threading.currentThread().ident, threading.currentThread().name,
                            os.getpid()))
        return get_val(thread_local) or 'failure'

    @app.route('/')
    def index():
        form = DeleteNoteForm()
        notes = Note.query.all()
        return render_template('index.html', notes=notes, form=form)

    @app.route('/new', methods=['GET', 'POST'])
    def new_note():
        form = NewNoteForm()
        if form.validate_on_submit():
            body = form.body.data
            note = Note(body=body)
            db.session.add(note)
            db.session.commit()
            flash('Your note is saved.')
            return redirect(url_for('index'))
        return render_template('new_note.html', form=form)

    @app.route('/edit/<int:note_id>', methods=['GET', 'POST'])
    def edit_note(note_id):
        form = EditNoteForm()
        note = Note.query.get(note_id)
        if form.validate_on_submit():
            note.body = form.body.data
            db.session.add(note)
            db.session.commit()
            flash('Your note is updated.')
            return redirect(url_for('index'))
        form.body.data = note.body
        return render_template('edit_note.html', form=form)

    @app.route('/delete/<int:note_id>', methods=['POST'])
    def delete_note(note_id):
        form = DeleteNoteForm()
        note = Note.query.get(note_id)
        if form.validate_on_submit():
            db.session.delete(note)
            db.session.commit()
            flash('Your note is updated.')
            return redirect(url_for('index'))
        else:
            abort(400)
