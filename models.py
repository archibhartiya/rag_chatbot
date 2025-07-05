from datetime import datetime
from database import db
import uuid

class Complaint(db.Model):
    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4())[:8])
    name = db.Column(db.String(50))
    phone_number = db.Column(db.String(15))
    email = db.Column(db.String(100))
    complaint_details = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
