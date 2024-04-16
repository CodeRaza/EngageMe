from datetime import datetime, timedelta
from flask import Blueprint, jsonify
from sqlalchemy import func, or_, extract, and_
import flask_praetorian
from http import HTTPStatus
from webargs.flaskparser import use_args
from webargs import fields
from app.models import db
from app.schemas.ClassroomSchema import ClassroomSchema
from app.models.Classroom import Classroom
from app.schemas.LectureSchema import LectureSchema
from app.models.Lecture import Lecture
from app.schemas.LectureSubtopicSchema import LectureSubtopicSchema
from app.models.LectureSubtopic import LectureSubtopic
from app.schemas.QuestionsAndPollsSchema import QuestionsAndPollsSchema
from app.models.QuestionsAndPolls import QuestionsAndPolls
from app.schemas.AnswersAndVotesSchema import AnswersAndVotesSchema
from app.models.AnswersAndVotes import AnswersAndVotes
from app.routes import guard
import flask_praetorian
import jwt

bp = Blueprint("teacher", __name__)

#################### Classroom ############################################
@bp.route("/classroom", methods=["POST"])
@use_args(ClassroomSchema, location="json")
# @flask_praetorian.roles_accepted("teacher")
# @flask_praetorian.auth_required
def add_classroom(args):
    """
    POST API to add a Classroom to database.
    :param: values for a single record to be added
            in tickets table.
    :response:  primary key for the record being added
                with status 200.
    """
    classroom = Classroom(**args)
    db.session.add(classroom)
    db.session.commit()

    return {"id": classroom.id, "message": "Classroom Added"}

@bp.route("/classroom", methods=["GET"])
@use_args(
    {
        "teacher_id": fields.Integer(required=False, missing=None),
    },
    location="query",
)
@flask_praetorian.roles_accepted("teacher")
@flask_praetorian.auth_required
def get_classrooms(args):
    """
    GET API to add a Get all classroms for a teacher from database.
    :param: teacher_id
    :response: List of classroom dicts
    """
    classrooms = db.session.query(Classroom).filter(Classroom.teacher_id==args.get("teacher_id")).all()
    schema = ClassroomSchema(many=True)
    result = schema.dump(classrooms)
    
    return (jsonify(result), HTTPStatus.OK)

@bp.route("/classroom", methods=["DELETE"])
@use_args(
    {
        "classroom_id": fields.Integer(required=False, missing=None),
    },
    location="query",
)
@flask_praetorian.roles_accepted("teacher")
@flask_praetorian.auth_required
def delete_classroom(args):
    """
    DELETE API to delete a Classroom from database.
    :param: classroom_id
    :response: 200 OK
    """
    classroom = db.session.query(Classroom).filter(Classroom.id==args.get("classroom_id")).first()
    db.session.delete(classroom)
    db.session.commit()
    
    return jsonify({"message": "classroom deleted"}), HTTPStatus.OK

#################### Lecture ############################################
@bp.route("/lecture", methods=["POST"])
@use_args(LectureSchema, location="json")
@flask_praetorian.roles_accepted("teacher")
@flask_praetorian.auth_required
def add_lecture(args):
    """
    POST API to add a Lecture to database.
    :param: values for a single record to be added
            in tickets table.
    :response:  primary key for the record being added
                with status 200.
    """
    lecture = Lecture(**args)
    db.session.add(lecture)
    db.session.commit()

    return {"id": lecture.id, "message": "Lecture Added"}

@bp.route("/lecture", methods=["GET"])
@use_args(
    {
        "classroom_id": fields.Integer(required=False, missing=None),
    },
    location="query",
)
# @flask_praetorian.roles_accepted("teacher")
@flask_praetorian.auth_required
def get_lectures(args):
    """
    GET API to add a Get all lectures for a teacher from database.
    :param: classroom_id
    :response: List of lecture dicts
    """
    lectures = db.session.query(Lecture).filter(Lecture.classroom_id==args.get("classroom_id")).all()
    schema = LectureSchema(many=True)
    result = schema.dump(lectures)
    
    return (jsonify(result), HTTPStatus.OK)

@bp.route("/lecture", methods=["DELETE"])
@use_args(
    {
        "lecture_id": fields.Integer(required=False, missing=None),
    },
    location="query",
)
# @flask_praetorian.roles_accepted("teacher")
@flask_praetorian.auth_required
def delete_lecture(args):
    """
    DELETE API to delete a lecture from database.
    :param: lecture_id
    :response: 200 OK
    """
    lecture = db.session.query(Lecture).filter(Lecture.id==args.get("lecture_id")).first()
    db.session.delete(lecture)
    db.session.commit()
    
    return jsonify({"message": "lecture deleted"}), HTTPStatus.OK


#################### Lecture Material ############################################



#################### Lecture Subtopic ############################################
@bp.route("/subtopic", methods=["POST"])
@use_args(LectureSubtopicSchema, location="json")
@flask_praetorian.roles_accepted("teacher")
@flask_praetorian.auth_required
def add_subtopic(args):
    """
    POST API to add a subtopic to database.
    :param: values for a single record to be added
            in lecture_subtopic table.
    :response:  primary key for the record being added
                with status 200.
    """
    subtopic = LectureSubtopic(**args)
    db.session.add(subtopic)
    db.session.commit()

    return {"id": subtopic.id, "message": "Subtopic Added"}

@bp.route("/subtopic", methods=["GET"])
@use_args(
    {
        "lecture_id": fields.Integer(required=False, missing=None),
    },
    location="query",
)
# @flask_praetorian.roles_accepted("teacher")
@flask_praetorian.auth_required
def get_subtopics(args):
    """
    GET API to add a Get all subtopics for a lecture from database.
    :param: lecture_id
    :response: List of subtopic dicts
    """
    subtopics = db.session.query(LectureSubtopic).filter(LectureSubtopic.lecture_id==args.get("lecture_id")).all()
    schema = LectureSubtopicSchema(many=True)
    result = schema.dump(subtopics)
    
    return (jsonify(result), HTTPStatus.OK)

@bp.route("/subtopic", methods=["DELETE"])
@use_args(
    {
        "lecture_subtopic_id": fields.Integer(required=False, missing=None),
    },
    location="query",
)
@flask_praetorian.roles_accepted("teacher")
@flask_praetorian.auth_required
def delete_subtopic(args):
    """
    DELETE API to delete a lecture subtopic from database.
    :param: lecture_subtopic_id
    :response: 200 OK
    """
    lecture_subtopic = db.session.query(LectureSubtopic).filter(LectureSubtopic.id==args.get("lecture_subtopic_id")).first()
    db.session.delete(lecture_subtopic)
    db.session.commit()
    
    return jsonify({"message": "lecture subtopic deleted"}), HTTPStatus.OK


#################### Lecture Subtopic ############################################


#################### Questions/Polls ############################################

@bp.route("/questions_and_polls", methods=["POST"])
@use_args(QuestionsAndPollsSchema, location="json")
@flask_praetorian.roles_accepted("teacher")
@flask_praetorian.auth_required
def add_questions_and_polls(args):
    """
    """
    subtopic = QuestionsAndPolls(**args)
    db.session.add(subtopic)
    db.session.commit()

    return {"id": subtopic.id, "message": "Added"}

@bp.route("/questions_and_polls", methods=["GET"])
@use_args(
    {
        "lecture_id": fields.Integer(required=False, missing=None),
    },
    location="query",
)
# @flask_praetorian.roles_accepted("teacher")
@flask_praetorian.auth_required
def get_questions_and_polls(args):
    """
    """
    subtopics = db.session.query(QuestionsAndPolls).filter(QuestionsAndPolls.lecture_id==args.get("lecture_id")).all()
    schema = QuestionsAndPollsSchema(many=True)
    result = schema.dump(subtopics)
    
    return (jsonify(result), HTTPStatus.OK)


#################### Questions/Polls ############################################

#################### Answers/Votes ############################################

@bp.route("/answer_and_votes", methods=["POST"])
@use_args(AnswersAndVotesSchema, location="json")
@flask_praetorian.roles_accepted("student")
@flask_praetorian.auth_required
def add_answer_and_votes(args):
    """
    """
    subtopic = AnswersAndVotes(**args)
    db.session.add(subtopic)
    db.session.commit()

    return {"id": subtopic.id, "message": "Added"}

@bp.route("/answer_and_votes", methods=["GET"])
@use_args(
    {
        "lecture_id": fields.Integer(required=False, missing=None),
    },
    location="query",
)
# @flask_praetorian.roles_accepted("teacher")
@flask_praetorian.auth_required
def get_answer_and_votes(args):
    """
    """
    subtopics = db.session.query(AnswersAndVotes).filter(AnswersAndVotes.lecture_id==args.get("lecture_id")).all()
    schema = AnswersAndVotesSchema(many=True)
    result = schema.dump(subtopics)
    
    return (jsonify(result), HTTPStatus.OK)


#################### Answers/Votes ############################################


#################### Join lecture ############################################

@bp.route("/create_lecture_link", methods=["GET"])
@use_args(
    {
        "lecture_id": fields.Integer(required=False, missing=None),
    },
    location="query",
)
@flask_praetorian.roles_accepted("teacher")
@flask_praetorian.auth_required
def create_lecture_link(args):
    """
    """
    token = jwt.encode(args.get("lecture_id"))
    
    return (jsonify({token:token}), HTTPStatus.OK)

@bp.route("/join_lecture", methods=["GET"])
@use_args(
    {
        "token": fields.Integer(required=False, missing=None),
    },
    location="query",
)
# @flask_praetorian.roles_accepted("teacher")
@flask_praetorian.auth_required
def join_lecture(args):
    """
    """
    token = jwt.decode(args.get("token"), "test")
    lecture_id = db.session.query(Lecture.classroom_id).filter(Lecture.id==token.first())
    breakpoint()
    user_id = flask_praetorian.current_user().id
    
    return (jsonify("result"), HTTPStatus.OK)


#################### Join lecture ############################################