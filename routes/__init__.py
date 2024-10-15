from pywa import WhatsApp
from config import Config

class Wa(WhatsApp):
    def __init__(self, app):
        super().__init__(
            phone_id=Config.PHONE_ID,
            server=app,
            verify_token=Config.VERIFY_TOKEN,
            app_id=Config.APP_ID,
            webhook_endpoint=Config.WEBHOOK_ENDPOINT,
            webhook_challenge_delay=Config.WEBHOOK_CHALLENGE_DELAY,
            app_secret=Config.APP_SECRET,
            token=Config.TOKEN,
        )

# Criar uma instância de Wa
wa = Wa(app=None)  # O app será definido posteriormente

# Não importe o webhook aqui para evitar importações circulares
