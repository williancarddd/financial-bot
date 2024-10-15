from flask import Blueprint, request, make_response
from config import Config

webhook_bp = Blueprint('webhook_bp', __name__)

@webhook_bp.route('/webhook', methods=['GET'])
def whatsapp_webhook_verification():
    # Obter o token de verificação do arquivo de configuração
    VERIFY_TOKEN = Config.VERIFY_TOKEN

    # Obter os parâmetros da solicitação GET
    mode = request.args.get('hub.mode')
    token = request.args.get('hub.verify_token')
    challenge = request.args.get('hub.challenge')

    # Verificar se o modo e o token estão presentes
    if mode and token:
        # Verificar se o modo é 'subscribe' e o token é válido
        if mode == 'subscribe' and token == VERIFY_TOKEN:
            print('WEBHOOK_VERIFIED')
            # Responder com o challenge para confirmar a verificação
            return make_response(challenge, 200)
        else:
            # Token inválido ou modo incorreto
            return make_response('Forbidden', 403)
    else:
        # Parâmetros ausentes
        return make_response('Bad Request', 400)
