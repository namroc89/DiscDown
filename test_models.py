from models import db, User, Follows, UserRound
from sqlalchemy import exc
from unittest import TestCase
from datetime import datetime
import os
os.environ['DATABASE_URL'] = "postgresql:///discgolf-test"  # noqa
from app import app

db.create_all()


class UserModelTestCase(TestCase):
    """Testing the user model"""

    def setUp(self):
        """Create test client and set up sample data"""
        db.drop_all()
        db.create_all()
        user1 = User.signup("natwil", "Nate",
                            "Williams", 'nate@mail.com', 'password')
        user1id = 100
        user1.id = user1id
        user2 = User.signup("danove", "Dan",
                            "Overholt", 'dan@mail.com', 'password')
        user2id = 101
        user2.id = user2id

        db.session.commit()

        u1 = User.query.get(user1id)
        u2 = User.query.get(user2id)

        self.u1 = u1
        self.u1id = user1id

        self.u2 = u2
        self.u2id = user2id

        self.client = app.test_client()

    def tearDown(self):
        res = super().tearDown()
        db.session.rollback()
        return res

    def test_user_model(self):
        """does basic user model work"""

        user = User(username="test", first_name="John",
                    last_name="Doe", email='john@mail.com', password='password')

        db.session.add(user)
        db.session.commit()

        self.assertEqual(len(user.followers), 0)
        self.assertEqual(len(user.user_rounds), 0)
        self.assertEqual(user.avatar, '/static/images/default_avatar.jpg')
        self.assertEqual(user.bio, None)

        ############
        ### Testing following ###

    def test_user_follows(self):
        """Tests to see if user can be added and removed from follows"""
        self.u1.following.append(self.u2)

        db.session.commit()

        self.assertEqual(len(self.u1.following), 1)
        self.assertEqual(len(self.u2.followers), 1)
        self.assertEqual(self.u2.followers[0], self.u1)
        self.assertEqual(self.u1.following[0], self.u2)

        self.u2.followers.remove(self.u1)
        db.session.commit()

        self.assertEqual(len(self.u1.following), 0)
        self.assertEqual(len(self.u2.followers), 0)

    ##############################
    # testing user signups

    def test_valid_signup(self):
        """tests if user can sign up using valind information"""

        user = User.signup('testytest', 'test', 'user',
                           'test@mail.com', 'password')
        user.id = 1000
        db.session.commit()

        self.assertEqual(user.username, 'testytest')
        self.assertEqual(user.first_name, 'test')
        self.assertEqual(user.last_name, 'user')
        self.assertEqual(user.email, 'test@mail.com')
        self.assertEqual(user.id, 1000)
        self.assertNotEqual(user.email, 'password')
        self.assertTrue(user.password.startswith('$2b$'))
        self.assertEqual(len(User.query.all()), 3)

    def test_repeated_username(self):
        """check if user receives error with invalid username"""
        user = User.signup('natwil', 'test', 'user',
                           'test@mail.com', 'password')
        user.id = 1000

        with self.assertRaises(exc.IntegrityError) as context:
            db.session.commit()

    def test_none_username(self):
        """check if user receives error when not entering username"""
        user = User.signup(None, 'test', 'user',
                           'test@mail.com', 'password')
        user.id = 1000

        with self.assertRaises(exc.IntegrityError) as context:
            db.session.commit()

    def test_repeated_email(self):
        """check if user receives error with invalid email"""
        user = User.signup('testytest', 'test', 'user',
                           'dan@mail.com', 'password')
        user.id = 1000

        with self.assertRaises(exc.IntegrityError) as context:
            db.session.commit()

    def test_none_email(self):
        """check if user receives error when not entering email"""
        user = User.signup('tester', 'test', 'user',
                           None, 'password')
        user.id = 1000

        with self.assertRaises(exc.IntegrityError) as context:
            db.session.commit()

    def test_invalid_pass(self):
        """tests to see if error is thrown when entering an invalid password"""

        with self.assertRaises(ValueError) as context:
            invalid_user = User.signup('tester', 'test', 'user',
                                       'test@mail.com', None)

        with self.assertRaises(ValueError) as context:
            invalid_user = User.signup('tester', 'test', 'user',
                                       'test@mail.com', '')

    def test_valid_authentication(self):
        """Test user is logged in, when giving correct credentials"""
        user = User.authenticate('danove', 'password')

        self.assertEqual(user.id, 101)
        self.assertIsNotNone(user)

    def test_invalid_username(self):
        """if invalid username is entered, user will not be authenticated"""
        self.assertFalse(User.authenticate('invalid', 'password'))
        self.assertFalse(User.authenticate('', 'password'))

    def test_wrong_password(self):
        """if password doesnt match user, user cannot log in"""
        self.assertFalse(User.authenticate('danove', 'wrongpass'))
        self.assertFalse(User.authenticate('danove', ''))


class UserRoundTestCase(TestCase):
    """testing user round model"""

    def setUp(self):

        db.drop_all()
        db.create_all()
        user = User.signup("natwil", "Nate",
                           "Williams", 'nate@mail.com', 'password')
        userid = 100
        user.id = userid

        db.session.commit()

        u = User.query.get(userid)

        self.u = u
        self.uid = userid

        uround = UserRound(user_id=100, course_id=1,
                           course_name="Oak Park", date=datetime(2020, 10, 16), score=70)
        uroundid = 1000
        uround.id = uroundid

        db.session.add(uround)
        db.session.commit()

        rnd = UserRound.query.get(uroundid)

        self.rnd = rnd
        self.rndid = uroundid

        self.client = app.test_client()

    def tearDown(self):
        res = super().tearDown()
        db.session.rollback()
        return res

    def test_user_round_model(self):
        """can a basic round be created"""

        rnd1 = UserRound(user_id=100, course_id=1,
                         course_name="Oak Park", date=datetime(2020, 10, 16), score=70)
        rnd1.id = 1001

        db.session.add(rnd1)
        db.session.commit()

        self.assertEqual(rnd1.id, 1001)
        self.assertEqual(rnd1.user_id, 100)
        self.assertEqual(rnd1.course_id, 1)
        self.assertEqual(rnd1.score, 70)
        self.assertEqual(rnd1.notes, None)

    def test_user_rounds(self):
        """test if round appears in user model relationship"""

        self.assertEqual(len(self.u.user_rounds), 1)
        self.assertEqual(self.rnd.user_id, self.uid)

    def test_user_cascade_delete(self):
        """is round removed when user is deleted"""

        db.session.delete(self.u)
        db.session.commit()

        self.assertFalse(UserRound.query.get(1001))
