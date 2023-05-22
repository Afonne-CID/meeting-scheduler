'''
This module initializes the Flask application and the database,
registers the application's error handlers, and creates the database tables.
'''

from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from .database import db
from .error_handlers import (handle_bad_request, handle_unauthorized,
                             handle_forbidden, handle_page_not_found,
                             handle_internal_server_error)


def create_app(name=__name__):
    '''
    This function initializes the Flask application with the specified name,
    configures it, initializes the JWT manager and the database,
    imports routes and models, creates the database tables,
    and registers error handlers.

    Args:
        name (str): The name of the application. Defaults to '__name__'.

    Returns:
        app (flask.Flask): The initialized Flask application.
    '''
    app = Flask(name)

    # Load the appropriate configuration
    if name == 'testing':
        app.config.from_object('config.TestConfig')
    elif name == 'development':
        app.config.from_object('config.DevelopmentConfig')
    else:  # 'production' or any other value
        app.config.from_object('config.Config')

    CORS(app, resources={
         r"/api/*": {"origins": app.config.get('ALLOWED_ORIGINS')}})
    jwt = JWTManager(app)  # pylint: disable=unused-variable

    db.init_app(app)

    with app.app_context():

        # import routes after the database is initialized

        # pylint: disable=import-outside-toplevel
        from .routes.user_routes import user_routes
        from .routes.meeting_routes import meeting_routes
        from .routes.vote_routes import vote_routes
        from .routes.timeslot_routes import timeslot_routes

        # Register blueprints
        app.register_blueprint(user_routes)
        app.register_blueprint(meeting_routes)
        app.register_blueprint(vote_routes)
        app.register_blueprint(timeslot_routes)

        # import models before db.create() call

        # pylint: disable=import-outside-toplevel,unused-import
        from .models import meeting, timeslot, user, vote

        # create tables for our models
        db.create_all()

        # register error handlers
        app.register_error_handler(400, handle_bad_request)
        app.register_error_handler(401, handle_unauthorized)
        app.register_error_handler(403, handle_forbidden)
        app.register_error_handler(404, handle_page_not_found)
        app.register_error_handler(500, handle_internal_server_error)

    return app
