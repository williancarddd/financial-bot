from . import db
from datetime import datetime

class UserState(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_phone = db.Column(db.String(20), unique=True, nullable=False)
    state_data = db.Column(db.JSON, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<UserState {self.user_phone}>'
