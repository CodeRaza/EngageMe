from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

from app.models import User
from app.models import Classroom
from app.models import Lecture
from app.models import LectureMaterial
from app.models import LectureSubtopic
from app.models import QuestionsAndPolls
from app.models import AnswersAndVotes
from app.models import LectureReview
from app.models import StudentQuestion
from app.models import Moderation

