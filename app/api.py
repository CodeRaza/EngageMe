from flask import Flask, jsonify
from flask_cors import CORS
import app.config as config
from app.routes.teacher import bp as teacher_bp
from app.routes.user import bp as user_bp
from app.models import db
from http import HTTPStatus
from app.models.User import User
from app.routes import guard
from app.mail import mail
import os
basedir = os.path.abspath(os.path.dirname(__file__))

def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.db')
   
    app.config['SQLALCHEMY_TRACK_MOIFICATIONS'] = False
    app.config['JSON_SORT_KEYS'] = False
    app.config['SECRET_KEY'] = 'top secret'
    app.config['JWT_ACCESS_LIFESPAN'] = {'hours': 24}
    app.config['JWT_REFRESH_LIFESPAN'] = {'days': 30}

    
    # Mail config
    app.config['MAIL_SERVER']= config.MAIL_SERVER
    app.config['MAIL_PORT'] = config.MAIL_PORT
    app.config['MAIL_USERNAME'] = config.MAIL_USERNAME
    app.config['MAIL_DEFAULT_SENDER'] = config.MAIL_USERNAME
    app.config['MAIL_PASSWORD'] = config.MAIL_PASSWORD
    app.config['MAIL_USE_TLS'] = True if config.MAIL_USE_TLS == 'true' else False
    app.config['MAIL_USE_SSL'] = True if config.MAIL_USE_SSL == 'true' else False

    CORS(app)
    guard.init_app(app, User)
    db.init_app(app)
    mail.init_app(app)


    """
    For deployement, Make sure you have a mysql server running and configured
    with SQLAlchemy, Uncomment these two lines and run the server to create tables
    and add users. You will get an Integrity error that's just because the function
    is called more than once.
    After running the server for the first time remove or comment these lines 
    again and run the server.
    Teacher Credentials: (Teacher, password)
    Student Credentials: (Student, password)
    """
    # with app.app_context():
    #     create_tables_and_add_user()

    app.register_blueprint(teacher_bp)
    app.register_blueprint(user_bp)

    @app.errorhandler(HTTPStatus.UNPROCESSABLE_ENTITY)
    @app.errorhandler(HTTPStatus.BAD_REQUEST)
    def webargs_error_handler(err):
        headers = err.data.get("headers", None)
        messages = err.data.get("messages", ["Invalid Request."])
        if headers:
            return jsonify({"errors": messages}), err.code, headers
        else:
            return jsonify({"errors": messages}), err.code

    return app


def create_tables_and_add_user():
    db.create_all()
    # db.session.add(User(email="teacher@gmail.com",password=guard.hash_password("password"),role="teacher"))
    # db.session.add(User(email="student@gmail.com",password=guard.hash_password("password"),role="student"))
    db.session.commit()