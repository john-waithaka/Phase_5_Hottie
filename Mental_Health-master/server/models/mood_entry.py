from models.mood_entry import MoodEntry  # Import MoodEntry first

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    
    # Relationship with MoodEntry
    mood_entries = db.relationship('MoodEntry', backref='user', lazy=True)