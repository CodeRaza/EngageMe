from flask import Blueprint, jsonify, render_template, request
from app.routes import guard
import flask_praetorian
from webargs.flaskparser import use_args
from webargs import fields
from app.models.User import User
from app.models import db
from app.mail import mail
import app.config as config
from flask_mail import Message
import jwt

bp = Blueprint("user", __name__)


@bp.route('/SignUp', methods=['POST'])
@use_args({
    "username": fields.String(required=True, allow_none=False),
    "email": fields.String(required=True, allow_none=False),
    "password": fields.String(required=True, allow_none=False),
    "role": fields.String(required=True, allow_none=False)
    }, location="json")
def add_user(args):
    """
    POST API to add a user
    """
    new_user = User(
        username=args["username"],
        email=args["email"],
        password=guard.hash_password(args["password"]),
        role=args["role"],
    )
    db.session.add(new_user)
    db.session.commit()

    return jsonify("User Added"), 200

@bp.route('/login', methods=['POST'])
@use_args({
    "email": fields.String(required=True, allow_none=False),
    "password": fields.String(required=True, allow_none=False),
    }, location="json")
def login(args):
    """
    POST API to login the user
    :params: username and password
    :response: an auth key and role of the user logged in 
    """
    username = args["email"]
    password = args["password"]
    user = guard.authenticate(username, password)
    ret = {
        'access_token': guard.encode_jwt_token(user),
        'role': user.role,
        'id' : user.id
        }
    return ret, 200


@bp.route('/forgotPassword', methods=['GET'])
@use_args({
    "username": fields.String(required=True, allow_none=False),
    }, location="query")
def forgot_password(args):
    """

    """
    username = args["username"]
    user = db.session.query(User).filter(User.username == username).first()

    if user:
        token = user.get_reset_token()
        url = f"{request.headers['Origin']}/resetPassword/{token}"
        msg = Message()
        msg.subject = "Flask App Password Reset"
        msg.sender = config.MAIL_USERNAME
        msg.recipients = [user.email]
        msg.html = render_template('reset_email.html',
                                    url=url,
                                    user=user)
        mail.send(msg)
    else:
        return 'failed', 422
    
    return 'success', 200


@bp.route('/resetPassword', methods=['POST'])
@use_args({
    "token": fields.String(required=True, allow_none=False),
    "password": fields.String(required=True, allow_none=False),
    }, location="json")
def reset_password(args):
    """

    """
    try:
        username = jwt.decode(args["token"],key=config.MAIL_SECRET_KEY,algorithms=['HS256'])['reset_password']
    except Exception as e:
        return e.args[0], 422
    user = db.session.query(User).filter(User.username == username).first()
    if user:
        user.password=guard.hash_password(args["password"])
        db.session.commit()
    else:
        raise Exception("user not found")

    
    return 'success', 200

@bp.route('/changePassword', methods=['POST'])
@flask_praetorian.auth_required
@use_args({
    "old_password": fields.String(required=True, allow_none=False),
    "new_password": fields.String(required=True, allow_none=False),
    }, location="json")

def change_password(args):

    username =flask_praetorian.current_user().username
    password = args["old_password"]
    user = guard.authenticate(username, password)
    if user:
        user.password = guard.hash_password(args["new_password"])
        db.session.commit()

    return 'success',200


@bp.route('/changeEmail', methods=['POST'])
@flask_praetorian.auth_required
@use_args({
    "email": fields.String(required=True, allow_none=False),
    "password": fields.String(required=True, allow_none=False),
    }, location="json")
def change_email(args):

    username =flask_praetorian.current_user().username
    user = guard.authenticate(username, args["password"])
    if user:
        user.email = args["email"]
        db.session.commit()

    return 'success',200
