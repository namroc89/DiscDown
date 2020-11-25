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

    password = db.Column(db.Text, nullable=False)

    bio = db.Column(db.String(200))

    fav_course = db.Column(db.Text)

    avatar = db.Column(db.Text, default='/static/images/default_avatar.jpg')

    user_rounds = db.relationship('UserRound', backref="user")

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

    @classmethod
    def authenticate(cls, username, password):
        """Find a user with username and password. 
        Checks to see if user matches hashed password.
        returns false if username and password do not match.
        """
        user = cls.query.filter_by(username=username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user

        return False

    @classmethod
    def signup(cls, username, first_name, last_name, email, password):
        """Sign up user.
        Hashes password and adds user to system.
        """

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=hashed_pwd,
        )

        db.session.add(user)
        return user


# class FavoriteCourse(db.Model):

#     __tablename__ = "favorite_courses"

#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)

#     user_id = db.Column(db.Integer, db.ForeignKey(
#         'users.id', ondelete='cascade'))

#     course_id = db.Column(db.Integer, unique=True, nullable=False)

#     best_score = db.Column(db.Integer)


class GroupRound(db.Model):

    __tablename__ = "group_rounds"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    course_id = db.Column(db.Integer, nullable=False)

    course_name = db.Column(db.Text, nullable=False)

    date = db.Column(db.DateTime, nullable=False)

    user_rounds = db.relationship('UserRound', backref="group_rounds")


class UserRound(db.Model):

    __tablename__ = "user_rounds"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    user_id = db.Column(db.Integer, db.ForeignKey(
        'users.id', ondelete='cascade'))

    course_id = db.Column(db.Integer, nullable=False)

    course_name = db.Column(db.Text, nullable=False)

    date = db.Column(db.Date, nullable=False)

    score = db.Column(db.Integer)

    group_rd_id = db.Column(db.Integer, db.ForeignKey(
        'group_rounds.id', ondelete='cascade'))

    notes = db.Column(db.String(200))
