# register.py file
from flask import (Blueprint, flash, redirect,
                   render_template, request, session, url_for)
from flaskapp.db import get_db
from werkzeug.security import generate_password_hash
from .utils import get_user

# initialize the Blueprint object
bp = Blueprint('register', __name__, url_prefix='/')

# Register View Code
@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        # get input fields
        username, password, fullname = get_input_fields()
        # get db
        db = get_db()
        # check input fields
        error = check_input_fields(username, password, fullname)
        # check error
        if error is None:
            try:
                # insert new user
                insert_into_db(db, username, password, fullname)
            except db.IntegrityError:
                error = f"User {username} is already registered."
            else:
                session.clear()
                session['user_id'] = get_user(username)['id']
                return redirect(url_for('home.index'))
        flash(error)
    return render_template('register/register.html')

# fn for getting inputs
def get_input_fields():
    username = request.form['username']
    password = request.form['password']
    fullname = request.form['fullname']
    return username, password, fullname

# fn for checking input fields
def check_input_fields(username, password, fullname):
    if not username or not password or not fullname:
        return 'Full Name, Username or Password can not be empty.'
    else:
        return None

# fn for inserting a DB row
def insert_into_db(db, username, password, fullname):
    db.execute("INSERT INTO user (username, password, fullname) "
               "VALUES (?, ?, ?)",
        (username, generate_password_hash(password), fullname),)
    db.commit()

