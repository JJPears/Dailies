import datetime
from app import db



# Main user model, each user linked to a list of dailies they can achieve
# Maybe I want them to be able to link to long term goals?
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    habits = db.relationship('habit', backref='user', lazy=True)


# TODO need to do email validation/verification
# TODO need to do password hashing?


class habit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
