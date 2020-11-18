from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)

class User(db.model):
    """Creates user model"""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    username = db.Column(db.String(15), unique=True, nullable=False)

    password = db.Column(db.String(15), nullable=False)

    email = db.Column(db.String(50), unique=True, nullable=False)

    first_name = db.Column(db.String(30), nullable=False)

    last_name = db.Column(db.String(30), nullable=False)

    bio = db.Column(db.String(200))

    avatar = db.Column(db.Text)

