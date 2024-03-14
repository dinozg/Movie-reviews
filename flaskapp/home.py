# home.py file
from flask import (Blueprint, g, render_template)
from .utils import login_required, get_all_reviews, \
    get_movies, get_review_from_db

# initialize the Blueprint object
bp = Blueprint('home', __name__, url_prefix='/')

# Index View Code
@bp.route('/', methods=['GET'])
@login_required
def index():
    # get all movies
    movies = get_movies()
    # get all reviews
    all_reviews = get_all_reviews()
    # render index.html
    return render_template('home/index.html', movies=movies,
                           all_reviews=all_reviews,
                           get_if_reviewed=get_if_reviewed)

def get_if_reviewed(movie):
    review = get_review_from_db(movie['id'])
    if review is not None and g.user['id'] == review['author_id']:
        return True
    else:
        return False

