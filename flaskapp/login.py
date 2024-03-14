# login.py file

from flask import (Blueprint, flash, g, redirect,
                   render_template, request, session, url_for)
from flaskapp.db import get_db
from werkzeug.security import check_password_hash

# initialize the Blueprint object
bp = Blueprint('login', __name__, url_prefix='/')

# Login View Code
@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()
        # check user from db
        if user is None:
            error = "Incorrect username. Please try again."
        elif not check_password_hash(user['password'], password):
            error = "Incorrect password. Please try again."
        # check error
        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('home.index'))
        # flash error
        flash(error)
    # render template
    return render_template('login/login.html')

# Run before all view functions
@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()

# logout route
@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login.login'))