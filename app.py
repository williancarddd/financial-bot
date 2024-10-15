# app.py

from flask import Flask
from config import Config
from models import db
from routes import wa  # Importe depois de wa ser definido
from services.scheduler_service import scheduler
from routes.webhooks import webhook_bp  

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Inicializar extensões
    db.init_app(app)
    scheduler.init_app(app)
    scheduler.start()

    app.register_blueprint(webhook_bp)

    # Definir o app no wa
    wa.server = app

    # Agora importar o webhook para registrar os handlers
    from routes import on_events

    with app.app_context():
        db.create_all()

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000)
