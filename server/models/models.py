from datetime import datetime
from database import db



# Main user model, each user linked to a list of dailies they can achieve
# Maybe I want them to be able to link to long term goals?
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=False, nullable=False)
    email = db.Column(db.String(100), unique=False, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    # created_at = db.Column(db.DateTime, default=datetime.utcnow)
    # last_login = db.Column(db.DateTime)
    habits = db.relationship('habit', backref='user', lazy=True)


    # this will update the whole object, including setting null values
    def update(self, user_data):
        if 'username' in user_data:
            self.username = user_data['username']
        if 'email' in user_data:
            self.email = user_data['email']
        if 'password' in user_data:
            self.password = user_data['password']
        if 'habits' in user_data:
            self.habits = user_data['habits']


# TODO need to do email validation/verification
# TODO need to do password hashing?


class Habit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
