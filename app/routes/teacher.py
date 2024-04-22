from datetime import datetime, timedelta
from flask import Blueprint, jsonify
from sqlalchemy import func, or_, extract, and_, not_, text
import sqlalchemy
import flask_praetorian
from http import HTTPStatus
from webargs.flaskparser import use_args
from webargs import fields
from app.models import db
from app.schemas.ClassroomSchema import ClassroomSchema
from app.models.Classroom import Classroom
from app.models.User import User
from app.models.Classroom import classroom_students
from app.schemas.LectureSchema import LectureSchema
from app.models.Lecture import Lecture
from app.schemas.LectureSubtopicSchema import LectureSubtopicSchema
from app.models.LectureSubtopic import LectureSubtopic
from app.schemas.QuestionsAndPollsSchema import QuestionsAndPollsSchema
from app.models.QuestionsAndPolls import QuestionsAndPolls
from app.schemas.AnswersAndVotesSchema import AnswersAndVotesSchema
from app.models.AnswersAndVotes import AnswersAndVotes
from app.schemas.LectureReviewSchema import LectureReviewSchema
from app.models.LectureReview import LectureReview
from app.schemas.StudentQuestionSchema import StudentQuestionSchema
from app.models.StudentQuestion import StudentQuestion
import flask_praetorian
import random
import string

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
@bp.route("/lecture", methods=["PUT"])
@use_args(
    {
        "lecture_id": fields.Integer(required=False, missing=None),
        "live": fields.Boolean(required=False, missing=None),
    },
    location="query",
)
@flask_praetorian.roles_accepted("teacher")
@flask_praetorian.auth_required
def update_lecture(args):
    """
    POST API to add a Lecture to database.
    :param: values for a single record to be added
            in tickets table.
    :response:  primary key for the record being added
                with status 200.
    """
    lecture = db.session.query(Lecture).filter(Lecture.id==args.get("lecture_id")).first()
    lecture.live = args.get("live")
    db.session.commit()

    return {"id": lecture.id, "message": "Lecture Updated"}
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
        "lecture_id": fields.Integer(required=False, missing=None),
        "student_id": fields.Integer(required=False, missing=None),
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
    lectures = db.session.query(Lecture)
    if args.get("classroom_id"):
        lectures = lectures.filter(Lecture.classroom_id==args.get("classroom_id")).all()
        schema = LectureSchema(many=True)
    if args.get("lecture_id"):
        lectures = lectures.filter(Lecture.id==args.get("lecture_id")).first()
        schema = LectureSchema(many=False)
    if args.get("student_id"):
        student = User.query.filter_by(id=args.get("student_id")).first()

        lectures = []
        if student:
            # Access the student_classrooms relationship to get all classrooms
            classrooms = student.student_classrooms

            # Iterate through each classroom and get all lectures associated with it
            for classroom in classrooms:
                classroom_lectures = classroom.lectures
                lectures.extend(classroom_lectures)
        schema = LectureSchema(many=True)
    result = schema.dump(lectures)
    
    return (jsonify(result), HTTPStatus.OK)

@bp.route("/lecture", methods=["DELETE"])
@use_args(
    {
        "lecture_id": fields.Integer(required=True),
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
        "lecture_id": fields.Integer(required=False),
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
    subtopic.uploaded_at = datetime.now()
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
    current_time = datetime.now()
    expiration_time = func.datetime(QuestionsAndPolls.uploaded_at, '+' + func.cast(QuestionsAndPolls.expires_in, sqlalchemy.String) + ' minutes')

    subtopics = db.session.query(QuestionsAndPolls).filter(
        QuestionsAndPolls.lecture_id == args.get("lecture_id"),
        expiration_time > current_time
    ).filter(
        not_(
            db.session.query(AnswersAndVotes)
            .filter(
                AnswersAndVotes.questions_and_polls_id == QuestionsAndPolls.id,
                AnswersAndVotes.student_id == flask_praetorian.current_user().id
            )
            .exists()
        )
    ).all()
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
        "student_id": fields.Integer(required=False, missing=None),
    },
    location="query",
)
# @flask_praetorian.roles_accepted("teacher")
@flask_praetorian.auth_required
def get_answer_and_votes(args):
    """
    """
    subtopics = db.session.query(QuestionsAndPolls).filter(QuestionsAndPolls.lecture_id == args.get("lecture_id")).filter(
            db.session.query(AnswersAndVotes)
            .filter(
                AnswersAndVotes.questions_and_polls_id == QuestionsAndPolls.id,
                AnswersAndVotes.student_id == flask_praetorian.current_user().id
            )
            .exists()
    ).all()
    schema = QuestionsAndPollsSchema(many=True)
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
    lecture_id = args.get("lecture_id")
    
    # Check if lecture_id is provided
    if lecture_id is None:
        return jsonify({"error": "lecture_id is required"}), HTTPStatus.BAD_REQUEST
    
    # Encode lecture_id as ASCII and append three randomly generated characters
    random_chars = ''.join(random.choices(string.ascii_uppercase + string.digits, k=3))
    encoded_id = str(lecture_id) + random_chars
    
    # Decode the lecture_id by removing the last three characters and converting ASCII to number
    decoded_id = int(encoded_id[:-3])
    
    return jsonify({"encoded_id": encoded_id, "decoded_id": decoded_id}), HTTPStatus.OK

@bp.route("/join_lecture", methods=["GET"])
@use_args(
    {
        "token": fields.String(required=False, missing=None),
    },
    location="query",
)
# @flask_praetorian.roles_accepted("teacher")
@flask_praetorian.auth_required
def join_lecture(args):
    """
    """
    encoded = args.get("token")
    # Decode the lecture_id by removing the last three characters and converting ASCII to number
    decoded_id = int(encoded[:-3])
    
    classroom_id = db.session.query(Lecture.classroom_id).filter(Lecture.id==decoded_id).first()
    user_id = flask_praetorian.current_user().id
    
    user = db.session.query(User).filter(User.id==user_id).first()
    classroom = db.session.query(Classroom).filter(Classroom.id==classroom_id[0]).first()
    classroom.students.append(user)
    db.session.commit()
    
    return (jsonify({
        "lecture_id": decoded_id
        }), HTTPStatus.OK)


#################### Join lecture ############################################


#################### Lecture Review ############################################

@bp.route("/lecture_review", methods=["POST"])
@use_args(LectureReviewSchema, location="json")
@flask_praetorian.roles_accepted("student")
@flask_praetorian.auth_required
def add_lecture_review(args):
    """
    """
    lecture_review_from_db = db.session.query(LectureReview).filter(and_(LectureReview.lecture_id == args.get("lecture_id"), LectureReview.student_id == args.get("student_id"))).first()
    if not lecture_review_from_db:
        lecture_review = LectureReview(**args)
        db.session.add(lecture_review)
        db.session.commit()
    else:
        for item in args.keys():
            if item=="favorite_checked":
                lecture_review_from_db.favorite_checked = args.get("favorite_checked")
            elif item=="thumbsup_checked":
                lecture_review_from_db.thumbsup_checked = args.get("thumbsup_checked")
            elif item=="thumbsdown_checked":
                lecture_review_from_db.thumbsdown_checked = args.get("thumbsdown_checked")
            elif item=="confuse_checked":
                lecture_review_from_db.confuse_checked = args.get("confuse_checked")
            elif item=="cannot_hear_checked":
                lecture_review_from_db.cannot_hear_checked = args.get("cannot_hear_checked")
            elif item=="cannot_see_checked":
                lecture_review_from_db.cannot_see_checked = args.get("cannot_see_checked")
            elif item=="cannot_see_button_checked":
                lecture_review_from_db.cannot_see_button_checked = args.get("cannot_see_button_checked")
            elif item=="cannot_hear_button_checked":
                lecture_review_from_db.cannot_hear_button_checked = args.get("cannot_hear_button_checked")
            elif item=="needtorepeat_button_checked":
                lecture_review_from_db.needtorepeat_button_checked = args.get("needtorepeat_button_checked")
            elif item=="rate_content":
                lecture_review_from_db.rate_content = args.get("rate_content")
            elif item=="effectively_communicate":
                lecture_review_from_db.effectively_communicate = args.get("effectively_communicate")
            elif item=="examples_clear":
                lecture_review_from_db.examples_clear = args.get("examples_clear")
            db.session.commit()

    return {"id": lecture_review_from_db.id, "message": "Added"}

@bp.route("/lecture_review", methods=["GET"])
@use_args(
    {
        "lecture_id": fields.Integer(required=False, missing=None),
        "student_id": fields.Integer(required=False, missing=None),
    },
    location="query",
)
@flask_praetorian.auth_required
def get_lecture_review(args):
    """
    """
    lecture_review_from_db = db.session.query(LectureReview).filter(and_(LectureReview.lecture_id == args.get("lecture_id"), LectureReview.student_id == args.get("student_id"))).first()
    schema = LectureReviewSchema(many=False)
    result = schema.dump(lecture_review_from_db)
    
    return (jsonify(result), HTTPStatus.OK)


#################### Lecture Review ############################################

#################### Student Question ############################################

@bp.route("/student_question", methods=["POST"])
@use_args(StudentQuestionSchema, location="json")
@flask_praetorian.roles_accepted("student")
@flask_praetorian.auth_required
def add_student_question(args):
    """
    """
    student_question = StudentQuestion(**args)
    db.session.add(student_question)
    db.session.commit()


    return {"id": student_question.id, "message": "Added"}

@bp.route("/student_question", methods=["GET"])
@use_args(
    {
        "lecture_id": fields.Integer(required=False, missing=None),
        "student_id": fields.Integer(required=False, missing=None),
    },
    location="query",
)
@flask_praetorian.auth_required
def get_student_question(args):
    """
    """
    student_question = db.session.query(StudentQuestion).filter(and_(StudentQuestion.lecture_id == args.get("lecture_id"), StudentQuestion.student_id == args.get("student_id"))).all()
    schema = StudentQuestionSchema(many=True)
    result = schema.dump(student_question)
    
    return (jsonify(result), HTTPStatus.OK)


#################### Student Question ############################################