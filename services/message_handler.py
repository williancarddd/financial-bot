from models import db, User, Transaction
from pywa import WhatsApp
from pywa.types import Message, CallbackButton

from utils.format_brazilian_number import format_brazilian_number
from utils.openai_api import openai_api
from datetime import datetime

from template.messages import (
    welcome_message,
    introduction_message,
    transaction_confirmation,
    daily_summary,
)
from models import User, Transaction
from datetime import datetime

class MessageHandler:
    def __init__(self, client: WhatsApp):
        self.client = client

    def process_button_callback(self, callback: CallbackButton):
        print(f"🔘 Botão pressionado por {callback.from_user.name}: {callback.payload}")
        user_phone = format_brazilian_number(callback.from_user.wa_id)
        user = User.query.filter_by(phone_number=user_phone).first()

        if callback.payload == "use_1_day":
            pass
        elif callback.payload == "daily_summary":
            transactions = Transaction.query.filter_by(user_id=user.id).all()
            summary_msg = daily_summary(user, transactions)
            self.client.send_message(user_phone, summary_msg)

    def process_message(self, msg: Message):

        print(f"📲 Mensagem recebida de {msg.from_user.name}: {msg.text}")
        user_phone = format_brazilian_number(msg.from_user.wa_id)
        user = User.query.filter_by(phone_number=user_phone).first()

        if not user:
            user = self.register_new_user(user_phone, msg.from_user.name)
            self.send_welcome_sequence(user_phone)

        # else:
        #     message_text = msg.text
        #     self.process_financial_message(user, message_text)

        self.client.send_message(user_phone, "🤖 Desculpe, ainda estou em desenvolvimento e não posso processar mensagens financeiras.")

    def register_new_user(self, user_phone, user_name):
        user = User(phone_number=user_phone, name=user_name)
        db.session.add(user)
        db.session.commit()
        return user

    def send_welcome_sequence(self, user_phone):
        """Enviar mensagens de boas-vindas e introdução para novos usuários."""
        self.client.send_message(user_phone, welcome_message())
        self.client.send_message(user_phone, introduction_message(),
                                  buttons=[{"text": "Usar por 1 dia.", "payload": "use_1_day"}]
                                  )

    def process_financial_message(self, user, message_text):
        result = openai_api.create_completation(message_text)

        try:
            data = eval(result)
            transaction = Transaction(
                user_id=user.id,
                value=data['value'],
                money_type=data['money_type'],
                category=data.get('category', 'Outros'),
                currency=data.get('currency', 'BRL'),
                date_time=datetime.fromisoformat(data['date_time']),
            )
            db.session.add(transaction)

            # Atualiza o saldo do usuário
            if transaction.money_type == 'received':
                user.balance += transaction.value
            elif transaction.money_type == 'spent':
                user.balance -= transaction.value

            db.session.commit()

            confirmation_msg = transaction_confirmation(transaction)
            self.client.send_message(user.phone_number, confirmation_msg)

        except Exception as e:
            self.client.send_message(user.phone_number, "⚠️ Houve um erro ao registrar sua transação.")

    def daily_summary(user, transactions):
        summary_by_category = {}
        for t in transactions:
            category = t.category or 'Outros'
            summary_by_category[category] = summary_by_category.get(category, 0) + t.value

        total_spent = sum(t.value for t in transactions if t.money_type == 'spent')
        total_received = sum(t.value for t in transactions if t.money_type == 'received')

        category_summary = "\n".join([f"- {cat}: R$ {val:.2f}" for cat, val in summary_by_category.items()])
        
        return (
            f"📅 Resumo Diário - {user.name}:\n"
            f"- Total gasto: R$ {total_spent:.2f}\n"
            f"- Total recebido: R$ {total_received:.2f}\n\n"
            "📂 Resumo por Categoria:\n"
            f"{category_summary}\n\n"
            "📈 Continue registrando suas transações para manter seu controle atualizado."
        )

