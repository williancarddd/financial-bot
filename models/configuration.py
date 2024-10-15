from . import db
from datetime import datetime

class Configuration(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    daily_summary_time = db.Column(db.Time, nullable=False)
    monthly_summary_day = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Configuration for User {self.user_id}>'
