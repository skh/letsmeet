from werkzeug.security import generate_password_hash
from . import db

participation = db.Table('participation',
    db.Column('user_id', db.Integer, db.ForeignKey('appusers.id')),
    db.Column('meeting_id', db.Integer, db.ForeignKey('meetings.id'))
)

class User(db.Model):
    __tablename__ = 'appusers'
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(64), unique=True, index=True)
    name = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    confirmed = db.Column(db.Boolean, default=False)
    meetings = db.relationship('Meeting', secondary=participation)

    @property
    def password(self):
        raise AttributeError('password is write-only')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

class Meeting(db.Model):
    __tablename__ = 'meetings'
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(256), unique=True, index=True)
    actions = db.relationship('Action')
    topics = db.relationship('Topic')
    timeslots = db.relationship('Timeslot')
    users = db.relationship('User', secondary=participation)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'title': self.title
        }
    

class Action(db.Model):
    __tablename__ = 'actions'
    id = db.Column(db.Integer, primary_key = True)
    text = db.Column(db.Text())
    meeting_id = db.Column(db.Integer, db.ForeignKey('meetings.id'))

class Topic(db.Model):
    __tablename__ = 'topics'
    id = db.Column(db.Integer, primary_key = True)
    text = db.Column(db.Text())
    meeting_id = db.Column(db.Integer, db.ForeignKey('meetings.id'))

class Timeslot(db.Model):
    __tablename__ = 'timeslots'
    id = db.Column(db.Integer, primary_key = True)
    datetime = db.Column(db.DateTime())
    active = db.Column(db.Boolean, default=False)
    meeting_id = db.Column(db.Integer, db.ForeignKey('meetings.id'))

