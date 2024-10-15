
from routes import wa
from services.message_handler import MessageHandler

@wa.on_message()
def handle_message(client, msg):
    handler = MessageHandler(client)
    handler.process_message(msg)

@wa.on_callback_button()
def handle_callback(client, callback):
    handler = MessageHandler(client)
    handler.process_callback(callback)
