from models import db, User, Follows, UserRound
from sqlalchemy import exc
from unittest import TestCase
import os
os.environ['DATABASE_URL'] = "postgresql:///discgolf-test"  # noqa
from app import app

db.create_all()

class UserModelTestCase(TestCase)