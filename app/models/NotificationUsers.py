from app.models import db
import app.config as config

class NotificationUsers(db.Model):
    __tablename__ = "notification_users"
    __tableargs__ = {"schema": config.DB_NAME}
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255))
    notification_types = db.Column(db.String(255))