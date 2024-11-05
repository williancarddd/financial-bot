
from flask import Flask
from config import config
from models import db
from pywa import WhatsApp
from routes.webhooks import webhook_bp
from services.message_handler import MessageHandler

def create_app():
    app = Flask(__name__)
    app.config.from_object(config)
    # Inicializar extensões
    db.init_app(app)
    app.register_blueprint(webhook_bp)

    # Definir o 'wa' com o aplicativo
    wa = WhatsApp(
        app_id=config.APP_ID,
        app_secret=config.APP_SECRET,
        token=config.TOKEN,
        phone_id=config.PHONE_ID,
        server=app,
        callback_url=config.CALLBACK_URL,
        verify_token=config.VERIFY_TOKEN,
        webhook_challenge_delay=config.WEBHOOK_CHALLENGE_DELAY,
    )

    

    @wa.on_message()
    def handle_message(client, msg):
        handler = MessageHandler(client)
        handler.process_message(msg)

    @wa.on_callback_button()
    def handle_callback(client, callback):
        handler = MessageHandler(client)
        handler.process_button_callback(callback)

    with app.app_context():
        db.create_all()

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000)
