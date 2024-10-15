import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Configurações do Flask
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    

    # API da OpenAI
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

    # Configurações da API do WhatsApp
    VERIFY_TOKEN = os.getenv('VERIFY_TOKEN')
    PHONE_ID = os.getenv('PHONE_ID')
    APP_ID = os.getenv('APP_ID')
    CALLBACK_URL = os.getenv('CALLBACK_URL')
    WEBHOOK_CHALLENGE_DELAY = float(os.getenv('WEBHOOK_CHALLENGE_DELAY', 0.5))
    APP_SECRET = os.getenv('APP_SECRET')
    TOKEN = os.getenv('TOKEN')
    WEBHOOK_ENDPOINT = "/webhook"

    # Outras configurações
    TEST_USER_PHONE = '+5569992643914'  # Número de teste
