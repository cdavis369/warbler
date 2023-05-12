"""User model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py


import os
from unittest import TestCase

from models import db, User, Message, Follows

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler_test"


# Now we can import app

from app import app

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()


class UserModelTestCase(TestCase):
    """Test model for users."""

    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        Message.query.delete()
        Follows.query.delete()
        self.u = User.signup(username="testuser",
                             email="test@test.com",
                             password="HASHED_PASSWORD",
                             image_url=User.image_url.default.arg)
        self.u2 = User.signup(username="testuser2",
                             email="test2@test.com",
                             password="HASHED_PASSWORD",
                             image_url=User.image_url.default.arg)
        db.session.commit()
        self.client = app.test_client()

    def test_user_model(self):
        """Does basic model work?"""

        # User should have no messages & no followers
        self.assertEqual(len(self.u.messages), 0)
        self.assertEqual(len(self.u.followers), 0)
        self.assertEqual(len(self.u2.messages), 0)
        self.assertEqual(len(self.u2.followers), 0)
        
    def test_user_follow(self):
        """Test users following and being followed."""
        self.u.following.append(self.u2)
        db.session.commit()
        self.assertEqual(len(self.u2.followers), 1)
        self.assertEqual(self.u2.is_followed_by(self.u), True)
        self.assertEqual(self.u.is_following(self.u2), True)
        
        self.u.following.remove(self.u2)
        db.session.commit()
        self.assertEqual(len(self.u.followers), 0)
        self.assertEqual(self.u2.is_followed_by(self.u), False)
        self.assertEqual(self.u.is_following(self.u2), False)
        
        
    def test_password_authentication(self):
        """Test password authentication."""
        a = User.authenticate("testuser", "HASHED_PASSWORD")
        self.assertEqual(a, self.u)
        
        a = User.authenticate("********", "HASHED_PASSWORD")
        self.assertFalse(a)
        
        a = User.authenticate("testuser", "********")
        self.assertFalse(a)