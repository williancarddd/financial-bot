from flask_apscheduler import APScheduler
from models import db, User, Transaction, Configuration
from templates import message
from datetime import datetime, timedelta
from routes import wa
import logging

scheduler = APScheduler()

def send_daily_summaries():
    with scheduler.app.app_context():
        users = User.query.all()
        for user in users:
            config = Configuration.query.filter_by(user_id=user.id).first()
            if not config:
                continue

            now = datetime.utcnow().time()
            if now.hour == config.daily_summary_time.hour and now.minute == config.daily_summary_time.minute:
                # Calcular transações de hoje
                today = datetime.utcnow().date()
                transactions = Transaction.query.filter(
                    Transaction.user_id == user.id,
                    Transaction.date_time >= datetime.combine(today, datetime.min.time()),
                    Transaction.date_time <= datetime.combine(today, datetime.max.time())
                ).all()
                # Enviar resumo
                message = message.daily_summary(user, transactions)
                wa.send_message(user.phone_number, message)

# Agendar o envio dos resumos diários
scheduler.add_job(
    id='send_daily_summaries',
    func=send_daily_summaries,
    trigger='interval',
    minutes=1  # Ajuste o intervalo conforme necessário
)
