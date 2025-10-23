# import packages
import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from FortiDragon.db import get_db

# Define blueprint named auth
bp = Blueprint('auth', __name__, url_prefix='/auth')

# create blueprint for /register
@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email_address = request.form['email_address']
        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'

        if error is None:
            try:
                db.execute(
                    "INSERT INTO user (username, first_name, last_name, email_address, password) VALUES (?, ?, ?, ?, ?)",
                    (username, first_name, last_name, email_address, generate_password_hash(password)),
                )
                db.commit()
            except db.IntegrityError:
                error = f"User {username} is already registered."
            else:
                return redirect(url_for("auth.login"))

        flash(error)

    return render_template('auth/register.html')

# Create blueprint for /login
@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # name = request.form['name']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')

# If the user is already logged in, restore session cookie
# @bp.before_app_request
# def load_logged_in_user():
#     user_id = session.get('user_id')
#
#     if user_id is None:
#         g.user = None
#     else:
#         g.user = get_db().execute(
#             'SELECT * FROM user WHERE id = ?', (user_id,)
#         ).fetchone()

@bp.before_app_request
def load_logged_in_user():
    """Load the logged-in user's data (including role) before every request."""
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        db = get_db()
        row = db.execute(
            '''
            SELECT id, username, first_name, last_name, email_address,
                   COALESCE(role, 'user') AS role
            FROM user
            WHERE id = ?
            ''',
            (user_id,)
        ).fetchone()

        # Convert sqlite3.Row -> dict so .get() works in templates
        g.user = dict(row) if row else None

# Create blueprint for /logout
@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

# Function to check for login status
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view