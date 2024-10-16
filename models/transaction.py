from . import db
from datetime import datetime

class Transaction(db.Model):
    __tablename__ = 'transactions'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    value = db.Column(db.Float, nullable=False)
    money_type = db.Column(db.String(20), nullable=False)  # 'spent', 'received', 'saved'
    category = db.Column(db.String(50), nullable=True)  # Categoria opcional
    currency = db.Column(db.String(10), default='BRL')  # Moeda (padrão: BRL)
    date_time = db.Column(db.DateTime, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Transaction {self.id} - {self.money_type} - R$ {self.value}>'