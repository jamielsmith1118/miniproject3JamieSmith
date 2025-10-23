from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from FortiDragon.auth import login_required
from FortiDragon.db import get_db

bp = Blueprint('report', __name__)

@bp.route('/index')
def index():
    # db = get_db()
    # posts = db.execute(
    #     #'SELECT p.id, title, body, created, author_id, username, severity, mitigation, status'
    #     'SELECT p.id, title, body, created, author_id, username'
    #     ' FROM post p JOIN user u ON p.author_id = u.id'
    #     ' ORDER BY created DESC'
    # ).fetchall()
    # #return render_template('report/index.html', posts=posts)
    return render_template('report/index.html')


@bp.route('/vulns')
def vulns():
    db = get_db()
    posts = db.execute(
        #'SELECT p.id, title, body, created, author_id, username, severity, mitigation, status'
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template('report/vulns.html', posts=posts)

@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO post (title, body, author_id)'
                ' VALUES (?, ?, ?)',
                (title, body, g.user['id'])
            )
            db.commit()
            return redirect(url_for('report.index'))

    return render_template('report/create.html')

def get_post(id, check_author=True):
    post = get_db().execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    if post is None:
        abort(404, f"Post id {id} doesn't exist.")

    if check_author and post['author_id'] != g.user['id']:
        abort(403)

    return post

@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE post SET title = ?, body = ?'
                ' WHERE id = ?',
                (title, body, id)
            )
            db.commit()
            return redirect(url_for('index'))

    return render_template('report/update.html', post=post)

@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_post(id)
    db = get_db()
    db.execute('DELETE FROM post WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('report.index'))

# User Profile page
@bp.route('/profile')
@login_required
def profile():
    """Show the logged-in user's profile."""
    db = get_db()
    user = db.execute(
        'SELECT u.id, u.username, u.first_name, u.last_name, u.email_address '
        'FROM user AS u '
        ' WHERE id = ?',
        (g.user['id'],)
    ).fetchone()

    # user will never be None here if your auth is correct, but guard anyway:
    if not user:
        # fallback: show minimal info from g.user
        user = g.user

    return render_template('report/profile.html', user=user)