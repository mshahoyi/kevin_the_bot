from whatsapp_api_client_python import API as WhatsAppAPI
from .base_bot import BaseBot
from responses import get_response_for_message

class WhatsAppBot(BaseBot):
    def __init__(self, config):
        super().__init__(config)
        self.client = WhatsAppAPI(
            base_url="https://api.whatsapp.com",
            token=config.WHATSAPP_TOKEN
        )

    async def start(self):
        # Initialize WhatsApp webhook listener
        pass

    async def process_webhook(self, webhook_data):
        message = webhook_data.get('message', {})
        sender = message.get('from')
        text = message.get('text', {}).get('body', '')
        
        response = get_response_for_message(text)
        await self.send_response(response, {'sender': sender})

    async def send_response(self, response, context):
        if isinstance(response, dict):
            text = response.get('text', '') or response.get('caption', '')
        else:
            text = response
        await self.client.send_message(
            phone_number=context['sender'],
            message=text
        ) 