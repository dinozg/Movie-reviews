# review.py file
from flask import (
    Blueprint, flash, g, redirect,
    render_template, request, url_for)
from werkzeug.exceptions import abort
from flaskapp.db import get_db
from .utils import login_required, get_all_reviews, \
    get_movie, get_review_from_db, get_movie_img

bp = Blueprint('review', __name__)

# reviews route
@bp.route('/reviews')
@login_required
def reviews():
    all_reviews = get_all_reviews()
    return render_template('review/reviews.html',
                           all_reviews=all_reviews,
                           get_movie_img=get_movie_img)

# create a new review
@bp.route('/<int:id>/create', methods=('GET', 'POST'))
@login_required
def create(id):
    # get movie
    movie = get_movie(id)
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None
        if not body:
            error = 'You need to add a review.'
        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO review (id, title, body, author_id)'
                ' VALUES (?, ?, ?, ?)',
                (id, title, body, g.user['id'])
            )
            db.commit()
            return redirect(url_for('review.reviews'))
    return render_template('review/create.html', movie=movie)

# get a single review
def get_review(id, check_author=True):
    review = get_review_from_db(id)
    if review is None:
        abort(404, f"Post id {id} doesn't exist.")
    if check_author and review['author_id'] != g.user['id']:
        abort(403)
    return review

# update review
@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    review = get_review(id)
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
                'UPDATE review SET title = ?, body = ?'
                ' WHERE id = ?',
                (title, body, id)
            )
            db.commit()
            return redirect(url_for('review.reviews'))
    return render_template('review/update.html', review=review)

# delete review
@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_review(id)
    db = get_db()
    db.execute('DELETE FROM review WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('review.reviews'))

