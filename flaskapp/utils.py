# utils.py file

from flask import (g, redirect, url_for)
from flaskapp.db import get_db
import csv
import functools

# function to read all movies
def get_movies():
    """reads the csv file and returns
        the list of movies"""
    movies = []
    movie_path = 'data/imdb_top_20.csv'
    with open(movie_path, 'r') as file:
        movie_dict = csv.DictReader(file, delimiter=';')
        for movie in movie_dict:
            movies.append(movie)
    # return the list
    return movies

# function to read a single movie
def get_movie(id):
    """returns a single movie"""
    movie = None
    movie_path = 'data/imdb_top_20.csv'
    with open(movie_path, 'r') as file:
        movie_dict = csv.DictReader(file, delimiter=';')
        for m in movie_dict:
            if m['id'] == str(id):
                movie = m
    return movie

# get movie image
def get_movie_img(id):
    return get_movie(id)['imageURL']

# get all reviews
def get_all_reviews():
    db = get_db()
    return db.execute(
        'SELECT r.id, title, body, created, author_id, username, fullname'
        ' FROM review r JOIN user u ON r.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()

# get review from db
def get_review_from_db(id):
    return get_db().execute(
        'SELECT r.id, title, body, created, author_id, username'
        ' FROM review r JOIN user u ON r.author_id = u.id'
        ' WHERE r.id = ?',
        (id,)
    ).fetchone()

# get user
def get_user(username):
    db = get_db()
    user = db.execute(
        'SELECT * FROM user WHERE username = ?', (username,)
    ).fetchone()
    return user

# Require Authentication
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('login.login'))
        return view(**kwargs)
    return wrapped_view