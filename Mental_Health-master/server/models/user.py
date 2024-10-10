
#main code
#  Define the User model, with attributes and relationships to other entities.

from extensions import db, bcrypt
from datetime import datetime
import uuid

class User(db.Model):
    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    email = db.Column(db.String, unique=True, nullable=False)
    password_hash = db.Column(db.String, nullable=False)
    full_name = db.Column(db.String)
    user_type = db.Column(db.Enum('Patient', 'Therapist', name='user_type'), nullable=False)
    profile_data = db.Column(db.JSON)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)

    # mood_entries = db.relationship('MoodEntry', backref='user', lazy=True)
    # journal_entries = db.relationship('JournalEntry', backref='user', lazy=True)
    # appointments = db.relationship('Appointment', backref='user', lazy=True)
    # therapy_relationships = db.relationship('TherapyRelationship', backref='user', lazy=True)

    def __init__(self, email, password, full_name, user_type, profile_data=None):
        self.email = email
        self.password_hash = bcrypt.generate_password_hash(password)
        self.full_name = full_name
        self.user_type = user_type
        self.profile_data = profile_data or {}

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    def __repr__(self) -> str:
        return f'<user {self.full_name}>'
