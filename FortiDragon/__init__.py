# import packages
import os

from flask import Flask, redirect, render_template, url_for


# initialize the app
def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'FortiDragon.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Displays the home page
    @app.route('/')
    def home():
            return redirect(url_for('report.index'))

    def create_app():
        app = ...
        # existing code omitted

    # Import init_app from db.py
    from . import db
    db.init_app(app)

    # Import auth blueprint
    from . import auth
    app.register_blueprint(auth.bp)

    # Import report blueprint
    from . import report
    app.register_blueprint(report.bp)
    app.add_url_rule('/index', endpoint='index')

    return app