# __init__.py file

import os
from flask import Flask
from . import db, register, login, home, review

# application factory
def create_app(test_config=None):
    # create a Flask app object
    app = Flask(__name__, instance_relative_config=True)

    # configure the app
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskapp.sqlite'),
    )

    # create the instance folder if not exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # db registration
    db.init_app(app)

    # register Blueprints
    app.register_blueprint(register.bp)
    app.register_blueprint(login.bp)
    app.register_blueprint(home.bp)
    app.register_blueprint(review.bp)

    # a simple test to see if it works
    @app.route('/test')
    def test():
        return 'Flaskapp init file works fine :)'

    # return the configured Flask app object
    return app

