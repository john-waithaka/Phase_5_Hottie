
#Warui

from extensions import db
from datetime import datetime
import uuid

class Treatment(db.Model):
    __tablename__ = 'treatments'

    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    treatment_name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    patient_id = db.Column(db.String, db.ForeignKey('user.id'), nullable=False)
    therapist_id = db.Column(db.String, db.ForeignKey('user.id'), nullable=False)
    start_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    end_date = db.Column(db.DateTime, nullable=True)
    is_active = db.Column(db.Boolean, default=True)

    # Relationships with the User model
    patient = db.relationship('User', foreign_keys=[patient_id], backref='treatments_as_patient', lazy=True)
    therapist = db.relationship('User', foreign_keys=[therapist_id], backref='treatments_as_therapist', lazy=True)

    def __repr__(self):
        return f'<Treatment {self.treatment_name} for patient {self.patient_id}>'

