from models import db, User, Transaction, Configuration
from utils.state_manager import StateManager
from utils.openai_api import parse_financial_message
from templates import message
from datetime import datetime
import logging

class MessageHandler:
    def __init__(self, client):
        self.client = client
        self.state_manager = StateManager()
        self.test_user_phone = '+5569992643914'  # Número de teste

    def process_message(self, msg):
        user_phone = msg.from_user
        # Para testes, usamos o número de teste
        user_phone = self.test_user_phone

        user = User.query.filter_by(phone_number=user_phone).first()

        if not user:
            # Novo usuário, iniciar processo de cadastro
            self.register_new_user(user_phone)
        else:
            # Verificar se o usuário está no processo de cadastro
            state = self.state_manager.get_state(user_phone)
            if state and state['state'] == 'registering':
                self.continue_registration(user_phone, msg.text)
            else:
                # Processar mensagem financeira
                self.process_financial_message(user, msg.text)

    def register_new_user(self, user_phone):
        # Criar novo usuário
        user = User(phone_number=user_phone)
        db.session.add(user)
        db.session.commit()

        # Definir estado do usuário como 'registering' e passo 1
        self.state_manager.set_state(user_phone, {'state': 'registering', 'step': 1})

        # Enviar mensagem de boas-vindas e primeira pergunta
        self.client.send_message(user_phone, message.welcome_message())
        self.ask_registration_question(user_phone, 1)

    def continue_registration(self, user_phone, response):
        state = self.state_manager.get_state(user_phone)
        step = state['step']

        user = User.query.filter_by(phone_number=user_phone).first()

        if step == 1:
            # Salvar nome do usuário
            user.name = response.strip()
            db.session.commit()
            self.state_manager.update_state(user_phone, {'step': 2})
            self.ask_registration_question(user_phone, 2)
        elif step == 2:
            # Salvar horário do resumo diário
            try:
                daily_time = datetime.strptime(response.strip(), '%H:%M').time()
                config = Configuration(user_id=user.id, daily_summary_time=daily_time, monthly_summary_day=1)
                db.session.add(config)
                db.session.commit()
                self.state_manager.update_state(user_phone, {'step': 3})
                self.ask_registration_question(user_phone, 3)
            except ValueError:
                self.client.send_message(user_phone, "Formato de horário inválido. Por favor, use HH:MM.")
        elif step == 3:
            # Salvar dia do resumo mensal
            try:
                day = int(response.strip())
                if 1 <= day <= 31:
                    config = Configuration.query.filter_by(user_id=user.id).first()
                    config.monthly_summary_day = day
                    db.session.commit()
                    # Cadastro concluído
                    self.client.send_message(user_phone, "Configuração concluída! Agora você pode me enviar suas transações.")
                    self.state_manager.clear_state(user_phone)
                else:
                    raise ValueError
            except ValueError:
                self.client.send_message(user_phone, "Por favor, insira um dia válido (1-31).")
        else:
            # Passo inválido, reiniciar cadastro
            self.state_manager.clear_state(user_phone)
            self.client.send_message(user_phone, "Ocorreu um erro na configuração. Vamos começar novamente.")
            self.register_new_user(user_phone)

    def ask_registration_question(self, user_phone, step):
        if step == 1:
            question = "Qual é o seu nome?"
        elif step == 2:
            question = "Qual horário você prefere receber o resumo diário? (HH:MM)"
        elif step == 3:
            question = "Em que dia do mês você prefere receber o resumo mensal? (1-31)"
        else:
            return
        self.client.send_message(user_phone, question)

    def process_financial_message(self, user, message_text):
        # Processar a mensagem financeira usando a API da OpenAI
        response = parse_financial_message(message_text)
        try:
            financial_data = eval(response)
            transaction = Transaction(
                user_id=user.id,
                value=financial_data.get('value'),
                money_type=financial_data.get('money_type'),
                date_time=financial_data.get('date_time', datetime.utcnow())
            )
            db.session.add(transaction)
            db.session.commit()
            self.client.send_message(user.phone_number, message.transaction_confirmation(transaction))
        except Exception as e:
            logging.error(f"Erro ao processar mensagem financeira: {e}")
            self.client.send_message(user.phone_number, "Não foi possível processar sua mensagem. Por favor, tente novamente.")

    def process_callback_button(self, callback):
        # Handle interactions with buttons if necessary
        pass
