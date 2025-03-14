from . import db
from datetime import datetime

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    phone_number = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    balance = db.Column(db.Float, default=0.0)  # Saldo atual do usuário
    preferences = db.Column(db.JSON, nullable=True)  # Preferências do usuário
    stripe_customer_id = db.Column(db.String(255), nullable=True)  # ID do cliente no Stripe
    stripe_subscription_id = db.Column(db.String(255), nullable=True)  # ID da assinatura no Stripe
    stripe_subscription_status = db.Column(db.String(50), nullable=True)  # Status da assinatura no Stripe

    # Relacionamentos
    transactions = db.relationship('Transaction', backref='user', lazy=True)

    def __repr__(self):
        return f'<User {self.phone_number}>'