from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt


bcrypt = Bcrypt()
db = SQLAlchemy()


def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)


class Follows(db.Model):

    __tablename__ = 'follows'

    user_following_id = db.Column(db.Integer, db.ForeignKey(
        'users.id', ondelete='cascade'), primary_key=True)

    user_followed_id = db.Column(db.Integer, db.ForeignKey(
        'users.id', ondelete='cascade'), primary_key=True)


class User(db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    username = db.Column(db.String(15), unique=True, nullable=False)

    first_name = db.Column(db.String(30), nullable=False)

    last_name = db.Column(db.String(30), nullable=False)

    location = db.Column(db.String(50), default="Earth")

    email = db.Column(db.String(50), unique=True, nullable=False)

    password = db.Column(db.String(15), nullable=False)

    bio = db.Column(db.String(200))

    avatar = db.Column(db.Text)

    favorite_courses = db.relationship('FavoriteCourse', backref="users")

    user_rounds = db.relationship('UserRound', backref="users")

    group_rounds = db.relationship(
        'GroupRound', secondary='user_rounds', backref="users")

    followers = db.relationship(
        "User",
        secondary="follows",
        primaryjoin=(Follows.user_followed_id == id),
        secondaryjoin=(Follows.user_following_id == id)
    )

    following = db.relationship(
        "User",
        secondary="follows",
        primaryjoin=(Follows.user_following_id == id),
        secondaryjoin=(Follows.user_followed_id == id)
    )

    def __repr__(self):
        return f"<User {self.id}, {self.username}>"


class FavoriteCourse(db.Model):

    __tablename__ = "favorite_courses"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    user_id = db.Column(db.Integer, db.ForeignKey(
        'users.id', ondelete='cascade'))

    course_id = db.Column(db.Integer, unique=True, nullable=False)

    best_score = db.Column(db.Integer)


class GroupRound(db.Model):

    __tablename__ = "group_rounds"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    course_id = db.Column(db.Integer, nullable=False)

    date = db.Column(db.DateTime, nullable=False)


class UserRound(db.Model):

    __tablename__ = "user_rounds"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    user_id = db.Column(db.Integer, db.ForeignKey(
        'users.id', ondelete='cascade'))

    course_id = db.Column(db.Integer, nullable=False)

    date = db.Column(db.DateTime, nullable=False)

    score = db.Column(db.String(3))

    group_rd_id = db.Column(db.Integer, db.ForeignKey(
        'group_rounds.id', ondelete='cascade'))

    notes = db.Column(db.String(200))
