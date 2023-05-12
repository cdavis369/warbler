"""Message model tests."""

import os
from unittest import TestCase
from models import db, User, Message

os.environ['DATABASE_URL'] = "postgresql:///warbler_test"

from app import app

db.create_all()

class MessageModelTestCase(TestCase):
    """Test model for messages."""

    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        Message.query.delete()
        self.u = User.signup(username="testuser",
                             email="test@test.com",
                             password="HASHED_PASSWORD",
                             image_url=User.image_url.default.arg)
        db.session.commit()
        self.client = app.test_client()
        
    def test_message_model(self):
      """Test creating a message."""
      msg = Message(text="Test message.")
      self.u.messages.append(msg)
      db.session.commit()
      msg = Message.query.filter_by(user_id=self.u.id).one()
      self.assertEqual(msg.text, "Test message.")
      
    def test_message_delete(self):
      """Test deleting a message."""
      msg = Message(text="Test message.")
      self.u.messages.append(msg)
      db.session.commit()
      msg = Message.query.filter_by(user_id=self.u.id).first()
      self.assertEqual(msg, None)
      

